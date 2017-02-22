"""
Steps for testing.
"""

import os
from contextlib import contextmanager

try:
    reload
except NameError:
    # pylint:disable=no-name-in-module,redefined-builtin
    from importlib import reload
    # pylint:enable=no-name-in-module,redefined-builtin

from aloe import around, before, step, world

import aloe_webdriver
import aloe_webdriver.css

from aloe_webdriver.tests.base import create_browser, test_server

# This module is reloaded during testing in order to re-register the steps and
# callbacks. Make sure the modules where the steps are defined are, too.
reload(aloe_webdriver)
reload(aloe_webdriver.css)

if os.environ.get('TAKE_SCREENSHOTS'):
    # Only register the screenshot steps if asked to
    import aloe_webdriver.screenshot_failed
    reload(aloe_webdriver.screenshot_failed)

    SCREENSHOTS_DIR = os.environ.get('SCREENSHOTS_DIR')
    if SCREENSHOTS_DIR:
        aloe_webdriver.screenshot_failed.DIRECTORY = SCREENSHOTS_DIR


@around.all
@contextmanager
def with_browser():
    """Start a browser for the tests."""
    world.browser = create_browser()

    yield

    world.browser.quit()
    delattr(world, 'browser')


@around.all
@contextmanager
def with_test_server():
    """Start a server for the test pages."""

    with test_server() as (server, address):
        world.server = server
        world.base_address = address
        yield


@before.each_feature
def reset_page(feature):
    """Reset the browser before each feature."""
    world.browser.get('about:blank')


@step(r'I visit test page "([^"]+)"')
def visit_test_page(self, page):
    """Open a test page in the browser."""
    self.when('I visit "http://{address[0]}:{address[1]}/{page}.html"'.format(
        address=world.base_address,
        page=page,
    ))
