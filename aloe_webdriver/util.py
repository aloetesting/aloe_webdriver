"""Utility functions that combine steps to locate elements"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# pylint:disable=redefined-builtin
from builtins import str
# pylint:enable=redefined-builtin

import operator
from time import time, sleep

try:
    reduce
except NameError:
    from functools import reduce  # pylint:disable=redefined-builtin

from selenium.common.exceptions import NoSuchElementException

# pylint:disable=missing-docstring,redefined-outer-name,redefined-builtin
# pylint:disable=invalid-name


def string_literal(content):
    """Choose a string literal that can wrap our string"""

    if '"' in content and "'" in content:
        # there is no way to escape string literal characters in XPath
        raise ValueError("Cannot represent this string in XPath")
    elif '"' in content:  # if it contains " wrap it in '
        content = "'%s'" % content
    else:  # wrap it in "
        content = '"%s"' % content

    return content


class XPathSelector(object):
    """
    A set of elements on a page matching an XPath query.

    Delays evaluation to batch the queries together, allowing operations on
    selectors (e.g. union) to be performed first, and then issuing as few
    requests to the browser as possible.

    Also behaves as a single element by proxying all method calls, asserting
    that there is only one element selected.
    """

    def __init__(self, browser, xpath=None, elements=None):
        """
        Initialise the selector.

        One of 'xpath' and 'elements' must be passed. Passing 'xpath' creates a
        selector delaying evaluation until it's needed, passing 'elements'
        stores the elements immediately.
        """
        self.browser = browser

        if xpath is None and elements is None:
            raise ValueError("Must supply either xpath or elements.")

        if xpath is not None:
            self.xpath = xpath
        else:
            self._elements_cached = elements

    def _select(self):
        """
        Fetch the elements from the browser.
        """
        return self.browser.find_elements_by_xpath(self.xpath)

    def _elements(self):
        """
        The cached list of elements.
        """
        if not hasattr(self, '_elements_cached'):
            setattr(self, '_elements_cached', list(self._select()))
        return self._elements_cached

    def __add__(self, other):
        """
        Return a union of the two selectors.

        Where possible, avoid evaluating either selector to batch queries.
        """

        if not hasattr(self, '_elements_cached') \
                and isinstance(other, XPathSelector) \
                and not hasattr(other, '_elements_cached'):
            # Both summands are delayed, return a new delayed selector
            return XPathSelector(self.browser,
                                 xpath=self.xpath + '|' + other.xpath)
        else:
            # Have to evaluate everything now
            # other can be either an already evaluated XPathSelector, a list or
            # a single element
            try:
                other = list(other)
            except TypeError:
                other = [other]

            return XPathSelector(self.browser, elements=list(self) + other)

    # The class behaves as a container for the elements, fetching the list from
    # the browser on the first attempt to enumerate itself.

    def __len__(self):
        return len(self._elements())

    def __getitem__(self, key):
        return self._elements()[key]

    def __iter__(self):
        for el in self._elements():
            yield el

    def __nonzero__(self):
        return bool(self._elements())

    def __getattr__(self, attr):
        """
        Delegate all calls to the only element selected.
        """

        if attr == '_elements_cached':
            # Never going to be on the element
            raise AttributeError()

        assert len(self) == 1, \
            'Must be a single element, have {0}'.format(len(self))
        return getattr(self[0], attr)


def element_id_by_label(browser, label):
    """Return the id of a label's for attribute"""
    label = XPathSelector(browser,
                          str('//label[contains(., %s)]' %
                              string_literal(label)))
    if not label:
        return False
    return label.get_attribute('for')


def field_xpath(field, attribute):
    """
    Field helper functions to locate select, textarea, and the other
    types of input fields (text, checkbox, radio)
    """
    if field in ['select', 'textarea']:
        xpath = './/{field}[@{attr}=%s]'

    elif field == 'button':
        if attribute == 'value':
            xpath = './/{field}[contains(., %s)]'
        else:
            xpath = './/{field}[@{attr}=%s]'

    elif field == 'option':
        xpath = './/{field}[@{attr}=%s]'

    else:
        xpath = './/input[@{attr}=%s][@type="{field}"]'

    return xpath.format(field=field, attr=attribute)


def find_button(browser, value):
    return find_field_with_value(browser, 'submit', value) + \
        find_field_with_value(browser, 'reset', value) + \
        find_field_with_value(browser, 'button', value) + \
        find_field_with_value(browser, 'image', value)


def find_field_with_value(browser, field, value):
    return find_field_by_id(browser, field, value) + \
        find_field_by_name(browser, field, value) + \
        find_field_by_value(browser, field, value)


def find_option(browser, select_name, option_name):
    # First, locate the select
    select_box = find_field(browser, 'select', select_name)
    assert select_box

    # Now locate the option
    option_box = find_field(select_box, 'option', option_name)
    if not option_box:
        # Locate by contents
        option_box = select_box.find_element_by_xpath(str(
            './/option[contains(., "%s")]' % option_name))
    return option_box


def find_field(browser, field, value):
    """Locate an input field of a given value

    This first looks for the value as the id of the element, then
    the name of the element, then a label for the element.

    """
    return find_field_by_id(browser, field, value) + \
        find_field_by_name(browser, field, value) + \
        find_field_by_label(browser, field, value)


def find_any_field(browser, field_types, field_name):
    """
    Find a field of any of the specified types.
    """

    return reduce(
        operator.add,
        (find_field(browser, field_type, field_name)
         for field_type in field_types)
    )


def find_field_by_id(browser, field, id):
    return XPathSelector(browser,
                         field_xpath(field, 'id') % string_literal(id))


def find_field_by_name(browser, field, name):
    return XPathSelector(browser,
                         field_xpath(field, 'name') % string_literal(name))


def find_field_by_value(browser, field, name):
    xpath = field_xpath(field, 'value') % string_literal(name)
    elems = [elem for elem in XPathSelector(browser, str(xpath))
             if elem.is_displayed() and elem.is_enabled()]

    # sort by shortest first (most closely matching)
    if field == 'button':
        elems = sorted(elems, key=lambda elem: len(elem.text))
    else:
        elems = sorted(elems,
                       key=lambda elem: len(elem.get_attribute('value')))

    if elems:
        elems = [elems[0]]
    return elems


def find_field_by_label(browser, field, label):
    """Locate the control input that has a label pointing to it

    This will first locate the label element that has a label of the given
    name. It then pulls the id out of the 'for' attribute, and uses it to
    locate the element by its id.

    """

    return XPathSelector(browser,
                         field_xpath(field, 'id') %
                         '//label[contains(., {0})]/@for'.format(
                             string_literal(label)))


def option_in_select(browser, select_name, option):
    """
    Returns the Element specified by @option or None

    Looks at the real <select> not the select2 widget, since that doesn't
    create the DOM until we click on it.
    """

    select = find_field(browser, 'select', select_name)
    assert select

    try:
        return select.find_element_by_xpath(str(
            './/option[normalize-space(text())=%s]' % string_literal(option)))
    except NoSuchElementException:
        return None


def wait_for(func):
    """
    A decorator to invoke a function periodically until it returns a truthy
    value.
    """

    def wrapped(*args, **kwargs):
        timeout = kwargs.pop('timeout', 15)

        start = time()
        result = None

        while time() - start < timeout:
            result = func(*args, **kwargs)
            if result:
                break
            sleep(0.2)

        return result

    return wrapped
