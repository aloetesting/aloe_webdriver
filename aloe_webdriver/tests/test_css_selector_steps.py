"""Test CSS selector steps."""

from aloe.testing import FeatureTest

from aloe_webdriver.tests.base import feature


class TestCSS(FeatureTest):
    """Test CSS steps."""

    @feature()
    def test_css_match(self):
        # pylint:disable=line-too-long
        """
        When I visit test page "basic_page"
        Then There should be an element matching $("textarea[name='bio']")
        """
        # pylint:enable=line-too-long

    @feature()
    def test_forms(self):
        """
        When I visit test page "basic_page"
        Then I fill in $("input[name='user']") with "A test string"
        And I check $("input[value='Bike']")
        """
