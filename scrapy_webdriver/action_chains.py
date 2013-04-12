from functools import partial

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class WaitingActionChains(ActionChains):
    """ActionChains that wait on conditions."""
    def wait(self, timeout, condition=None, name=None, args=None):
        """Add a waiting action to the stack."""
        if args is None:
            args = []
        if name:
            condition = getattr(ec, name)(*args)
        if condition is None:
            raise ValueError('You must provide a condition, either directly '
                             'or by specifying its name.')

        def do_wait(condition):
            return WebDriverWait(self._driver, timeout).until(condition)
        self._actions.append(partial(do_wait, condition))
        return self
