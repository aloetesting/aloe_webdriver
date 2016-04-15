"""
Steps for testing.
"""

import os
import socketserver
import threading
from contextlib import contextmanager
from http.server import SimpleHTTPRequestHandler
from time import sleep

try:
    reload
except NameError:
    # pylint:disable=no-name-in-module,redefined-builtin
    from importlib import reload
    # pylint:enable=no-name-in-module,redefined-builtin

from selenium import webdriver

from aloe import around, before, step, world

import aloe_webdriver
import aloe_webdriver.css

# This module is reloaded during testing in order to re-register the steps and
# callbacks. Make sure the modules where the steps are defined are, too.
reload(aloe_webdriver)
reload(aloe_webdriver.css)

if os.environ.get('TAKE_SCREENSHOTS'):
    # Only register the screenshot steps if asked to
    import aloe_webdriver.screenshot_failed
    reload(aloe_webdriver.screenshot_failed)


@around.all
@contextmanager
def with_browser():
    """Start a browser for the tests."""
    world.browser = webdriver.Firefox()

    yield

    world.browser.quit()
    delattr(world, 'browser')


class TestRequestHandler(SimpleHTTPRequestHandler):
    """A handler serving the test pages."""

    def translate_path(self, path):
        """Serve the pages directory instead of the current directory."""

        pages_dir = os.path.relpath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'html_pages'))

        return SimpleHTTPRequestHandler.translate_path(
            self, '/' + pages_dir + path)

    def do_GET(self):
        """
        Artificially slow down the response to make sure there are no race
        conditions.
        """

        sleep(0.5)

        return SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, *args, **kwargs):
        """Turn off logging."""
        pass


class TestServer(socketserver.TCPServer):
    """Server for the test pages."""

    allow_reuse_address = True


def test_server():
    """Start a server for the test pages."""

    return TestServer(('', 7755), TestRequestHandler)


@around.all
@contextmanager
def with_test_server():
    """Start a server for the test pages."""

    world.server = test_server()

    server_thread = threading.Thread(target=world.server.serve_forever)
    server_thread.start()

    yield

    world.server.shutdown()
    server_thread.join()
    world.server.server_close()


@before.each_feature
def reset_page(feature):
    """Reset the browser before each feature."""
    world.browser.get('')


@step(r'I visit test page "([^"]+)"')
def visit_test_page(self, page):
    """Open a test page in the browser."""
    self.when('I visit "http://{address[0]}:{address[1]}/{page}.html"'.format(
        address=world.server.server_address,
        page=page,
    ))
