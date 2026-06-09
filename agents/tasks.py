import subprocess
from celery import shared_task
from opportunities.models import Opportunity
from django.core.mail import send_mail
from django.conf import settings
from groq import Groq


@shared_task
def lancer_scraping():
    """
    Tâche Celery qui lance le spider Scrapy
    automatiquement toutes les 6 heures
    """
    subprocess.run([
        'scrapy', 'crawl', 'emploi_ci',
        '--logfile', '/tmp/scrapy.log'
    ], cwd=str(settings.BASE_DIR / 'scraping'))

    return "Scraping terminé"


@shared_task
def analyser_opportunites():
    """
    Tâche Celery qui analyse toutes les opportunités
    qui n'ont pas encore de résumé IA (summary vide)
    """

    # On récupère les opportunités sans résumé
    opportunites = Opportunity.objects.filter(
        summary='',
        is_active=True
    )

    for opportunite in opportunites:
        analyser_une_opportunite(opportunite.id)

    return f"{opportunites.count()} opportunités analysées"


@shared_task
def analyser_une_opportunite(opportunite_id):
    """
    Tâche Celery qui analyse UNE opportunité
    et génère :
    → un résumé clair en français
    → un score de pertinence (0-10)
    """

    try:
        # On récupère l'opportunité depuis la BDD
        opportunite = Opportunity.objects.get(id=opportunite_id)

        # On prépare le prompt pour Groq
        prompt = f"""
        Analyse cette offre d'emploi et retourne :
        1. Un résumé clair en 3 phrases maximum
        2. Un score de pertinence de 0 à 10

        Titre : {opportunite.title}
        Entreprise : {opportunite.company}
        Description : {opportunite.description[:500]}

        Réponds exactement dans ce format :
        RESUME: [ton résumé ici]
        SCORE: [chiffre entre 0 et 10]
        """

        # On initialise le client Groq
        # avec notre clé API
        client = Groq(api_key=settings.GROQ_API_KEY)

        # On appelle le modèle Llama3 via Groq
        # (gratuit et très rapide)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un expert RH africain qui analyse des offres d'emploi."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300
        )

        # On extrait le texte de la réponse
        texte = response.choices[0].message.content

        # On parse le résumé et le score
        lines = texte.strip().split('\n')
        resume = ''
        score = 0.0

        for line in lines:
            if line.startswith('RESUME:'):
                resume = line.replace('RESUME:', '').strip()
            elif line.startswith('SCORE:'):
                try:
                    score = float(line.replace('SCORE:', '').strip())
                except ValueError:
                    score = 0.0

        # On sauvegarde dans la BDD
        opportunite.summary = resume
        opportunite.score = score
        opportunite.save()

        return f"Opportunité {opportunite_id} analysée - Score: {score}"

    except Exception as e:
        return f"Erreur : {str(e)}"


@shared_task
def envoyer_alertes():
    """
    Tâche Celery qui envoie les meilleures
    opportunités aux abonnés par email
    Lancée automatiquement tous les jours à 8h
    """

    from opportunities.models import Alert, Opportunity

    # On récupère toutes les alertes actives
    alertes = Alert.objects.filter(is_active=True)

    for alerte in alertes:

        # On cherche les opportunités correspondantes
        opportunites = Opportunity.objects.filter(
            is_active=True,
            score__gt=5  # score supérieur à 5
        )

        # Filtre par mots clés
        if alerte.keywords:
            opportunites = opportunites.filter(
                title__icontains=alerte.keywords
            )

        # Filtre par pays
        if alerte.country:
            opportunites = opportunites.filter(
                country=alerte.country
            )

        # Filtre par type
        if alerte.type:
            opportunites = opportunites.filter(
                type=alerte.type
            )

        # On prend les 5 meilleures
        opportunites = opportunites.order_by('-score')[:5]

        # Si des opportunités correspondent
        if opportunites.exists():

            # On construit le message email
            message = f"🌍 OPPORTUN'AI - Vos opportunités du jour\n\n"
            message += f"Mots clés : {alerte.keywords}\n\n"
            message += "─" * 40 + "\n\n"

            for i, opp in enumerate(opportunites, 1):
                message += f"{i}. {opp.title}\n"
                if opp.company:
                    message += f"   Entreprise : {opp.company}\n"
                if opp.summary:
                    message += f"   Résumé : {opp.summary}\n"
                message += f"   Score : ⭐ {opp.score}/10\n"
                message += f"   Voir l'offre : {opp.url}\n\n"

            # On envoie l'email
            send_mail(
                subject=f"🌍 OPPORTUNAI - {opportunites.count()} opportunités pour vous !",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[alerte.email],
                fail_silently=True,
            )

    return f"{alertes.count()} alertes traitées"
