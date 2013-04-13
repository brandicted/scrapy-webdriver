from functools import partial
from time import sleep

from mock import call, Mock
from scrapy.crawler import Crawler
from scrapy.http import Request
from scrapy import log, signals
from scrapy.settings import Settings
from scrapy.spider import BaseSpider
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import reactor

from scrapy_webdriver.http import WebdriverRequest

BASE_SETTINGS = dict(
    DOWNLOAD_HANDLERS={
        'http': 'scrapy_webdriver.download.WebdriverDownloadHandler',
        'https': 'scrapy_webdriver.download.WebdriverDownloadHandler',
    },
    SPIDER_MIDDLEWARES={
        'scrapy_webdriver.middlewares.WebdriverSpiderMiddleware': 543,
    })


class TestRequestQueue:
    @classmethod
    def setup_class(cls):
        cls._settings = BASE_SETTINGS

    def settings(self, **options):
        settings = self._settings.copy()
        settings.update(**options)
        return settings

    def _stop_reactor(self):
        reactor.stop()

    def _wait(self, url, *args, **kwargs):
        sleep(0.1)

    def test_priorization(self):
        webdriver = Mock()
        settings = self.settings(WEBDRIVER_BROWSER=webdriver)
        webdriver.get.side_effect = self._wait
        webdriver.page_source = u''

        dispatcher.connect(self._stop_reactor, signal=signals.spider_closed)

        crawler = Crawler(Settings(values=settings))
        crawler.configure()
        spider = self.Spider(name='test', domain='testdomain')
        crawler.crawl(spider)
        crawler.start()
        log.start(loglevel='ERROR')
        reactor.run()

        assert webdriver.get.mock_calls == [
            call('http://testdomain/path?wr=0'),
            call('http://testdomain/path?wr=0&wa=0'),
            call('http://testdomain/path?wr=0&wa=1'),
            call('http://testdomain/path?wr=1'),
            call('http://testdomain/path?wr=1&wa=0'),
            call('http://testdomain/path?wr=1&wa=1'),
            call('http://testdomain/path?wr=0&wa=0&wr=0'),
            call('http://testdomain/path?wr=0&wa=1&wr=0'),
            call('http://testdomain/path?wr=1&wa=0&wr=0'),
            call('http://testdomain/path?wr=1&wa=1&wr=0')]

    class Spider(BaseSpider):
        def start_requests(self):
            for i in xrange(2):
                yield WebdriverRequest('http://testdomain/path?wr=%d' % i)
                yield Request('http://testdomain/path?r=%d' % i)

        def parse(self, response):
            def get(url):
                response.webdriver.get(url)

            for i in xrange(2):
                fake_url = '%s&wa=%d' % (response.url, i)
                request = response.action_request(url=fake_url,
                                                  callback=self.parse_action)
                # Leave a trace in the webdriver instance mock so we can look
                # at the request processing order.
                request.actions = Mock()
                request.actions.perform.side_effect = partial(get, fake_url)
                yield request

        def parse_action(self, response):
            yield WebdriverRequest('%s&wr=%d' % (response.url, 0),
                                   callback=self.parse_nothing)

        def parse_nothing(self, response):
            pass
