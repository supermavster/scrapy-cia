import json
import scrapy

# curl -u dd7c837f14c947c7a39ce7baae339bcd: https://app.scrapinghub.com/api/run.json -d project=465578 -d spider=cia       

class SpiderCia(scrapy.Spider):
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/library/readingroom/historical-collections'
    ]
    custom_settings = {
        'FEED_URI': './dist/response.json',
        'FEED_FORMAT': 'json',
        'CURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['ingeniero.miguelvargas@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'PepitoPerez',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    # Runner
    def parse(self, response):
        all_links = self.get_all_links(response)
        for link in all_links:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        url = kwargs['url']
        title = self.get_item_title(response)
        description = self.get_item_description(response)
        yield {
            'url': url,
            'title': title,
            'description': description
        }

    # Scraping Data
    def get_all_links(self, response):
        return response.xpath('//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').getall()

    def get_item_title(self, response):
        return response.xpath('//h1[@class="documentFirstHeading"]/text()').get()

    def get_item_description(self, response):
        return response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').get()