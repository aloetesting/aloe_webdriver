Aloe steps for Web Testing with Selenium
========================================

A set of [Gherkin][gherkin] steps for use with [Aloe][aloe] to test Web
applications using Selenium.

Based on [lettuce_webdriver](lettuce_webdriver) which, in turn, is inspired by
[cucmber_watir](cucumber_watir).

Setting Up Aloe Webdriver
-------------------------

In your ``terrain.py`` file, add an include statement to register the
additional step definitions provided by Aloe Webdriver:

```python
import aloe_webdriver.webdriver
```

And a step to create the desired Selenium browser:

```python
from contextlib import contextmanager
from aloe import before, world
from selenium import webdriver

@around.all
@contextmanager
def with_browser():
    world.browser = webdriver.Firefox()
    yield
    world.browser.quit()
    delattr(world, 'browser')
```

Usage
-----

Aloe features are written in the standard Gherkin language, for example:

```gherkin
Scenario: Filling out the signup form
    Given I go to "http://foo.com/signup"
    When I fill in "Name" with "Foo Bar"
    And I fill in "Email" with "nospam@gmail.com"
    And I fill in "City" with "San Jose"
    And I fill in "State" with "CA"
    And I uncheck "Send me spam!"
    And I select "Male" from "Gender"
    And I press "Sign up"
    Then I should see "Thank you for signing up!"
```

Included Matchers
-----------------

The following Aloe steps are included in this package and can be used with
Given/When/Then/And as desired.

### URLs

```gherkin
    I visit "http://google.com/"
    I go to "http://google.com/"
```

### Links

```gherkin
    I click "Next page"
    I should see a link with the url "http://foobar.com/"
    I should see a link to "Google" with the url "http://google.com/"
    I should see a link that contains the text "Foobar" and the url "http://foobar.com/"
```

### General

```gherkin
    I should see "Page Content"
    I see "Page Content"
    I should see "Page Content" within 4 seconds
    I should not see "Foobar"
    I should be at "http://foobar.com/"
    I should see an element with id of "http://bar.com/"
    I should see an element with id of "http://bar.com/" within 2 seconds
    I should not see an element with id of "http://bar.com/"
    The element with id of "cs_PageModeContainer" contains "Read"
    The element with id of "cs_BigDiv" does not contain "Write"
```

### Browser

```gherkin
    The browser's URL should be "http://bar.com/"
    The browser's URL should contain "foo.com"
    The browser's URL should not contain "bar.com"
```

### Forms

```gherkin
    I should see a form that goes to "http://bar.com/submit.html"
    I press "Submit"
```

### Checkboxes

```gherkin
    I check "I have a car"
    I uncheck "I have a bus"
    The "I have a car" checkbox should be checked
    The "I have a bus" checkbox should not be checked
```

### Select

```gherkin
    I select "Volvo" from "Car Choices"
    I select the following from "Car Choices":
        """
        Volvo
        Saab
        """
    The "Volvo" option from "Car Choices" should be selected
    The following options from "Car Choices" should be selected:
        """
        Volvo
        Saab
        """
```

### Radio buttons

```gherkin
    I choose "Foobar"
    The "Foobar" option should be chosen
    The "Bar" option should not be chosen
```

### Text entry fields

```gherkin
    I fill in "Username" with "Smith"
```

[gherkin]: https://cucumber.io/
[aloe]: http://aloe.readthedocs.org/
[lettuce_webdriver]: https://github.com/bbangert/lettuce_webdriver
[cucumber_watir]: https://github.com/napcs/cucumber_watir
