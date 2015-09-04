"""
Django-specific extensions for use with aloe_django_.

.. _aloe_django: https://github.com/koterpillar/aloe_django
"""

try:
    from urllib.parse import urljoin  # pylint:disable=no-name-in-module
except ImportError:
    from urlparse import urljoin  # pylint:disable=import-error

from aloe import step

# make sure the steps are loaded
import aloe_webdriver.webdriver  # pylint:disable=unused-import


@step(r'I visit site page "([^"]*)"')
def visit_page(self, page):
    """
    Visit the specific page of the site, e.g.

    .. code-block:: gherkin

        When I visit site page "/users"
    """

    testclass = self.testclass
    base_url = testclass.live_server_url.__get__(testclass)
    url = urljoin(base_url, page)
    self.given('I visit "%s"' % url)
