# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OpportunityItem(scrapy.Item):

    # Titre de l'opportunité
    # Exemple : "Développeur Python - Abidjan"
    title = scrapy.Field()

    # Description complète
    description = scrapy.Field()

    # Type : emploi, business, formation...
    type = scrapy.Field()

    # Pays : ci, sn, ml...
    country = scrapy.Field()

    # Lien direct vers l'opportunité
    url = scrapy.Field()

    # Salaire si disponible
    salary = scrapy.Field()

    # Nom du site source
    # Exemple : "Emploi.ci"
    source_name = scrapy.Field()

    # URL du site source
    source_url = scrapy.Field()

    # Date de publication
    published_at = scrapy.Field()

    # Nom de l'entreprise qui recrute
    company = scrapy.Field()
