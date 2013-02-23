from scrapy.utils.decorator import inthread
from scrapy.utils.misc import load_object

from .http import WebdriverInPageRequest, WebdriverRequest, WebdriverResponse

SCRAPY_HANDLER = 'scrapy.core.downloader.handlers.http.HttpDownloadHandler'


class WebdriverDownloadHandler(object):
    """This download handler uses webdriver, deferred in a thread.

    Falls back to the stock scrapy download handler for non-webdriver requests.

    """
    def __init__(self, settings):
        self._enabled = settings.getbool('WEBDRIVER_ENABLED')
        self._scrapy_handler = load_object(SCRAPY_HANDLER)(settings)

    def download_request(self, request, spider):
        """Return the result of the right download method for the request."""
        print 'download_request %r' % request.url
        if self._enabled and isinstance(request, WebdriverRequest):
            if isinstance(request, WebdriverInPageRequest):
                download = self._do_inpage_request
            else:
                download = self._download_request
        else:
            download = self._scrapy_handler.download_request
        return download(request, spider)

    @inthread
    def _download_request(self, request, spider):
        """Download a request URL using webdriver."""
        print 'downloading %s' % request.url
        request.manager.webdriver.get(request.url)
        print 'got %s' % request.url
        return WebdriverResponse(request.url, request.manager.webdriver)

    @inthread
    def _do_inpage_request(self, request, spider):
        """Perform an action on a previously webdriver-loaded page."""
        print 'downloading in-page %s' % request.url
        request.manager.webdriver.get(request.url)
        print 'got in-page %s' % request.url
        return WebdriverResponse(request.url, request.manager.webdriver)
