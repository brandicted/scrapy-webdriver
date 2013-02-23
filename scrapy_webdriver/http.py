from scrapy.http import Request, TextResponse


class WebdriverRequest(Request):
    """A Request needed when using the webdriver download handler."""
    WAITING = None

    def __init__(self, url, manager=None, **kwargs):
        super(WebdriverRequest, self).__init__(url, **kwargs)
        self.manager = manager

    def replace(self, *args, **kwargs):
        kwargs.setdefault('manager', self.manager)
        return super(WebdriverRequest, self).replace(*args, **kwargs)


class WebdriverInPageRequest(WebdriverRequest):
    """A Request that handles in-page webdriver actions."""
    pass


class WebdriverResponse(TextResponse):
    """A Response that will feed the webdriver page into its body. Uhuhuh."""
    def __init__(self, url, webdriver, **kwargs):
        kwargs.setdefault('body', webdriver.page_source)
        kwargs.setdefault('encoding', 'utf-8')
        super(WebdriverResponse, self).__init__(url, **kwargs)
