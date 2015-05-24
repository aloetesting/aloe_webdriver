import os
import unittest

from aloe import world
from aloe.testing import FeatureTest

from lettuce_webdriver.tests import html_pages

PAGES = {}
for filename in os.listdir(html_pages):
    name = filename.split('.html')[0]
    PAGES[name] = 'file://%s' % os.path.join(html_pages, filename)


FEATURES = [
    """
    Feature: Wait and match CSS
        Scenario: Everything fires up
            When I go to "%(page)s"
            Then There should be an element matching $("textarea[name='bio']") within 1 second
    """ % {'page': PAGES['basic_page']},

    """
    Feature: CSS-based formstuff
        Scenario: Everything fires up
            When I go to "%(page)s"
            Then I fill in $("input[name='user']") with "A test string"
            And I check $("input[value='Bike']")
    """ % {'page': PAGES['basic_page']},
]

class TestUtil(FeatureTest):
    def test_features(self):
        import lettuce_webdriver.webdriver
        import lettuce_webdriver.css_selector_steps
        for feature_string in FEATURES:
            result = self.run_feature_string(feature_string)
            self.assertTrue(result.success)
