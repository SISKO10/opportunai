from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Count : compte le nombre d'éléments
# Avg : calcule la moyenne
from django.db.models import Count, Avg

from opportunities.models import Opportunity, Source, Category

# Pour créer des graphiques
import plotly.graph_objects as go

# Pour convertir le graphique en HTML
import plotly.offline as opy


@login_required(login_url='/login/')
def index(request):
    """
    Vue de la page d'accueil
    """

    # ═══════════════════════════════════════
    # STATISTIQUES GÉNÉRALES (déjà connu)
    # ═══════════════════════════════════════

    total_opportunites = Opportunity.objects.filter(
        is_active=True
    ).count()

    total_sources = Source.objects.filter(
        is_active=True
    ).count()

    total_categories = Category.objects.count()

    meilleures_opportunites = Opportunity.objects.filter(
        is_active=True,
        score__gt=0
    ).order_by('-score')[:6]

    opportunites_recentes = Opportunity.objects.filter(
        is_active=True
    ).order_by('-created_at')[:6]


    # ═══════════════════════════════════════
    # GRAPHIQUE 1 : Répartition par type
    # ═══════════════════════════════════════

    # .values('type') : on regroupe par type
    # .annotate(total=Count('id')) : on compte combien
    #                                 il y en a dans chaque groupe
    par_type = Opportunity.objects.filter(
        is_active=True
    ).values('type').annotate(total=Count('id'))

    # Résultat de par_type :
    # [
    #   {'type': 'emploi', 'total': 45},
    #   {'type': 'business', 'total': 5},
    # ]


    # Dictionnaire pour traduire les codes en français
    # 'emploi' → 'Emploi'
    labels_type = {
        'emploi': 'Emploi',
        'business': 'Business',
        'formation': 'Formation',
        'appel_offre': "Appel d'offre",
    }

    # On parcourt par_type et on traduit chaque type
    # .get(item['type'], item['type']) :
    # → si 'emploi' existe dans labels_type → 'Emploi'
    # → sinon → garde la valeur originale
    type_labels = [labels_type.get(item['type'], item['type']) for item in par_type]

    # On extrait juste les nombres
    # [45, 5]
    type_values = [item['total'] for item in par_type]


    # On crée un graphique en CAMEMBERT (Pie)
    graphique_type = go.Figure(
        data=[go.Pie(
            labels=type_labels,    # ['Emploi', 'Business']
            values=type_values,    # [45, 5]
            hole=0.4,               # trou au milieu (donut)
            marker=dict(colors=['#2C3E50', '#E74C3C', '#27AE60', '#F39C12'])
            # couleurs personnalisées pour chaque part
        )]
    )

    # On configure l'apparence du graphique
    graphique_type.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),  # marges réduites
        height=300,                            # hauteur en pixels
    )

    # On convertit le graphique Python en code HTML
    # pour pouvoir l'afficher dans le template
    graphique_type_html = opy.plot(
        graphique_type,
        auto_open=False,    # ne pas ouvrir dans un navigateur
        output_type='div'   # retourne du HTML <div>
    )


    # ═══════════════════════════════════════
    # GRAPHIQUE 2 : Répartition par pays
    # ═══════════════════════════════════════

    # Même logique mais groupé par pays
    # .order_by('-total') : trie du plus grand au plus petit
    par_pays = Opportunity.objects.filter(
        is_active=True
    ).values('country').annotate(total=Count('id')).order_by('-total')

    labels_pays = {
        'ci': "Côte d'Ivoire",
        'sn': 'Sénégal',
        'ml': 'Mali',
        'bf': 'Burkina Faso',
        'gn': 'Guinée',
        'cm': 'Cameroun',
        'other': 'Autre',
    }

    pays_labels = [labels_pays.get(item['country'], item['country']) for item in par_pays]
    pays_values = [item['total'] for item in par_pays]

    # Graphique en BARRES (Bar) cette fois
    graphique_pays = go.Figure(
        data=[go.Bar(
            x=pays_labels,    # axe horizontal : noms des pays
            y=pays_values,    # axe vertical : nombres
            marker=dict(color='#2C3E50')  # couleur des barres
        )]
    )

    graphique_pays.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        yaxis_title="Nombre d'opportunités"  # titre de l'axe Y
    )

    graphique_pays_html = opy.plot(
        graphique_pays,
        auto_open=False,
        output_type='div'
    )


    # ═══════════════════════════════════════
    # GRAPHIQUE 3 : Score moyen par catégorie
    # ═══════════════════════════════════════

    # Avg('score') : calcule la moyenne des scores
    # par groupe de type
    scores_par_type = Opportunity.objects.filter(
        is_active=True,
        score__gt=0    # on ignore les offres pas encore analysées
    ).values('type').annotate(score_moyen=Avg('score')).order_by('-score_moyen')

    # Résultat :
    # [
    #   {'type': 'emploi', 'score_moyen': 7.85},
    #   {'type': 'business', 'score_moyen': 6.2},
    # ]

    score_labels = [labels_type.get(item['type'], item['type']) for item in scores_par_type]

    # round(x, 1) : arrondit à 1 décimale
    # 7.853 → 7.9
    score_values = [round(item['score_moyen'], 1) for item in scores_par_type]

    graphique_score = go.Figure(
        data=[go.Bar(
            x=score_labels,
            y=score_values,
            marker=dict(color='#27AE60'),
            text=score_values,        # affiche le chiffre sur la barre
            textposition='auto'       # position automatique du texte
        )]
    )

    graphique_score.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        yaxis_title="Score moyen",
        yaxis_range=[0, 10]    # l'axe Y va de 0 à 10 (échelle des scores)
    )

    graphique_score_html = opy.plot(
        graphique_score,
        auto_open=False,
        output_type='div'
    )


    # ═══════════════════════════════════════
    # ENVOI AU TEMPLATE
    # ═══════════════════════════════════════

    context = {
        'total_opportunites': total_opportunites,
        'total_sources': total_sources,
        'total_categories': total_categories,
        'meilleures_opportunites': meilleures_opportunites,
        'opportunites_recentes': opportunites_recentes,

        # Les 3 graphiques en HTML
        'graphique_type': graphique_type_html,
        'graphique_pays': graphique_pays_html,
        'graphique_score': graphique_score_html,
    }

    return render(request, 'dashboard/index.html', context)
