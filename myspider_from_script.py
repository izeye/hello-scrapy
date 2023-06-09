import scrapy
from scrapy.crawler import CrawlerProcess


class MySpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://www.zyte.com/blog/']

    def parse(self, response):
        for title in response.css('.oxy-post-title'):
            yield {'title': title.css('::text').get()}

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)


def crawl():
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"}
        }
    })
    process.crawl(MySpider)
    process.start()


crawl()
crawl()
