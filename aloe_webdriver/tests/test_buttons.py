"""
Test a variety of different buttons.
"""

from aloe.testing import FeatureTest

from aloe_webdriver.tests.base import feature

# pylint:disable=line-too-long


class TestSteps(FeatureTest):
    """Test steps."""

    @feature()
    def test_press_of_submit_button_by_name(self):
        """
        Given I visit test page "button_page"
        When I press "submit_button"
        Then I should see "You pressed the submit button"
        """

    @feature()
    def test_press_of_submit_button_by_value(self):
        """
        Given I visit test page "button_page"
        When I press "Submit button"
        Then I should see "You pressed the submit button"
        """

    @feature()
    def test_press_of_reset_button_by_name(self):
        """
        Given I visit test page "button_page"
        When I press "reset_button"
        Then I should see "You pressed the reset button"
        """

    @feature()
    def test_press_of_reset_button_by_value(self):
        """
        Given I visit test page "button_page"
        When I press "Reset button"
        Then I should see "You pressed the reset button"
        """

    @feature()
    def test_press_of_input_button_by_name(self):
        """
        Given I visit test page "button_page"
        When I press "input_button"
        Then I should see "You pressed the input button"
        """

    @feature()
    def test_press_of_input_button_by_value(self):
        """
        Given I visit test page "button_page"
        When I press "Input button"
        Then I should see "You pressed the input button"
        """

    @feature()
    def test_press_of_image_button_by_name(self):
        """
        Given I visit test page "button_page"
        When I press "image_button"
        Then I should see "You pressed the image button"
        """

    @feature()
    def test_press_of_button_element_by_name(self):
        """
        Given I visit test page "button_page"
        When I press "button_element"
        Then I should see "You pressed the button element"
        """

    @feature()
    def test_press_of_button_element_by_value(self):
        """
        Given I visit test page "button_page"
        When I press "Button element"
        Then I should see "You pressed the button element"
        """

    @feature()
    def test_press_of_anchor_button_by_name(self):
        """
        Given I visit test page "button_page"
        When I press "anchor_button"
        Then I should see "You pressed the anchor button"
        """

    @feature()
    def test_press_of_anchor_button_by_value(self):
        """
        Given I visit test page "button_page"
        When I press "Anchor button"
        Then I should see "You pressed the anchor button"
        """

    @feature()
    def test_press_of_div_button_by_name(self):
        """
        Given I visit test page "button_page"
        When I press "div_button"
        Then I should see "You pressed the div button"
        """

    @feature()
    def test_press_of_div_button_by_value(self):
        """
        Given I visit test page "button_page"
        When I press "Div button"
        Then I should see "You pressed the div button"
        """

    @feature()
    def test_press_of_span_button_by_name(self):
        """
        Given I visit test page "button_page"
        When I press "span_button"
        Then I should see "You pressed the span button"
        """

    @feature()
    def test_press_of_span_button_by_value(self):
        """
        Given I visit test page "button_page"
        When I press "Span button"
        Then I should see "You pressed the span button"
        """

    @feature()
    def test_press_of_paragraph_button_by_name(self):
        """
        Given I visit test page "button_page"
        When I press "paragraph_button"
        Then I should see "You pressed the paragraph button"
        """

    @feature()
    def test_press_of_paragraph_button_by_value(self):
        """
        Given I visit test page "button_page"
        When I press "Paragraph button"
        Then I should see "You pressed the paragraph button"
        """
