scrapy-webdriver
================

Scrape using Selenium webdriver.

Configuration
-------------

Add something like this in your scrapy project settings:

    DOWNLOAD_HANDLERS = {
        'http': 'scrapy_webdriver.download.WebdriverDownloadHandler',
        'https': 'scrapy_webdriver.download.WebdriverDownloadHandler',
    }

    SPIDER_MIDDLEWARES = {
        'scrapy_webdriver.middlewares.WebdriverSpiderMiddleware': 543,
    }

    WEBDRIVER_BROWSER = 'PhantomJS'

Usage
-----

In order to have webdriver handle your downloads, use the provided class
`scrapy_webdriver.http.WebdriverRequest` in place of the stock scrapy `Request`.

