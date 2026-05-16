from django.contrib import admin

# On importe tous nos modèles
from .models import Category, Source, Opportunity, Alert


# @admin.register = enregistre le modèle dans l'interface admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    # Colonnes affichées dans la liste
    list_display = ['name', 'created_at']

    # Champs sur lesquels on peut faire une recherche
    search_fields = ['name']


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):

    # Affiche le nom, l'url, si active et la date
    list_display = ['name', 'url', 'is_active', 'created_at']

    # Filtre sur le côté droit par statut actif/inactif
    list_filter = ['is_active']

    # Recherche par nom
    search_fields = ['name']


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):

    # Affiche les infos principales de chaque opportunité
    list_display = ['title', 'type', 'country', 'score', 'is_active', 'created_at']

    # Filtres sur le côté droit
    list_filter = ['type', 'country', 'is_active']

    # Recherche dans le titre et la description
    search_fields = ['title', 'description']


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):

    # Affiche email, mots clés, pays et statut
    list_display = ['email', 'keywords', 'country', 'is_active', 'created_at']

    # Filtre par statut actif/inactif
    list_filter = ['is_active']

    # Recherche par email et mots clés
    search_fields = ['email', 'keywords']