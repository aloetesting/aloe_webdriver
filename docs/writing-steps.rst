.. _good-bdd:

Writing good BDD steps
======================

The tools provided in `Aloe-Webdriver` form a reasonably thin wrapper
around Selenium_ and thus make it very easy to write `imperative` tests.
While the occasional imperative test is useful, it is frequently more useful
to abstract these into sub-steps of a more `declarative test`.

For example, take this example from the `BBC essay: Tips for writing better
feature files <http://www.bbc.co.uk/blogs/internet/entries/ff14236d-098a-3565-b678-ff4ba5776a5f>`_.

Here is a bad, imperative example:

.. code-block:: gherkin

    Given I am on the login page
    When I fill in "username" with "ABC"
    And I fill in "password" with "XYZ"
    And I checked the "Remember Me" checkbox
    And I click on the "Submit" button
    Then I should log into the system
    And I should see "Welcome"

Instead a better, declarative example would be:

.. code-block:: gherkin

    Given I have logged into the system
    Then I should see "Welcome"

Use :meth:`step.behave_as` to call the imperative steps from your own step
abstracts the mechanics of your website into something more descriptive. This
also makes it easier if you ever change the login process.

.. code-block:: python

    @step("I have logged into the system")
    def i_log_in():
        '''Log in to the site'''
        step.behave_as('Given I am on the login page')
        step.behave_as('When I fill in "username" with "ABC"')
        step.behave_as('And I fill in "password" with "XYZ"')
        step.behave_as('And I checked the "Remember Me" checkbox')
        step.behave_as('And I click on the "Submit" button')
        step.behave_as('Then I should log into the system')

.. _selenium: http://selenium-python.readthedocs.io/

Step Writing Utilities
----------------------

.. automodule:: aloe_webdriver.util
    :members:
    :exclude-members: field_xpath, option_in_select
