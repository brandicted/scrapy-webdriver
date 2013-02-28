scrapy-webdriver
================

Scrape using Selenium webdriver.

Installation
=============

For now, nothing's on pypi, but this should work:

    pip install https://github.com/sosign/scrapy-webdriver/archive/master.zip

Configuration
=============

Add something like this in your scrapy project settings:

    DOWNLOAD_HANDLERS = {
        'http': 'scrapy_webdriver.download.WebdriverDownloadHandler',
        'https': 'scrapy_webdriver.download.WebdriverDownloadHandler',
    }

    SPIDER_MIDDLEWARES = {
        'scrapy_webdriver.middlewares.WebdriverSpiderMiddleware': 543,
    }

    WEBDRIVER_BROWSER = 'PhantomJS'  # Or any other from selenium.webdriver

Usage
=====

In order to have webdriver handle your downloads, use the provided
class `scrapy_webdriver.http.WebdriverRequest` in place of the stock scrapy
`Request`.

Hacking
=======

Pull requests much welcome. Just make sure the tests still pass, and add to
them as necessary:

    python setup.py test
