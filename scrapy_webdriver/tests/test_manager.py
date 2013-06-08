from scrapy.crawler import Crawler
from scrapy.settings import Settings
from selenium import webdriver

from scrapy_webdriver.manager import WebdriverManager

BASE_SETTINGS = dict(
    DOWNLOAD_HANDLERS={
        'http': 'scrapy_webdriver.download.WebdriverDownloadHandler',
        'https': 'scrapy_webdriver.download.WebdriverDownloadHandler',
    },
    SPIDER_MIDDLEWARES={
        'scrapy_webdriver.middlewares.WebdriverSpiderMiddleware': 543,
    })


class TestManager:
    @classmethod
    def setup_class(cls):
        cls._settings = BASE_SETTINGS

    def settings(self, **options):
        settings = self._settings.copy()
        settings.update(**options)
        return settings

    def test_browser_config(self):
        class TestBrowser(object):
            pass

        settings = self.settings(WEBDRIVER_BROWSER='Firefox')
        crawler = Crawler(Settings(values=settings))
        crawler.configure()
        browser = WebdriverManager(crawler)
        assert issubclass(browser._browser, webdriver.Firefox)

        settings = self.settings(WEBDRIVER_BROWSER=TestBrowser)
        crawler = Crawler(Settings(values=settings))
        crawler.configure()
        browser = WebdriverManager(crawler)
        assert issubclass(browser._browser, TestBrowser)

        settings = self.settings(WEBDRIVER_BROWSER=TestBrowser())
        crawler = Crawler(Settings(values=settings))
        crawler.configure()
        browser = WebdriverManager(crawler)
        assert isinstance(browser._webdriver, TestBrowser)
