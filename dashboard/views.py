from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from opportunities.models import Opportunity, Source, Category


@login_required(login_url='/login/')
def index(request):
    """
    Vue de la page d'accueil
    Affiche les stats et les meilleures opportunités
    """

    # Statistiques générales
    total_opportunites = Opportunity.objects.filter(
        is_active=True
    ).count()

    total_sources = Source.objects.filter(
        is_active=True
    ).count()

    total_categories = Category.objects.count()

    # Meilleures opportunités (top 6)
    meilleures_opportunites = Opportunity.objects.filter(
        is_active=True,
        score__gt=0
    ).order_by('-score')[:6]

    # Opportunités récentes (6 dernières)
    opportunites_recentes = Opportunity.objects.filter(
        is_active=True
    ).order_by('-created_at')[:6]

    # On envoie tout au template
    context = {
        'total_opportunites': total_opportunites,
        'total_sources': total_sources,
        'total_categories': total_categories,
        'meilleures_opportunites': meilleures_opportunites,
        'opportunites_recentes': opportunites_recentes,
    }

    return render(request, 'dashboard/index.html', context)
