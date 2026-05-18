import subprocess
from celery import shared_task
from opportunities.models import Opportunity
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
