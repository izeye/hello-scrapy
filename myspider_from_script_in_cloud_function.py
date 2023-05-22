from multiprocessing import Queue, Process, freeze_support

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


def script(queue):
    try:
        process = CrawlerProcess(settings={
            "FEEDS": {
                "items.json": {"format": "json"}
            }
        })
        process.crawl(MySpider)
        process.start()
        queue.put(None)
    except Exception as e:
        queue.put(e)


def crawl():
    queue = Queue()

    main_process = Process(target=script, args=(queue,))
    main_process.start()
    main_process.join()

    result = queue.get()
    if result is not None:
        raise result


if __name__ == '__main__':
    freeze_support()

    crawl()
    crawl()
