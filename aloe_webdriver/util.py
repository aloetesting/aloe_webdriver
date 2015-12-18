"""
`Aloe-Webdriver` includes several utilities for writing Selenium_ tests.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# pylint:disable=redefined-builtin
from builtins import str
# pylint:enable=redefined-builtin

import operator
from copy import copy
from time import time, sleep

try:
    reduce
except NameError:
    from functools import reduce  # pylint:disable=redefined-builtin

from selenium.common.exceptions import NoSuchElementException

# pylint:disable=missing-docstring,redefined-outer-name,redefined-builtin
# pylint:disable=invalid-name

# Pylint cannot infer the attributes on world
# pylint:disable=no-member


def string_literal(content):
    """
    Choose a string literal that can wrap our string.

    If your string contains a ``\'`` the result will be wrapped in ``\"``.
    If your string contains a ``\"`` the result will be wrapped in ``\'``.

    Cannot currently handle strings which contain both ``\"`` and ``\'``.
    """

    if '"' in content and "'" in content:
        # there is no way to escape string literal characters in XPath
        raise ValueError("Cannot represent this string in XPath")
    elif '"' in content:  # if it contains " wrap it in '
        content = "'%s'" % content
    else:  # wrap it in "
        content = '"%s"' % content

    return content


class ElementSelector(object):
    """
    A set of elements on a page matching an XPath query.

    :param browser: ``world.browser``
    :param str xpath: XPath query
    :param list elements: list of :class:`selenium.WebElement` objects
    :param bool filter_displayed: whether to only return displayed elements
    :param bool filter_enabled: whether to only return enabled elements

    Delays evaluation to batch the queries together, allowing operations on
    selectors (e.g. union) to be performed first, and then issuing as few
    requests to the browser as possible.

    One of `xpath` or `elements` must be passed. Passing `xpath` creates a
    selector delaying evaluation until it's needed, passing `elements`
    stores the elements immediately.

    Can behave as an iterable of elements or a single element by proxying all
    method calls, asserting that there is only one element selected.

    Can be combined using the addition operator (``+``) to `OR` XPath queries
    together.
    """

    def __init__(self, browser, xpath=None, elements=None,  # pylint:disable=too-many-arguments
                 filter_displayed=False, filter_enabled=False):
        """
        Initialise the selector.

        One of `xpath` or `elements` must be passed. Passing `xpath` creates a
        selector delaying evaluation until it's needed, passing `elements`
        stores the elements immediately.
        """
        self.browser = browser

        if xpath is None and elements is None:
            raise ValueError("Must supply either xpath or elements.")

        if xpath is not None:
            self.xpath = xpath
        else:
            self._elements_cached = elements

        self.filter_displayed = filter_displayed
        self.filter_enabled = filter_enabled

    @property
    def evaluated(self):
        """Whether the selector has already been evaluated."""

        return hasattr(self, '_elements_cached')

    def filter(self, displayed=False, enabled=False):
        """
        Filter elements by visibility and enabled status.

        :param displayed: whether to filter out invisible elements
        :param enabled: whether to filter out disabled elements

        Returns: an :class:`ElementSelector`
        """

        if self.evaluated:
            # Filter elements one by one
            result = self

            if displayed:
                result = ElementSelector(
                    result.browser,
                    elements=[e for e in result if e.is_displayed()]
                )

            if enabled:
                result = ElementSelector(
                    result.browser,
                    elements=[e for e in result if e.is_enabled()]
                )

        else:
            result = copy(self)
            if displayed:
                result.displayed = True
            if enabled:
                result.enabled = True

        return result

    def _select(self):
        """Fetch the elements from the browser."""

        for element in self.browser.find_elements_by_xpath(self.xpath):
            if self.filter_displayed:
                if not element.is_displayed():
                    continue

            if self.filter_enabled:
                if not element.is_enabled():
                    continue

            yield element

    def _elements(self):
        """
        The cached list of elements.
        """
        if not self.evaluated:
            setattr(self, '_elements_cached', list(self._select()))
        return self._elements_cached

    def __add__(self, other):
        """
        Return a union of the two selectors.

        Where possible, avoid evaluating either selector to batch queries.
        """

        if not self.evaluated \
                and isinstance(other, ElementSelector) \
                and not other.evaluated \
                and self.filter_displayed == other.filter_displayed \
                and self.filter_enabled == other.filter_enabled:
            # Both summands are delayed, return a new delayed selector
            return ElementSelector(
                self.browser,
                xpath=self.xpath + '|' + other.xpath,
                filter_displayed=self.filter_displayed,
                filter_enabled=self.filter_enabled,
            )
        else:
            # Have to evaluate everything now
            # other can be either an already evaluated ElementSelector, a list
            # or a single element
            try:
                other = list(other)
            except TypeError:
                other = [other]

            return ElementSelector(self.browser, elements=list(self) + other)

    # The class behaves as a container for the elements, fetching the list from
    # the browser on the first attempt to enumerate itself.

    def __len__(self):
        return len(self._elements())

    def __getitem__(self, key):
        return self._elements()[key]  # pylint:disable=unsubscriptable-object

    def __iter__(self):
        for el in self._elements():  # pylint:disable=not-an-iterable
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
    """
    Return an :class:`ElementSelector` for the element referenced by a `label`s
    ``for`` attribute. The label must be visible.

    :param browser: ``world.browser``
    :param label: label text to return the referenced element for.

    Returns: an :class:`ElementSelector`
    """
    label = ElementSelector(browser,
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
    """
    Find a button with the given value.

    Searches for `submit`, `reset`, `button` and `image` buttons.

    Returns: an :class:`ElementSelector`
    """
    field_types = (
        'submit',
        'reset',
        'button',
        'image',
    )

    return reduce(
        operator.add,
        (find_field_with_value(browser, field_type, value)
         for field_type in field_types)
    )


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


def find_field(browser, field_type, value):
    """
    Locate an input field.

    :param browser: ``world.browser``
    :param string field_type: a field type (i.e. `button`)
    :param string value: an id, name or label

    This first looks for `value` as the id of the element, else
    the name of the element, else as a label for the element.

    Returns: an :class:`ElementSelector`
    """
    return find_field_by_id(browser, field_type, value) + \
        find_field_by_name(browser, field_type, value) + \
        find_field_by_label(browser, field_type, value)


def find_any_field(browser, field_types, field_name):
    """
    Find a field of any of the specified types.

    :param browser: ``world.browser``
    :param list field_types: a list of field type (i.e. `button`)
    :param string value: an id, name or label

    Returns: an :class:`ElementSelector`

    See also: :func:`find_field`.
    """

    return reduce(
        operator.add,
        (find_field(browser, field_type, field_name)
         for field_type in field_types)
    )


def find_field_by_id(browser, field_type, id):
    """
    Locate the control input with the given ``id``.

    :param browser: ``world.browser``
    :param string field_type: a field type (i.e. `button`)
    :param string id: ``id`` attribute

    Returns: an :class:`ElementSelector`
    """
    return ElementSelector(
        browser,
        xpath=field_xpath(field_type, 'id') % string_literal(id),
        filter_displayed=True,
    )


def find_field_by_name(browser, field_type, name):
    """
    Locate the control input with the given ``name``.

    :param browser: ``world.browser``
    :param string field_type: a field type (i.e. `button`)
    :param string name: ``name`` attribute

    Returns: an :class:`ElementSelector`
    """
    return ElementSelector(
        browser,
        field_xpath(field_type, 'name') %
        string_literal(name),
        filter_displayed=True,
    )


def find_field_by_value(browser, field_type, name):
    """
    Locate the control input with the given ``value``. Useful for buttons.

    :param browser: ``world.browser``
    :param string field_type: a field type (i.e. `button`)
    :param string name: ``value`` attribute

    Returns: an :class:`ElementSelector`
    """
    xpath = field_xpath(field_type, 'value') % string_literal(name)
    elems = ElementSelector(
        browser,
        xpath=str(xpath),
        filter_displayed=True,
        filter_enabled=True,
    )

    # sort by shortest first (most closely matching)
    if field_type == 'button':
        elems = sorted(elems, key=lambda elem: len(elem.text))
    else:
        elems = sorted(elems,
                       key=lambda elem: len(elem.get_attribute('value')))

    if elems:
        elems = [elems[0]]  # pylint:disable=redefined-variable-type

    return ElementSelector(browser, elements=elems)


def find_field_by_label(browser, field_type, label):
    """
    Locate the control input that has a label pointing to it.

    :param browser: ``world.browser``
    :param string field_type: a field type (i.e. `button`)
    :param string label: label text

    This will first locate the label element that has a label of the given
    name. It then pulls the id out of the 'for' attribute, and uses it to
    locate the element by its id.

    Returns: an :class:`ElementSelector`
    """

    return ElementSelector(
        browser,
        xpath=field_xpath(field_type, 'id') %
        '//label[contains(., {0})]/@for'.format(
            string_literal(label)),
        filter_displayed=True,
    )


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

    Adds a kwarg `timeout` to `func` which is a number of seconds to try
    for (default 15).
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
