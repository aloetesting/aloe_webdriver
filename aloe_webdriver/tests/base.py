"""
Base functions for tests.
"""

import os
import socketserver
import threading
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

            feature_string = """
            Feature: {name}
            Scenario: {name}
            {scenario_string}
            """.format(name=func.__name__, scenario_string=func.__doc__)

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

    def log_message(self, *args, **kwargs):
        """Turn off logging."""
        pass


class TestServer(socketserver.TCPServer):
    """Server for the test pages."""

    allow_reuse_address = True


@contextmanager
def test_server():
    """A context manager starting a server for the test pages."""

    server = TestServer(('', 7755), TestRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    yield server

    server.shutdown()
    server_thread.join()
    server.server_close()


def create_browser():
    """Create a Selenium browser for tests."""

    return webdriver.Firefox()
