"""
Base functions for tests.
"""

import os
import socketserver
import threading
import unittest
from contextlib import contextmanager
from functools import wraps
from http.server import SimpleHTTPRequestHandler
from time import sleep

from selenium import webdriver

from aloe.testing import in_directory


def feature(fails=False):
    """
    Decorate a test method to test the feature contained in its docstring.

    For example:
        @feature(failed=False)
        def test_some_feature(self):
            '''
            When I ...
            Then I ...
            '''

    The method code is ignored.
    """

    def outer(func):
        """
        A decorator to run the function as the feature contained in docstring.
        """

        @wraps(func)
        @in_directory(os.path.dirname(__file__))
        def inner(self):
            """Run the scenario from docstring."""

            scenario = func.__doc__

            # Make it possible to reference SERVER_HOST in URLs inside
            # scenarios
            scenario = scenario.replace(
                'SERVER_HOST',
                os.environ.get('SERVER_HOST', '0.0.0.0')
            )

            feature_string = """
            Feature: {name}
            Scenario: {name}
            {scenario_string}
            """.format(name=func.__name__, scenario_string=scenario)

            result = self.run_feature_string(feature_string)

            if fails:
                self.assertFalse(result.success)
            else:
                self.assertTrue(result.success)

        return inner

    return outer


class TestRequestHandler(SimpleHTTPRequestHandler):
    """A handler serving the test pages."""

    def translate_path(self, path):
        """Serve the pages directory instead of the current directory."""

        pages_dir = os.path.relpath(
            os.path.join(os.path.dirname(__file__), 'html_pages'))

        return SimpleHTTPRequestHandler.translate_path(
            self, '/' + pages_dir + path)

    def do_GET(self):
        """
        Artificially slow down the response to make sure there are no race
        conditions.
        """

        sleep(0.5)

        return SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, *args, **kwargs):  # pylint:disable=arguments-differ
        """Turn off logging."""
        pass


class TestServer(socketserver.TCPServer):
    """Server for the test pages."""

    allow_reuse_address = True

    def get_request(self):
        """Set a timeout on the request socket."""

        request, addr = socketserver.TCPServer.get_request(self)
        request.settimeout(2)  # pylint:disable=no-member
        return request, addr


@contextmanager
def test_server():
    """A context manager starting a server for the test pages."""

    port = 7755

    server = TestServer(('', port), TestRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    # When running the browser in Docker, pass the host address
    # to allow the container to access the server on the host
    if 'SERVER_HOST' in os.environ:
        address = (os.environ['SERVER_HOST'], port)
    else:
        address = server.server_address

    yield server, address

    server.shutdown()
    server_thread.join()
    server.server_close()


def browser_type():
    """Browser type selected for the tests."""

    return os.environ.get('BROWSER_TYPE', 'firefox')


def skip_if_browser(browsers, message):
    """Decorator to skip a test with a particular browser type."""

    if not isinstance(browsers, (list, tuple)):
        browsers = [browsers]

    if browser_type() in browsers:
        return unittest.skip(message)
    return lambda func: func


def create_browser():
    """Create a Selenium browser for tests."""

    if 'SELENIUM_ADDRESS' in os.environ:
        address = 'http://{}/wd/hub'.format(os.environ['SELENIUM_ADDRESS'])

        capabilities = {
            'chrome': webdriver.DesiredCapabilities.CHROME,
            'firefox': webdriver.DesiredCapabilities.FIREFOX,
            'phantomjs': webdriver.DesiredCapabilities.PHANTOMJS,
        }
        try:
            browser = capabilities[browser_type()]
        except KeyError:
            raise ValueError("Invalid BROWSER_TYPE.")

        return webdriver.Remote(
            address,
            desired_capabilities=browser,
        )

    browsers = {
        'chrome': webdriver.Chrome,
        'firefox': webdriver.Firefox,
        'phantomjs': webdriver.PhantomJS,
    }
    driver = browsers[browser_type()]

    # Explicitly specify the browser locale for the date input tests to work
    # regardless of the user's settings
    old_lc_all = os.environ.get('LC_ALL', '')
    try:
        os.environ['LC_ALL'] = 'en_US'
        return driver()
    finally:
        os.environ['LC_ALL'] = old_lc_all
