import scrapy
from opportunai_scraper.items import OpportunityItem


class EmploiCiSpider(scrapy.Spider):

    # Nom unique du spider
    name = 'emploi_ci'

    # Pays associé à ce spider
    country = 'ci'

    # URL de départ : page des offres d'emploi
    start_urls = ['https://emploi.ci/recherche-jobs-cote-ivoire']

    def parse(self, response):
        """
        Scrapy appelle cette méthode automatiquement
        pour chaque page visitée
        """

        # On cherche tous les blocs d'offres sur la page
        # Chaque offre est dans un div.card-job-detail
        for offre in response.css('.card-job-detail'):

            # On crée un conteneur vide pour chaque offre
            item = OpportunityItem()

            # Titre de l'offre
            # Exemple : "Commercial - Abidjan"
            item['title'] = offre.css('h3 a::text').get(default='').strip()

            # URL complète de l'offre
            # urljoin() transforme "/offre/123" en
            # "https://emploi.ci/offre/123"
            item['url'] = response.urljoin(
                offre.css('h3 a::attr(href)').get(default='')
            )

            # Nom de l'entreprise qui recrute
            item['company'] = offre.css(
                '.card-job-company::text'
            ).get(default='').strip()

            # Description du poste
            item['description'] = offre.css(
                '.card-job-description p::text'
            ).get(default='').strip()

            # Date de publication
            # datetime="2026-05-15" → on prend l'attribut
            item['published_at'] = offre.css(
                'time::attr(datetime)'
            ).get(default='')

            # Informations fixes pour toutes les offres
            # de ce spider
            item['type'] = 'emploi'
            item['country'] = self.country
            item['source_name'] = 'Emploi.ci'
            item['source_url'] = 'https://emploi.ci'
            item['salary'] = ''

            # On envoie l'item au pipeline
            yield item

        # On cherche le lien vers la page suivante
        # pour scraper toutes les pages
        next_page = response.css('.pager-next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)