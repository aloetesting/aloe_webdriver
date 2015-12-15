"""
Django-specific extensions for use with aloe_django_.

.. _aloe_django: https://github.com/koterpillar/aloe_django
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# pylint:disable=redefined-builtin,unused-wildcard-import,wildcard-import
from builtins import *
# pylint:enable=redefined-builtin,unused-wildcard-import,wildcard-import

try:
    from urllib.parse import urljoin  # pylint:disable=import-error
except ImportError:
    from urlparse import urljoin  # pylint:disable=import-error

from aloe import step
from aloe_django import django_url

# make sure the steps are loaded
import aloe_webdriver  # pylint:disable=unused-import


@step(r'I visit site page "([^"]*)"')
def visit_page(self, page):
    """
    Visit the specific page of the site, e.g.

    .. code-block:: gherkin

        When I visit site page "/users"
    """

    url = urljoin(django_url(self), page)
    self.given('I visit "%s"' % url)
