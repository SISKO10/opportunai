from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Source, Opportunity, Alert
from .serializers import (
    CategorySerializer,
    SourceSerializer,
    OpportunitySerializer,
    OpportunityListSerializer,
    AlertSerializer
)


class CategoryListView(APIView):
    """
    Retourne la liste de toutes les catégories
    GET /api/categories/
    """
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class SourceListView(APIView):
    """
    Retourne la liste de toutes les sources
    GET /api/sources/
    """
    def get(self, request):
        sources = Source.objects.all()
        serializer = SourceSerializer(sources, many=True)
        return Response(serializer.data)


class OpportunityListView(APIView):
    """
    Retourne la liste de toutes les opportunités
    avec filtres optionnels
    GET /api/opportunites/
    GET /api/opportunites/?type=emploi
    GET /api/opportunites/?country=ci
    GET /api/opportunites/?type=emploi&country=ci
    """
    def get(self, request):

        # On récupère toutes les opportunités actives
        opportunites = Opportunity.objects.filter(is_active=True)

        # Filtre optionnel par type
        # Exemple : ?type=emploi
        type_filtre = request.query_params.get('type')
        if type_filtre:
            opportunites = opportunites.filter(type=type_filtre)

        # Filtre optionnel par pays
        # Exemple : ?country=ci
        country_filtre = request.query_params.get('country')
        if country_filtre:
            opportunites = opportunites.filter(country=country_filtre)

        # Filtre optionnel par mot clé dans le titre
        # Exemple : ?search=developpeur
        search = request.query_params.get('search')
        if search:
            opportunites = opportunites.filter(
                title__icontains=search
            )

        # On sérialise avec la version allégée
        serializer = OpportunityListSerializer(
            opportunites,
            many=True
        )
        return Response({
            'count': opportunites.count(),
            'results': serializer.data
        })


class OpportunityDetailView(APIView):
    """
    Retourne le détail d'une opportunité
    GET /api/opportunites/<id>/
    """
    def get(self, request, pk):
        try:
            opportunite = Opportunity.objects.get(
                id=pk,
                is_active=True
            )
            serializer = OpportunitySerializer(opportunite)
            return Response(serializer.data)

        except Opportunity.DoesNotExist:
            return Response(
                {'erreur': 'Opportunité non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )


class OpportunityTopView(APIView):
    """
    Retourne les meilleures opportunités
    triées par score décroissant
    GET /api/opportunites/top/
    GET /api/opportunites/top/?limit=5
    """
    def get(self, request):

        # Nombre d'opportunités à retourner
        # Par défaut 10, modifiable via ?limit=5
        limit = int(request.query_params.get('limit', 10))

        opportunites = Opportunity.objects.filter(
            is_active=True,
            score__gt=0  # score supérieur à 0
        ).order_by('-score')[:limit]

        serializer = OpportunityListSerializer(
            opportunites,
            many=True
        )
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })


class AlertCreateView(APIView):
    """
    Crée une nouvelle alerte email
    POST /api/alertes/
    """
    def post(self, request):
        serializer = AlertSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Alerte créée avec succès !',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@login_required(login_url='/login/')
def opportunite_list(request):
    """
    Vue de la liste des opportunités
    avec filtres et pagination
    """

    opportunites = Opportunity.objects.filter(is_active=True)

    # Filtres
    type_filtre = request.GET.get('type')
    if type_filtre:
        opportunites = opportunites.filter(type=type_filtre)

    country_filtre = request.GET.get('country')
    if country_filtre:
        opportunites = opportunites.filter(country=country_filtre)

    search = request.GET.get('search')
    if search:
        opportunites = opportunites.filter(
            title__icontains=search
        )

    total = opportunites.count()

    # ─────────────────────────────────────
    # PAGINATION
    # ─────────────────────────────────────

    # On affiche 10 opportunités par page
    paginator = Paginator(opportunites, 10)

    # On récupère le numéro de page demandé
    # Exemple : ?page=2
    page_number = request.GET.get('page', 1)

    # On récupère les opportunités de cette page
    page_obj = paginator.get_page(page_number)

    context = {
        'opportunites': page_obj,  # ← contient les 10 résultats de la page
        'page_obj': page_obj,      # ← infos de pagination (page actuelle, total...)
        'total': total,
        'type_filtre': type_filtre or '',
        'country_filtre': country_filtre or '',
        'search': search or '',
    }

    return render(request, 'opportunities/list.html', context)
   

@login_required(login_url='/login/')
def opportunite_detail(request, pk):
    """
    Vue du détail d'une opportunité
    """

    # get_object_or_404 retourne automatiquement
    # une erreur 404 si l'objet n'existe pas
    opportunite = get_object_or_404(
        Opportunity,
        id=pk,
        is_active=True
    )

    context = {
        'opportunite': opportunite,
    }

    return render(request, 'opportunities/detail.html', context)
