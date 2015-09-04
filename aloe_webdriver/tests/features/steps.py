"""
Steps for testing.
"""

from contextlib import contextmanager
try:
    reload
except NameError:
    # pylint:disable=no-name-in-module,redefined-builtin
    from importlib import reload
    # pylint:enable=no-name-in-module,redefined-builtin

from selenium import webdriver

from aloe import around, before, world

import aloe_webdriver
import aloe_webdriver.css

# This module is reloaded during testing in order to re-register the steps and
# callbacks. Make sure the modules where the steps are defined are, too.
reload(aloe_webdriver)
reload(aloe_webdriver.css)


@around.all
@contextmanager
def with_browser():
    """Start a browser for the tests."""
    world.browser = webdriver.Firefox()
    world.browser.get('')
    yield
    world.browser.quit()
    delattr(world, 'browser')


@before.each_feature
def reset_page(feature):
    """Reset the browser before each feature."""
    world.browser.get('')
