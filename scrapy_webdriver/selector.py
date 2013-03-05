import re

from scrapy.selector import XPathSelector, XPathSelectorList

_UNSUPPORTED_XPATH_ENDING = re.compile(r'.*/((@)?([^/()]+)(\(\))?)$')


class WebdriverXPathSelector(XPathSelector):
    """Scrapy selector that works using XPath selectors in a remote browser.

    Based on some code from Marconi Moreto:
        https://github.com/marconi/ghost-selector

    """
    def __init__(self, response=None, webdriver=None, element=None,
                 *args, **kwargs):
        kwargs['response'] = response
        super(WebdriverXPathSelector, self).__init__(*args, **kwargs)
        self.response = response
        self.webdriver = webdriver or response.webdriver
        self.element = element

    def _make_result(self, result):
        if type(result) is not list:
            result = [result]
        return [self.__class__(webdriver=self.webdriver, element=e)
                for e in result]

    def select(self, xpath):
        """Return elements using webdriver `find_elements_by_xpath` method."""
        xpathev = self.element if self.element else self.webdriver
        ending = _UNSUPPORTED_XPATH_ENDING.match(xpath)
        if ending:
            match, atsign, name, parens = ending.groups()
            if atsign:
                xpath = xpath[:-len(name) - 2]
            elif parens and name == 'text':
                xpath = xpath[:-len(name) - 3]
        else:
            atsign = parens = None
        result = self._make_result(xpathev.find_elements_by_xpath(xpath))
        if atsign:
            result = (_NodeAttribute(r.element, name) for r in result)
        elif parens and result and name == 'text':
            result = (_TextNode(self.webdriver, r.element) for r in result)
        return XPathSelectorList(result)

    def select_script(self, script, *args):
        """Return elements using JavaScript snippet execution."""
        result = self.webdriver.execute_script(script, *args)
        return XPathSelectorList(self._make_result(result))

    def extract(self):
        """Extract text from selenium element."""
        return self.element.text if self.element else None


class _NodeAttribute(object):
    """Works around webdriver XPath inability to select attributes."""
    def __init__(self, element, attribute):
        self.element = element
        self.attribute = attribute

    def extract(self):
        return self.element.get_attribute(self.attribute)


class _TextNode(object):
    """Works around webdriver XPath inability to select text nodes."""
    JS_FIND_FIRST_TEXT_NODE = 'return arguments[0].firstChild.nodeValue'

    def __init__(self, webdriver, element):
        self.element = element
        self.webdriver = webdriver

    def extract(self):
        args = (self.JS_FIND_FIRST_TEXT_NODE, self.element)
        return self.webdriver.execute_script(*args)
