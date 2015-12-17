"""
Test Webdriver steps.
"""

from aloe.testing import FeatureTest

from aloe_webdriver.tests.base import feature, PAGES

# pylint:disable=line-too-long


class TestUtil(FeatureTest):
    """Test steps."""

    @feature()
    def test_I_should_see(self):
        """
Feature: I should see, I should not see
    Scenario: Everything fires up
        When I visit "{page}"
        Then I should see "Hello there!"
        And I should see 'Welcome "User"'
        And I should see a link to "Google" with the url "http://google.com/"
        And I should see a link with the url "http://google.com/"
        And I should not see "Bogeyman"
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_I_see_a_link(self):
        """
Feature: I should see a link
    Scenario: Everything fires up
        When I go to "{page}"
        Then  I should see a link to "Google" with the url "http://google.com/"
        And I see "Hello there!"
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_see_a_link_containing(self):
        """
Feature: I should see a link containing
    Scenario: Everything fires up
        When I go to "{page}"
        Then The browser's URL should contain "file://"
        And I should see a link that contains the text "Goo" and the url "http://google.com/"
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_basic_page_linking(self):
        """
Feature: Basic page linking
    Scenario: Follow links
        Given I go to "{link_page}"
        And I see "Page o link"
        When I click "Next Page"
        Then I should be at "{link_dest_page}"
        And The browser's URL should be "{link_dest_page}"
        And The browser's URL should not contain "http://"
        """

        return {
            'link_page': PAGES['link_page'],
            'link_dest_page': PAGES['link_dest']
        }

    @feature()
    def test_I_see_a_form(self):
        """
Feature: I should see a form
    Scenario: Everything fires up
        When I go to "{page}"
        Then I should see a form that goes to "basic_page.html"
        And the element with id of "somediv" contains "Hello"
        And the element with id of "somediv" does not contain "bye"
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_I_fill_in_a_form(self):
        """
Feature: I fill in a form
    Scenario: Everything fires up
        Given I go to "{page}"
        And I fill in "bio" with "everything awesome"
        And I fill in "Password: " with "neat"
        When I press "Submit!"
        Then The browser's URL should contain "bio=everything"
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_checkboxes_checked(self):
        """
Feature: Checkboxes checked
    Scenario: Everything fires up
        Given I go to "{page}"
        When I check "I have a bike"
        Then The "I have a bike" checkbox should be checked
        And The "I have a car" checkbox should not be checked
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_checkboxes_unchecked(self):
        """
Feature: Checkboxes unchecked
    Scenario: Everything fires up
        Given I go to "{page}"
        And I check "I have a bike"
        And The "I have a bike" checkbox should be checked
        When I uncheck "I have a bike"
        Then The "I have a bike" checkbox should not be checked
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_combo_boxes(self):
        """
Feature: Combo boxes
    Scenario: Everything fires up
        Given I go to "{page}"
        Then I should see option "Mercedes" in selector "car_choice"
        And I should see option "Volvo" in selector "car_choice"
        And I should not see option "Skoda" in selector "car_choice"
        When I select "Mercedes" from "car_choice"
        Then The "Mercedes" option from "car_choice" should be selected
        """

        return dict(page=PAGES['basic_page'])

    @feature(fails=True)
    def test_combo_boxes_fail(self):
        """
