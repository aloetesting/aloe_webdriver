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

import logging
log = logging.getLogger(__name__)


@wait_for
def wait_for_elem(browser, sel):
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
        except WebDriverException as e:
            if e.msg.startswith('$ is not defined'):
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
def check_element_by_selector(step, selector):
    elems = find_elements_by_jquery(world.browser, selector)
    assert_true(elems)


@step(r'There should be an element matching \$\("(.*?)"\) '
      'within (\d+) seconds?$')
def wait_for_element_by_selector(step, selector, seconds):
    elems = wait_for_elem(world.browser, selector, timeout=int(seconds))
    assert_true(elems)


@step(r'There should be exactly (\d+) elements matching \$\("(.*?)"\)$')
def count_elements_exactly_by_selector(step, number, selector):
    elems = find_elements_by_jquery(world.browser, selector)
    assert_equal(len(elems), int(number))


@step(r'I fill in \$\("(.*?)"\) with "(.*?)"$')
def fill_in_by_selector(step, selector, value):
    elem = find_element_by_jquery(world.browser, selector)
    elem.clear()
    elem.send_keys(value)


@step(r'I submit \$\("(.*?)"\)')
def submit_by_selector(step, selector):
    elem = find_element_by_jquery(world.browser, selector)
    elem.submit()


@step(r'I check \$\("(.*?)"\)$')
def check_by_selector(step, selector):
    elem = find_element_by_jquery(world.browser, selector)
    if not elem.is_selected():
        elem.click()


@step(r'I click \$\("(.*?)"\)$')
def click_by_selector(step, selector):
    # No need for separate button press step with selector style.
    elem = find_element_by_jquery(world.browser, selector)
    elem.click()


@step(r'I follow the link \$\("(.*?)"\)$')
def click_by_selector(step, selector):
    elem = find_element_by_jquery(world.browser, selector)
    href = elem.get_attribute('href')
    world.browser.get(href)


@step(r'\$\("(.*?)"\) should be selected$')
def click_by_selector(step, selector):
    # No need for separate button press step with selector style.
    elem = find_element_by_jquery(world.browser, selector)
    assert_true(elem.is_selected())


@step(r'I select \$\("(.*?)"\)$')
def select_by_selector(step, selector):
    option = find_element_by_jquery(world.browser, selector)
    selectors = find_parents_by_jquery(world.browser, selector)
    assert_true(len(selectors) > 0)
    selector = selectors[0]
    selector.click()
    sleep(0.3)
    option.click()
    assert_true(option.is_selected())


@step(r'There should not be an element matching \$\("(.*?)"\)$')
def check_element_by_selector(step, selector):
    elems = find_elements_by_jquery(world.browser, selector)
    assert_false(elems)

__all__ = [
    'wait_for_element_by_selector',
    'fill_in_by_selector',
    'check_by_selector',
    'click_by_selector',
    'check_element_by_selector',
]
