"""Test CSS selector steps."""

from aloe.testing import FeatureTest

from aloe_webdriver.tests.base import feature


class TestCSS(FeatureTest):
    """Test CSS steps."""

    @feature()
    def test_css_match(self):
        """
        When I visit test page "basic_page"
        Then there should be an element matching $("textarea[name='bio']")
        """

    @feature(fails=True)
    def test_css_match_failure(self):
        """
        When I visit test page "basic_page"
        Then there should be an element matching $("textarea[name='fail']")
        """

    @feature()
    def test_css_no_match(self):
        """
        When I visit test page "basic_page"
        Then there should not be an element matching $("textarea[name='fail']")
        """

    @feature(fails=True)
    def test_css_no_match_failure(self):
        """
        When I visit test page "basic_page"
        Then there should not be an element matching $("textarea[name='bio']")
        """

    @feature()
    def test_css_count(self):
        """
        When I visit test page "basic_page"
        Then there should be exactly 2 elements matching $("select")
        """

    @feature(fails=True)
    def test_css_count_failure(self):
        """
        When I visit test page "basic_page"
        Then there should be exactly 4 elements matching $("select")
        """

    @feature()
    def test_css_click(self):
        """
        When I visit test page "basic_page"
        And I click $("input[value='Reveal']")
        Then I should see "You pressed an input button"
        """

    @feature()
    def test_forms(self):
        """
        When I visit test page "basic_page"
        Then I fill in $("input[name='user']") with "A test string"
        And I check $("input[value='Bike']")
        And I select $("option[value='green']")
        And I select $("option[value='green']")
        Then $("option[value='green']") should be selected
        And I submit $("form")
        """

    @feature(fails=True)
    def test_select_failure(self):
        """
        When I visit test page "basic_page"
        And I select $("option[value='magenta']")
        """

    @feature(fails=True)
    def test_selected_failure(self):
        """
        When I visit test page "basic_page"
        Then $("option[value='black']") should be selected
        """

    @feature()
    def test_link(self):
        """
        Given I visit test page "link_page"
        And I see "Page o link"
        When I follow the link $("a[href='link_dest.html']")
        Then I should be at "http://SERVER_HOST:7755/link_dest.html"
        """

    @feature()
    def test_delayed_selector(self):
        (
            '''When I visit test page "basic_page"'''
            "\n"
            """And I click $("input[value='Start timer']")\n"""
            """Then there should be an element matching """
            """$("p[id='changed_id']") within 15 seconds"""
        )

    @feature(fails=True)
    def test_delayed_selector_failure(self):
        (
            '''When I visit test page "basic_page"'''
            "\n"
            """And I click $("input[value='Start timer']")\n"""
            """And there should be an element matching """
            """$("p[id='changed_id']") within 1 second"""
        )
