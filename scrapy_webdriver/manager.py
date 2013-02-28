from collections import deque
from threading import Lock

from scrapy.signals import engine_stopped
from selenium import webdriver
from scrapy_webdriver.http import WebdriverRequest, WebdriverInPageRequest


class WebdriverManager(object):
    """Manages the life cycle of a webdriver instance."""
    def __init__(self, crawler):
        self.crawler = crawler
        self._lock = Lock()
        self._wait_queue = deque()
        self._wait_inpage_queue = deque()
        self._browser = crawler.settings.get('WEBDRIVER_BROWSER', None)
        self._webdriver = None
        if isinstance(self._browser, basestring):
            self._browser = getattr(webdriver, self._browser)
        elif self._browser is not None:
            self._webdriver = self._browser

    @property
    def webdriver(self):
        """Return the webdriver instance, instantiate it if necessary."""
        if self._webdriver is None:
            self._webdriver = self._browser()
            self.crawler.signals.connect(self._cleanup, signal=engine_stopped)
        return self._webdriver

    def acquire(self, request):
        """Acquire lock for the request, or enqueue request upon failure."""
        assert isinstance(request, WebdriverRequest), \
            'Only a WebdriverRequest can use the webdriver instance.'
        if self._lock.acquire(False):
            request.manager = self
            return request
        else:
            if isinstance(request, WebdriverInPageRequest):
                queue = self._wait_inpage_queue
            else:
                queue = self._wait_queue
            queue.append(request)

    def acquire_next(self):
        """Return the next waiting request, if any.

        In-page requests are returned first.

        """
        try:
            request = self._wait_inpage_queue.popleft()
        except IndexError:
            try:
                request = self._wait_queue.popleft()
            except IndexError:
                return
        return self.acquire(request)

    def release(self, msg):
        """Release the the webdriver instance's lock."""
        self._lock.release()

    def _cleanup(self):
        """Clean up when the scrapy engine stops."""
        if self._webdriver is not None:
            self._webdriver.quit()
            assert len(self._wait_queue) + len(self._wait_inpage_queue) == 0, \
                'Webdriver queue not empty at engine stop.'
