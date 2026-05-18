# On importe le module models de Django
# qui contient tous les types de champs disponibles
from django.db import models


# Chaque classe représente une table dans la base de données
# Category hérite de models.Model pour être reconnue par Django
class Category(models.Model):

    # Champ texte court pour le nom de la catégorie
    # Exemples : "Emploi", "Business", "Formation"
    name = models.CharField(max_length=100)

    # Date et heure de création de la catégorie
    # auto_now_add=True : Django remplit ce champ automatiquement
    # à la création, on n'a pas besoin de le faire manuellement
    created_at = models.DateTimeField(auto_now_add=True)

    # Définit ce qui s'affiche quand on appelle l'objet
    # Sans ça Django afficherait "Category object (1)"
    # Avec ça il affichera le nom ex : "Emploi"
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Source(models.Model):

    # Nom du site scrappé
    # Exemples : "LinkedIn", "Indeed", "Emploi.ci"
    name = models.CharField(max_length=200)

    # URL du site à scrapper
    # Exemple : "https://emploi.ci"
    url = models.URLField()

    # Indique si la source est active ou non
    # True = on scrape ce site
    # False = on ignore ce site temporairement
    is_active = models.BooleanField(default=True)

    # Date de création de la source
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Sources"
    

class Opportunity(models.Model):

    # Liste des types d'opportunités disponibles
    # Format : ('valeur_en_bdd', 'Label affiché')
    TYPE_CHOICES = [
        ('emploi', 'Emploi'),
        ('business', 'Business'),
        ('appel_offre', "Appel d'offre"),
        ('formation', 'Formation'),
    ]

    # Liste des pays disponibles
    COUNTRY_CHOICES = [
        ('ci', "Côte d'Ivoire"),
        ('sn', 'Sénégal'),
        ('ml', 'Mali'),
        ('bf', 'Burkina Faso'),
        ('gn', 'Guinée'),
        ('cm', 'Cameroun'),
        ('other', 'Autre'),
    ]

    # Titre de l'opportunité
    # Exemple : "Développeur Python - Abidjan"
    title = models.CharField(max_length=300)

    # Description complète de l'opportunité
    # TextField = texte long sans limite de caractères
    description = models.TextField()

    # Type d'opportunité parmi TYPE_CHOICES
    # Exemple : "emploi" ou "business"
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # Pays de l'opportunité parmi COUNTRY_CHOICES
    # Exemple : "ci" pour Côte d'Ivoire
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES)

    # Lien vers la catégorie de l'opportunité
    # ForeignKey = relation entre deux tables
    # on_delete=SET_NULL : si la catégorie est supprimée,
    # l'opportunité reste mais sans catégorie (null)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Lien vers la source (site) d'où vient l'opportunité
    # Même logique que category
    source = models.ForeignKey(
        Source,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # URL directe vers l'opportunité
    # blank=True : ce champ n'est pas obligatoire
    url = models.URLField(blank=True)

    # Salaire ou budget proposé
    # Exemple : "800 000 CFA", "À négocier"
    # blank=True : pas toujours disponible
    salary = models.CharField(max_length=100, blank=True)

    # Score de pertinence calculé par l'agent IA
    # 0.0 = pas pertinent, 10.0 = très pertinent
    # default=0.0 : vaut 0 par défaut
    score = models.FloatField(default=0.0)

    # Résumé généré automatiquement par l'agent IA
    # blank=True : rempli plus tard par l'agent
    summary = models.TextField(blank=True)

    # Indique si l'opportunité est encore valide
    # False = expirée ou supprimée
    is_active = models.BooleanField(default=True)

    # Date de publication sur le site source
    # null=True : pas toujours disponible lors du scraping
    published_at = models.DateTimeField(null=True, blank=True)

    # Date d'ajout automatique dans notre BDD
    created_at = models.DateTimeField(auto_now_add=True)

    # Nom de l'entreprise qui recrute
    # blank=True : pas toujours disponible
    company = models.CharField(max_length=200, blank=True)

    # Affiche le titre au lieu de "Opportunity object (1)"
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Opportunities"
        # Trie par score décroissant puis par date décroissante
        # Les meilleures opportunités apparaissent en premier
        ordering = ['-score', '-created_at']

class Alert(models.Model):

    # Email de l'utilisateur qui veut recevoir des alertes
    # EmailField : Django vérifie automatiquement que
    # le format est valide (ex: brahima@gmail.com)
    email = models.EmailField()

    # Mots clés que l'utilisateur recherche
    # Exemple : "développeur python, comptable, marketing"
    keywords = models.CharField(max_length=300)

    # Pays souhaité pour les opportunités
    # blank=True : l'utilisateur peut ne pas filtrer par pays
    # et recevoir les opportunités de tous les pays
    country = models.CharField(max_length=10, blank=True)

    # Type d'opportunité souhaité
    # blank=True : l'utilisateur peut recevoir tous les types
    # Exemple : "emploi", "business", "formation"
    type = models.CharField(max_length=20, blank=True)

    # Indique si l'alerte est active ou non
    # False = l'utilisateur a désactivé ses alertes
    is_active = models.BooleanField(default=True)

    # Date de création de l'alerte
    # Remplie automatiquement par Django
    created_at = models.DateTimeField(auto_now_add=True)

    # Affiche l'email au lieu de "Alert object (1)"
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Alerts"