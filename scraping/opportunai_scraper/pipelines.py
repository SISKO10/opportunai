# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import sys
import django

'''On indique à Django où trouver le projet
__file__
# = chemin du fichier actuel
# = /home/sissoko/projets_perso/opportunai/scraping/opportunai_scraper/pipelines.py

os.path.dirname(__file__)
# = dossier du fichier actuel
# = /home/sissoko/projets_perso/opportunai/scraping/opportunai_scraper/

os.path.join(..., '../../')
# = on remonte de 2 dossiers
# = /home/sissoko/projets_perso/opportunai/

sys.path.append(...)
# = on dit à Python :
# "cherche les modules aussi dans ce dossier" : → /home/sissoko/projets_perso/opportunai/
'''
sys.path.append(os.path.join(os.path.dirname(__file__), '../../')) 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup() # = on initialise Django pour pouvoir utiliser les modeles et la base de donnees

from asgiref.sync import sync_to_async
from opportunities.models import Opportunity, Source


class SaveToDBPipeline:
    """
    Pipeline qui sauvegarde chaque item scrapy
    directement dans la base de données Django
    """

    async def process_item(self, item, spider):
        """
        Méthode async appelée automatiquement pour
        chaque item retourné par le spider.
        sync_to_async permet d'appeler des fonctions
        Django synchrones depuis un contexte async
        """

        # On enveloppe les opérations Django dans
        # sync_to_async pour éviter l'erreur async
        await sync_to_async(self.save_to_db)(item)

        return item

    def save_to_db(self, item):
        """
        Méthode synchrone qui fait le vrai travail
        de sauvegarde en BDD
        """

        # On récupère ou crée la source dans la BDD
        source, created = Source.objects.get_or_create(
            name=item['source_name'],
            defaults={'url': item['source_url']}
        )

        # On vérifie si l'opportunité existe déjà
        # pour éviter les doublons (même URL)
        if not Opportunity.objects.filter(url=item['url']).exists():

            # On sauvegarde l'opportunité en BDD
            Opportunity.objects.create(
                title=item['title'],
                description=item['description'],
                type=item['type'],
                country=item['country'],
                url=item['url'],
                salary=item.get('salary', ''),
                source=source,
                published_at=item.get('published_at') or None,
                company=item.get('company', '')     
            )     
