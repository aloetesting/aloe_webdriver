"""
Steps for selecting elements using CSS selectors.

Like with steps based on HTML id, these steps should be used cautiously to
avoid creating tests that do not describe the behaviours of your application.
See :ref:`good-bdd`.

.. note::

    Be aware these steps require jQuery_. If jQuery_ is not present it will be
    added (v1.10).

.. _jQuery: https://jquery.com/
"""

from functools import wraps
from time import sleep

from aloe import step
from aloe import world

from aloe_webdriver.util import (
    wait_for,
)

from nose.tools import (
    assert_equal,
    assert_false,
    assert_true,
)

from selenium.common.exceptions import WebDriverException

# pylint:disable=missing-docstring

# Pylint cannot infer the attributes on world
# pylint:disable=no-member


@wait_for
def wait_for_elem_selector(browser, sel):
    """Wait until the element specified by jQuery selector appears."""
    return find_elements_by_jquery(browser, sel)


def load_script(browser, url):
    """Ensure that JavaScript at a given URL is available to the browser."""
    if browser.current_url.startswith('file:'):
        url = 'https:' + url
    browser.execute_script("""
    var script_tag = document.createElement("script");
    script_tag.setAttribute("type", "text/javascript");
    script_tag.setAttribute("src", arguments[0]);
    document.getElementsByTagName("head")[0].appendChild(script_tag);
    """, url)

    sleep(1)


JQUERY = '//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js'


def load_jquery(func):
    """
    A decorator to ensure a function is run with jQuery available.

    If an exception from a function indicates jQuery is missing, it is loaded
    and the function re-executed.

    The browser to load jQuery into must be the first argument of the function.
    """

    @wraps(func)
    def wrapped(browser, *args, **kwargs):
        """Run the function, loading jQuery if needed."""

        try:
            return func(browser, *args, **kwargs)
        except WebDriverException as ex:
            if ex.msg.startswith('$ is not defined'):
                load_script(browser, JQUERY)
                return func(browser, *args, **kwargs)
            else:
                raise

    return wrapped


@load_jquery
def find_elements_by_jquery(browser, selector):
    """Find HTML elements using jQuery-style selectors.

    Ensures that jQuery is available to the browser."""

    return browser.execute_script(
        """return ($ || jQuery)(arguments[0]).get();""", selector)


def find_element_by_jquery(browser, selector):
    """Find a single HTML element using jQuery-style selectors."""
    elements = find_elements_by_jquery(browser, selector)
    assert_true(len(elements) > 0)
    return elements[0]


@load_jquery
def find_parents_by_jquery(browser, selector):
    """Find HTML elements' parents using jQuery-style selectors.

    Ensures that jQuery is available to the browser."""

    return browser.execute_script(
        """return ($ || jQuery)(arguments[0]).parent().get();""", selector)


@step(r'There should be an element matching \$\("(.*?)"\)$')
def check_element_by_selector(self, selector):
    """Assert an element exists matching the given selector."""
    elems = find_elements_by_jquery(world.browser, selector)
    assert_true(elems)


@step(r'There should not be an element matching \$\("(.*?)"\)$')
def check_no_element_by_selector(self, selector):
    """Assert an element does not exist matching the given selector."""
    elems = find_elements_by_jquery(world.browser, selector)
    assert_false(elems)


@step(r'There should be an element matching \$\("(.*?)"\) '
      r'within (\d+) seconds?$')
def wait_for_element_by_selector(self, selector, seconds):
    """
    Assert an element exists matching the given selector within the given time
    period.
    """
    # pylint:disable=unexpected-keyword-arg
    # wait_for decorator parses the argument
    elems = wait_for_elem_selector(
        world.browser, selector, timeout=int(seconds))
    assert_true(elems)


@step(r'There should be exactly (\d+) elements matching \$\("(.*?)"\)$')
def count_elements_exactly_by_selector(self, number, selector):
    """
    Assert n elements exist matching the given selector.
    """
    elems = find_elements_by_jquery(world.browser, selector)
    assert_equal(len(elems), int(number))


@step(r'I fill in \$\("(.*?)"\) with "(.*?)"$')
def fill_in_by_selector(self, selector, value):
    """Fill in the form element matching the CSS selector."""
    elem = find_element_by_jquery(world.browser, selector)
    elem.clear()
    elem.send_keys(value)


@step(r'I submit \$\("(.*?)"\)')
def submit_by_selector(self, selector):
    """Submit the form matching the CSS selector."""
    elem = find_element_by_jquery(world.browser, selector)
    elem.submit()


@step(r'I check \$\("(.*?)"\)$')
def check_by_selector(self, selector):
    """Check the checkbox matching the CSS selector."""
    elem = find_element_by_jquery(world.browser, selector)
    if not elem.is_selected():
        elem.click()


@step(r'I click \$\("(.*?)"\)$')
def click_by_selector(self, selector):
    """Click the element matching the CSS selector."""
    # No need for separate button press step with selector style.
    elem = find_element_by_jquery(world.browser, selector)
    elem.click()


@step(r'I follow the link \$\("(.*?)"\)$')
def follow_link_by_selector(self, selector):
    """
    Navigate to the href of the element matching the CSS selector.

    N.B. this does not click the link, but changes the browser's URL.
    """
    elem = find_element_by_jquery(world.browser, selector)
    href = elem.get_attribute('href')
    world.browser.get(href)


@step(r'\$\("(.*?)"\) should be selected$')
def is_selected_by_selector(self, selector):
    """Assert the option matching the CSS selector is selected."""
    # No need for separate button press step with selector style.
    elem = find_element_by_jquery(world.browser, selector)
    assert_true(elem.is_selected())


@step(r'I select \$\("(.*?)"\)$')
def select_by_selector(self, selector):
    """Select the option matching the CSS selector."""
    option = find_element_by_jquery(world.browser, selector)
    selectors = find_parents_by_jquery(world.browser, selector)
    assert_true(len(selectors) > 0)
    selector = selectors[0]
    selector.click()
    sleep(0.3)
    option.click()
    assert_true(option.is_selected())
