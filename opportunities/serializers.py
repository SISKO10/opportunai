from rest_framework.serializers import ModelSerializer
from .models import Category, Source, Opportunity, Alert


class CategorySerializer(ModelSerializer):
    """
    Transforme un objet Category en JSON
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class SourceSerializer(ModelSerializer):
    """
    Transforme un objet Source en JSON
    """
    class Meta:
        model = Source
        fields = ['id', 'name', 'url', 'is_active']


class OpportunitySerializer(ModelSerializer):
    """
    Transforme un objet Opportunity en JSON
    On inclut le nom de la catégorie et de la source
    au lieu de juste leur id
    """

    # Affiche le nom de la catégorie
    # au lieu de juste l'id
    category = CategorySerializer(read_only=True)

    # Affiche le nom de la source
    # au lieu de juste l'id
    source = SourceSerializer(read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            'id',
            'title',
            'company',
            'description',
            'summary',
            'type',
            'country',
            'salary',
            'score',
            'url',
            'category',
            'source',
            'is_active',
            'published_at',
            'created_at',
        ]


class OpportunityListSerializer(ModelSerializer):
    """
    Version allégée pour la liste
    (sans description complète pour aller plus vite)
    """
    class Meta:
        model = Opportunity
        fields = [
            'id',
            'title',
            'company',
            'summary',
            'type',
            'country',
            'salary',
            'score',
            'url',
            'published_at',
        ]


class AlertSerializer(ModelSerializer):
    """
    Transforme un objet Alert en JSON
    """
    class Meta:
        model = Alert
        fields = [
            'id',
            'email',
            'keywords',
            'country',
            'type',
            'is_active',
            'created_at',
        ]