Feature: Combo boxes fail
    Scenario: Everything fires up
        Given I go to "{page}"
        Then I should not see option "Mercedes" in selector "car_choice"
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_multi_combo_boxes(self):
        '''
Feature: Multi-combo-boxes
    Scenario: Everything fires up
        Given I go to "{page}"
        When I select the following from "Favorite Colors:":
            """
            Blue
            Green
            """
        Then The following options from "Favorite Colors:" should be selected:
            """
            Blue
            Green
            """
        '''

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_radio_buttons(self):
        """
Feature: Radio buttons
    Scenario: Everything fires up
        When I go to "{page}"
        And I choose "Male"
        Then The "Male" option should be chosen
        And The "Female" option should not be chosen
        """

        return dict(page=PAGES['basic_page'])

    @feature(fails=True)
    def test_hidden_text(self):
        """
Feature: Hidden text
    Scenario: Everything fires up
        When I go to "{page}"
        Then I should see an element with id of "bio_field"
        And I should see an element with id of "somediv" within 2 seconds
        And I should not see an element with id of "hidden_text"
        And I should see "Weeeee" within 1 second
        """

        return dict(page=PAGES['basic_page'])

    @feature(fails=True)
    def test_hidden_text_2(self):
        """
Feature: Hidden text 2
    Scenario: Everything fires up
        When I go to "{page}"
        Then I should see "Hello there" within 1 second
        And I should see an element with id of "oops_field" within 1 second
        And I should not see an element with id of "hidden_text"
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_alert_accept(self):
        """
Feature: test alert accept
    Scenario: alerts
        When I go to "{page}"
        Then I should see an alert with text "This is an alerting alert"
        When I accept the alert
        Then I should not see an alert
        And I should see "true"
        """

        return dict(page=PAGES['alert_page'])

    @feature()
    def test_alert_dismiss(self):
        """
Feature: test alert accept
    Scenario: alerts
        When I go to "{page}"
        Then I should see an alert with text "This is an alerting alert"
        When I dismiss the alert
        Then I should not see an alert
        And I should see "false"
        """

        return dict(page=PAGES['alert_page'])

    @feature()
    def test_tooltips(self):
        """
Feature: test tooltips
    Scenario: tooltips
        When I go to "{page}"
        Then I should see an element with tooltip "A tooltip"
        And I should not see an element with tooltip "Does not exist"
        And I should not see an element with tooltip "Hidden"
        When I click the element with tooltip "A tooltip"
        Then the browser's URL should contain "#anchor"
        """

        return dict(page=PAGES['tooltips'])

    @feature()
    def test_labels(self):
        """
Feature: test labels
    Scenario: basic page
        When I go to "{page}"
        And I click on label "Favorite Colors:"
        Then element with id "fav_colors" should be focused
        And element with id "bio_field" should not be focused
        """

        return dict(page=PAGES['basic_page'])

    @feature(fails=True)
    def test_labels_fail(self):
        """
Feature: test labels fail
    Scenario: basic page
        When I go to "{page}"
        And I click on label "Favorite Colors:"
        Then element with id "fav_colors" should not be focused
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_input_values(self):
        """
Feature: assert value
    Scenario: basic page
        When I go to "{page}"
        And I fill in "username" with "Danni"
        Then input "username" has value "Danni"
        """

        return dict(page=PAGES['basic_page'])

    @feature(fails=True)
    def test_input_values_fail(self):
        """
Feature: assert value
    Scenario: basic page
        When I go to "{page}"
        And I fill in "username" with "Danni"
        Then input "username" has value "Ricky"
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_date_input(self):
        """
Feature: assert value
    Scenario: basic page
        When I go to "{page}"
        And I fill in "dob" with "1900/01/01"
        Then input "dob" has value "1900/01/01"
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_page_title(self):
        """
Feature: assert value
    Scenario: basic page
        When I go to "{page}"
        Then the page title should be "A Basic Page"
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_submit_only(self):
        """
Feature: submit only form
    Scenario: basic page
        When I go to "{page}"
        And I submit the only form
        Then the browser's URL should contain "bio="
        And the browser's URL should contain "user="
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_submit_action(self):
        """
Feature: submit only form
    Scenario: basic page
        When I go to "{page}"
        And I submit the form with action "basic_page.html"
        Then the browser's URL should contain "bio="
        And the browser's URL should contain "user="
        """

        return dict(page=PAGES['basic_page'])

    @feature()
    def test_submit_id(self):
        """
Feature: submit only form
    Scenario: basic page
        When I go to "{page}"
        And I submit the form with id "the-form"
        Then the browser's URL should contain "bio="
        And the browser's URL should contain "user="
        """

        return dict(page=PAGES['basic_page'])
