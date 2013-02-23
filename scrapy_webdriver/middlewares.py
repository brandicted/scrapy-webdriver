from scrapy.exceptions import IgnoreRequest, NotConfigured

from .http import WebdriverInPageRequest, WebdriverRequest
from .manager import WebdriverManager


class WebdriverSpiderMiddleware(object):
    """This middleware coordinates concurrent webdriver access attempts."""
    def __init__(self, crawler):
        self.manager = WebdriverManager(crawler)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('WEBDRIVER_ENABLED'):
            raise NotConfigured
        return cls(crawler)

    def process_start_requests(self, start_requests, spider):
        """Return start requests with some reordered by the manager.

        The reordering occurs as a result of some requests waiting to gain
        access to the webdriver instance. Those waiting requests are queued up
        in the manager, from which we pop the next in line after we release the
        webdriver instance while processing spider output.

        """
        print 'process_start_requests'
        return self._process_requests(start_requests, start=True)

    def process_spider_output(self, response, result, spider):
        """Return spider result with some requests reordered by the manager.

        See ``process_start_requests`` for a description of the reordering.

        """
        print 'process_spider_output %s' % response.request.url
        if isinstance(response.request, WebdriverRequest):
            print 'entering with webdriver %s' % response.request.url
        else:
            print 'entering with regular request %r' % response.request
        for item_or_request in self._process_requests(result):
            yield item_or_request
        if isinstance(response.request, WebdriverRequest):
            print 'exiting with webdriver %s' % response.request.url
            self.manager.release(response.request.url)
            next_request = self.manager.acquire_next()
            if next_request is not WebdriverRequest.WAITING:
                print 'popped %s' % next_request.url
                yield next_request.replace(dont_filter=True)
            else:
                print 'queue empty'

    def _process_requests(self, items_or_requests, start=False):
        """Acquire the webdriver manager when it's available for requests."""
        error_msg = "WebdriverRequests from start_requests can't be in-page."
        for request in iter(items_or_requests):
            if isinstance(request, WebdriverRequest):
                if start and isinstance(request, WebdriverInPageRequest):
                    raise IgnoreRequest(error_msg)
                request = self.manager.acquire(request)
                if request is WebdriverRequest.WAITING:
                    continue  # Request has been enqueued, so drop it.
            if start:
                print 'yielding start request'
            yield request
