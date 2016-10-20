"""
Basic Selenium_ :class:`Webdriver` steps for Aloe_.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# pylint:disable=redefined-builtin
from builtins import str
# pylint:enable=redefined-builtin

from aloe import step, world

from aloe_webdriver.util import (
    ElementSelector,
    find_any_field,
    find_button,
    find_field,
    find_option,
    option_in_select,
    wait_for,
    string_literal,
)

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    NoAlertPresentException,
    WebDriverException)

# pylint:disable=missing-docstring

# Pylint cannot infer the attributes on world
# pylint:disable=no-member


def contains_content(browser, content):
    """
    Search for an element that contains the whole of the text we're looking
    for in it or its subelements, but whose children do NOT contain that
    text - otherwise matches <body> or <html> or other similarly useless
    things.
    """
    for elem in browser.find_elements_by_xpath(str(
            '//*[contains(normalize-space(.), {content}) '
            'and not(./*[contains(normalize-space(.), {content})])]'
            .format(content=string_literal(content)))):

        try:
            if elem.is_displayed():
                return True
        except StaleElementReferenceException:
            pass

    return False


# Navigation ################################################################


@step('I visit "(.*?)"$')
@step('I go to "(.*?)"$')
def visit(self, url):
    """Navigate to the provided (fully qualified) URL."""
    world.browser.get(url)


@step('The browser\'s URL should be "([^"]*)"$')
@step('I should be at "([^"]*)"$')
@wait_for
def url_should_be(self, url):
    """Assert the absolute URL of the browser is as provided."""

    if world.browser.current_url != url:
        raise AssertionError(
            "Browser URL expected to be {!r}, got {!r}.".format(
                url, world.browser.current_url))


@step('''The browser's URL should contain "([^"]*)"$''')
@wait_for
def url_should_contain(self, url):
    """Assert the absolute URL of the browser contains the provided."""

    if url not in world.browser.current_url:
        raise AssertionError(
            "Browser URL expected to contain {!r}, got {!r}.".format(
                url, world.browser.current_url))


@step('''The browser's URL should not contain "([^"]*)"$''')
@wait_for
def url_should_not_contain(self, url):
    """Assert the absolute URL of the browser does not contain the provided."""

    if url in world.browser.current_url:
        raise AssertionError(
            "Browser URL expected not to contain {!r}, got {!r}.".format(
                url, world.browser.current_url))


@step(r'The page title should be "([^"]*)"')
@step(r"The page title should be '([^']*)'")
@wait_for
def page_title(self, title):
    """
    Assert the page title matches the given text.
    """

    if world.browser.title != title:
        raise AssertionError(
            "Page title expected to be {!r}, got {!r}.".format(
                title, world.browser.title))

# Links #####################################################################


@step('I click "([^"]*)"$')
@step("I click '([^']*)'$")
@wait_for
def click(self, name):
    """Click the link with the provided link text."""
    try:
        elem = world.browser.find_element_by_link_text(name)
    except NoSuchElementException:
        raise AssertionError(
            "Cannot find the link with text '{}'.".format(name))
    elem.click()


@step('I should see a link with the url "([^"]*)"$')
@wait_for
def should_see_link(self, link_url):
    """Assert a link with the provided URL is visible on the page."""

    elements = ElementSelector(
        world.browser,
        str('//a[@href="%s"]' % link_url),
        filter_displayed=True,
    )
    if not elements:
        raise AssertionError("Expected link not found.")


@step('I should see a link to "([^"]*)" with the url "([^"]*)"$')
@step("I should see a link to '([^']*)' with the url '([^']*)'$")
@wait_for
def should_see_link_text(self, link_text, link_url):
    """Assert a link with the provided text points to the provided URL."""

    elements = ElementSelector(
        world.browser,
        str('//a[@href="%s"][./text()="%s"]' % (link_url, link_text)),
        filter_displayed=True,
    )
    if not elements:
        raise AssertionError("Expected link not found.")


@step('I should see a link that contains the text "([^"]*)" and '
      'the url "([^"]*)"$')
@step("I should see a link that contains the text '([^']*)' and "
      "the url '([^']*)'$")
@wait_for
def should_include_link_text(self, link_text, link_url):
    """
    Assert a link containing the provided text points to the provided URL.
    """

    elements = ElementSelector(
        world.browser,
        str('//a[@href="%s"][contains(., %s)]' %
            (link_url, string_literal(link_text))),
        filter_displayed=True,
    )
    if not elements:
        raise AssertionError("Expected link not found.")


# ID based checks ###########################################################


@step('The element with id of "([^"]*)" contains "([^"]*)"$')
@step("The element with id of '([^']*)' contains '([^']*)'$")
@wait_for
def element_contains(self, element_id, value):
    """
    Assert provided content is contained within an element found by ``id``.
    """

    elements = ElementSelector(
        world.browser,
        str('id("{id}")[contains(., "{value}")]'.format(
            id=element_id, value=value)),
        filter_displayed=True,
    )
    if not elements:
        raise AssertionError("Expected element not found.")


@step('The element with id of "([^"]*)" does not contain "([^"]*)"$')
@step("The element with id of '([^']*)' does not contain '([^']*)'$")
@wait_for
def element_not_contains(self, element_id, value):
    """
    Assert provided content is not contained within an element found by ``id``.
    """
    elem = world.browser.find_elements_by_xpath(str(
        'id("{id}")[contains(., "{value}")]'.format(
            id=element_id, value=value)))
    assert not elem, \
        "Expected element not to contain the given text."


@step(r'I should see an element with id of "([^"]*)" within (\d+) seconds?$')
def should_see_id_in_seconds(self, element_id, timeout):
    """
    Assert an element with the given ``id`` is visible within n seconds.
    """

    def check_element():
        """Check for the element with the given id."""

        assert ElementSelector(
            world.browser,
            'id("%s")' % element_id,
            filter_displayed=True,
        ), "Expected element with given id."

    wait_for(check_element)(timeout=int(timeout))


@step('I should see an element with id of "([^"]*)"$')
@wait_for
def should_see_id(self, element_id):
    """
    Assert an element with the given ``id`` is visible.
    """

    elements = ElementSelector(
        world.browser,
        'id("%s")' % element_id,
        filter_displayed=True,
    )
    if not elements:
        raise AssertionError("Expected element with given id.")


@step('I should not see an element with id of "([^"]*)"$')
@wait_for
def should_not_see_id(self, element_id):
    """
    Assert an element with the given ``id`` is not visible.
    """

    elements = ElementSelector(
        world.browser,
        'id("%s")' % element_id,
        filter_displayed=True,
    )
    if elements:
        raise AssertionError("Expected element with given id to be absent.")


@step(r'Element with id "([^"]*)" should be focused')
@wait_for
def element_focused(self, id_):
    """
    Assert the element is focused.
    """

    try:
        elem = world.browser.find_element_by_id(id_)
    except NoSuchElementException:
        raise AssertionError("Element with ID '{}' not found.".format(id_))

    focused = world.browser.switch_to.active_element

    # Elements don't have __ne__ defined, cannot test for inequality
    if not elem == focused:
        raise AssertionError("Expected element to be focused.")


@step(r'Element with id "([^"]*)" should not be focused')
@wait_for
def element_not_focused(self, id_):
    """
    Assert the element is not focused.
    """

    try:
        elem = world.browser.find_element_by_id(id_)
    except NoSuchElementException:
        raise AssertionError("Element with ID '{}' not found.".format(id_))

    focused = world.browser.switch_to.active_element

    # Elements don't have __ne__ defined, cannot test for inequality
    if elem == focused:
        raise AssertionError("Expected element not to be focused.")


# Text ######################################################################


@step(r'I should see "([^"]+)" within (\d+) seconds?$')
@step(r"I should see '([^']+)' within (\d+) seconds?$")
def should_see_in_seconds(self, text, timeout):
    """
    Assert provided text is visible within n seconds.

    Be aware this text could be anywhere on the screen. Also be aware that
    it might cross several HTML nodes. No determination is made between
    block and inline nodes. Whitespace can be affected.
    """

    def check_element():
        """Check for an element with the given content."""

        assert contains_content(world.browser, text), \
            "Expected element with the given text."

    wait_for(check_element)(timeout=int(timeout))


@step('I should see "([^"]+)"$')
@step("I should see '([^']+)'$")
@step('I see "([^"]+)"$')
@step("I see '([^']+)'$")
@wait_for
def should_see(self, text):
    """
    Assert provided text is visible.

    Be aware this text could be anywhere on the screen. Also be aware that
    it might cross several HTML nodes. No determination is made between
    block and inline nodes. Whitespace can be affected.
    """
    if not contains_content(world.browser, text):
        raise AssertionError("Expected content not found.")


@step('I should not see "([^"]+)"$')
@step("I should not see '([^']+)'$")
@wait_for
def should_not_see(self, text):
    """
    Assert provided text is not visible.

    Be aware that because of the caveats of the positive case, the text MAY
    be on the screen in a slightly different form.
    """
    if contains_content(world.browser, text):
        raise AssertionError("Content unexpectedly found.")


# Forms #####################################################################


@step('I should see a form that goes to "([^"]*)"$')
@wait_for
def see_form(self, url):
    """
    Assert the existence of a HTML form that submits to the given URL.
    """

    elements = ElementSelector(
        world.browser,
        str('//form[@action="%s"]' % url),
        filter_displayed=True,
    )
    if not elements:
        raise AssertionError("Expected form not found.")


DATE_FIELDS = (
    'datetime',
    'datetime-local',
    'date',
)


TEXT_FIELDS = (
    'text',
    'textarea',
    'password',
    'month',
    'time',
    'week',
    'number',
    'range',
    'email',
    'url',
    'tel',
    'color',
)


@step('I fill in "([^"]*)" with "([^"]*)"$')
@step("I fill in '([^']*)' with '([^']*)'$")
@wait_for
def fill_in_textfield(self, field_name, value):
    """
    Fill in the HTML input with given label (recommended), name or id with
    the given text.

    Supported input types are text, textarea, password, month, time, week,
    number, range, email, url, tel and color.
    """

    date_field = find_any_field(world.browser,
                                DATE_FIELDS,
                                field_name)
    if date_field:
        field = date_field
    else:
        field = find_any_field(world.browser,
                               TEXT_FIELDS,
                               field_name)

    if not field:
        raise AssertionError(
            "Cannot find a field named '{}'.".format(field_name))

    if date_field:
        field.send_keys(Keys.DELETE)
    else:
        field.clear()

    field.send_keys(value)


@step('I press "([^"]*)"$')
@step("I press '([^']*)'$")
@wait_for
def press_button(self, value):
    """
    Click the button with the given label.
    """
    button = find_button(world.browser, value)
    if not button:
        raise AssertionError(
            "Cannot find a button named '{}'.".format(value))
    button.click()


@step('I click on label "([^"]*)"')
@step("I click on label '([^']*)'")
@wait_for
def click_on_label(self, label):
    """
    Click on the given label.

    On a correctly set up form this will highlight the appropriate field.
    """

    elem = ElementSelector(
        world.browser,
        str('//label[normalize-space(text())=%s]' % string_literal(label)),
        filter_displayed=True,
    )
    if not elem:
        raise AssertionError(
            "Cannot find a label with text '{}'.".format(label))
    elem.click()


@step(r'Input "([^"]*)" (?:has|should have) value "([^"]*)"')
@step(r"Input '([^']*)' (?:has|should have) value '([^']*)'")
@wait_for
def input_has_value(self, field_name, value):
    """
    Assert the form input with label (recommended), name or id has given value.
    """
    text_field = find_any_field(world.browser,
                                DATE_FIELDS + TEXT_FIELDS,
                                field_name)
    if text_field is False:
        raise AssertionError(
            "Can not find a field named {!r}.".format(field_name))

    actual = text_field.get_attribute('value')
    if actual != value:
        raise AssertionError(
            "Field value expected to be {!r}, got {!r}.".format(
                value, actual))


@step(r'I submit the only form')
@wait_for
def submit_the_only_form(self):
    """
    Look for a form on the page and submit it.

    Asserts if more than one form exists.
    """
    form = ElementSelector(world.browser, str('//form'))
    assert form, "Cannot find a form on the page."
    form.submit()


@step(r'I submit the form with id "([^"]*)"')
@wait_for
def submit_form_id(self, id_):
    """
    Submit the form with given id (used to disambiguate between multiple
    forms).
    """
    form = ElementSelector(
        world.browser,
        str('id("{id}")'.format(id=id_)),
    )
    assert form, "Cannot find a form with ID '{}' on the page.".format(id_)
    form.submit()


@step(r'I submit the form with action "([^"]*)"')
def submit_form_action(self, url):
    """
    Submit the form with the given action URL (i.e. the form that submits to
    ``/post/my/data``).
    """
    form = ElementSelector(
        world.browser,
        str('//form[@action="%s"]' % url),
    )
    assert form, \
        "Cannot find a form with action '{}' on the page.".format(url)
    form.submit()


# Checkboxes ################################################################


@step('I check "([^"]*)"$')
@step("I check '([^']*)'$")
@wait_for
def check_checkbox(self, value):
    """Check the checkbox with label (recommended), name or id."""
    check_box = find_field(world.browser, 'checkbox', value)
    assert check_box, "Cannot find checkbox '{}'.".format(value)
    if not check_box.is_selected():
        check_box.click()


@step('I uncheck "([^"]*)"$')
@step("I uncheck '([^']*)'$")
@wait_for
def uncheck_checkbox(self, value):
    """Uncheck the checkbox with label (recommended), name or id."""
    check_box = find_field(world.browser, 'checkbox', value)
    assert check_box, "Cannot find checkbox '{}'.".format(value)
    if check_box.is_selected():
        check_box.click()


@step('The "([^"]*)" checkbox should be checked$')
@step("The '([^']*)' checkbox should be checked$")
@wait_for
def assert_checked_checkbox(self, value):
    """Assert the checkbox with label (recommended), name or id is checked."""
    check_box = find_field(world.browser, 'checkbox', value)
    assert check_box, "Cannot find checkbox '{}'.".format(value)
    assert check_box.is_selected(), "Check box should be selected."


@step('The "([^"]*)" checkbox should not be checked$')
@step("The '([^']*)' checkbox should not be checked$")
@wait_for
def assert_not_checked_checkbox(self, value):
    """
    Assert the checkbox with label (recommended), name or id is not checked.
    """
    check_box = find_field(world.browser, 'checkbox', value)
    assert check_box, "Cannot find checkbox '{}'.".format(value)
    assert not check_box.is_selected(), "Check box should not be selected."


# Selects ###################################################################


@step('I select "([^"]*)" from "([^"]*)"$')
@step("I select '([^']*)' from '([^']*)'$")
@wait_for
def select_single_item(self, option_name, select_name):
    """
    Select the named option from select with label (recommended), name or id.
    """
    option_box = find_option(world.browser, select_name, option_name)
    assert option_box, "Cannot find option '{}'.".format(option_name)
    option_box.click()


@step('I select the following from "([^"]*?)":?$')
@step("I select the following from '([^']*?)':?$")
@wait_for
def select_multi_items(self, select_name):
    """
    Select multiple options from select with label (recommended), name, or
    id. Pass a multiline string of options. e.g.

    .. code-block:: gherkin

        When I select the following from "Contact Methods":
            \"\"\"
            Email
            Phone
            Fax
            \"\"\"
    """
    # Ensure only the options selected are actually selected
    option_names = self.multiline.split('\n')
    select_box = find_field(world.browser, 'select', select_name)
    assert select_box, "Cannot find a '{}' select.".format(select_name)

    select = Select(select_box)
    select.deselect_all()

    for option in option_names:
        try:
            select.select_by_value(option)
        except NoSuchElementException:
            try:
                select.select_by_visible_text(option)
            except NoSuchElementException:
                raise AssertionError("Cannot find option: '{}'.".format(option))


@step('The "([^"]*)" option from "([^"]*)" should be selected$')
@step("The '([^']*)' option from '([^']*)' should be selected$")
@wait_for
def assert_single_selected(self, option_name, select_name):
    """
    Assert the given option is selected from the select with label
    (recommended), name or id.

    If multiple selections are supported other options may be selected.
    """
    option = find_option(world.browser, select_name, option_name)
    assert option.is_selected(), "Option should be selected."


@step('The following options from "([^"]*?)" should be selected:?$')
@step("The following options from '([^']*?)' should be selected:?$")
@wait_for
def assert_multi_selected(self, select_name):
    select_box = find_field(world.browser, 'select', select_name)
    assert select_box, "Cannot find a '{}' select.".format(select_name)

    option_names = self.multiline.split('\n')
    option_elems = select_box.find_elements_by_xpath(str('./option'))

    # Check only the options that are specified are selected
    for option in option_elems:
        if option.get_attribute('id') in option_names or \
                option.get_attribute('name') in option_names or \
                option.get_attribute('value') in option_names or \
                option.text in option_names:
            assert option.is_selected(), "Option should be selected."
        else:
            assert not option.is_selected(), \
                "Option should not be selected."


@step(r'I should see option "([^"]*)" in selector "([^"]*)"')
@step(r"I should see option '([^']*)' in selector '([^']*)'")
@wait_for
def select_contains(self, option, id_):
    """Assert the select contains the given option."""
    assert option_in_select(world.browser, id_, option) is not None, \
        "Selector should have the given option."


@step(r'I should not see option "([^"]*)" in selector "([^"]*)"')
@step(r"I should not see option '([^']*)' in selector '([^']*)'")
@wait_for
def select_does_not_contain(self, option, id_):
    """Assert the select does not contain the given option."""
    assert option_in_select(world.browser, id_, option) is None, \
        "Selector should not have the given option."


# Radios ####################################################################


@step('I choose "([^"]*)"$')
@step("I choose '([^']*)'$")
@wait_for
def choose_radio(self, value):
    """
    Click (and choose) the radio button with the given label (recommended),
    name or id.
    """
    box = find_field(world.browser, 'radio', value)
    assert box, "Cannot find a '{}' radio button.".format(value)
    box.click()


@step('The "([^"]*)" option should be chosen$')
@step("The '([^']*)' option should be chosen$")
@wait_for
def assert_radio_selected(self, value):
    """
    Assert the radio button with the given label (recommended), name or id is
    chosen.
    """
    radio = find_field(world.browser, 'radio', value)
    assert radio, "Cannot find a '{}' radio button.".format(value)
    assert radio.is_selected(), "Radio button should be selected."


@step('The "([^"]*)" option should not be chosen$')
@step("The '([^']*)' option should not be chosen$")
@wait_for
def assert_radio_not_selected(self, value):
    """
    Assert the radio button with the given label (recommended), name or id is
    not chosen.
    """
    radio = find_field(world.browser, 'radio', value)
    assert radio, "Cannot find a '{}' radio button.".format(value)
    assert not radio.is_selected(), "Radio button should not be selected."


# Alerts ####################################################################


@step('I accept the alert')
def accept_alert(self):
    """
    Accept the alert.
    """

    try:
        alert = Alert(world.browser)
        alert.accept()
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step('I dismiss the alert')
def dismiss_alert(self):
    """
    Dismiss the alert.
    """

    try:
        alert = Alert(world.browser)
        alert.dismiss()
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step(r'I should see an alert with text "([^"]*)"')
@step(r"I should see an alert with text '([^']*)'")
def check_alert(self, text):
    """
    Assert an alert is showing with the given text.
    """

    try:
        alert = Alert(world.browser)
        if alert.text != text:
            raise AssertionError(
                "Alert text expected to be {!r}, got {!r}.".format(
                    text, alert.text))
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step('I should not see an alert')
def check_no_alert(self):
    """
    Assert there is no alert.
    """

    try:
        alert = Alert(world.browser)
        raise AssertionError("Should not see an alert. Alert '%s' shown." %
                             alert.text)
    except NoAlertPresentException:
        pass

# Tooltips ##################################################################


def find_by_tooltip(browser, tooltip):
    """
    Find elements with the given tooltip.

    :param browser: ``world.browser``
    :param tooltip: Tooltip to search for

    Returns: an :class:`ElementSelector`
    """

    return ElementSelector(
        world.browser,
        str('//*[@title=%(tooltip)s or @data-original-title=%(tooltip)s]' %
            dict(tooltip=string_literal(tooltip))),
        filter_displayed=True,
    )


@step(r'I should see an element with tooltip "([^"]*)"')
@step(r"I should see an element with tooltip '([^']*)'")
@wait_for
def see_tooltip(self, tooltip):
    """
    Assert an element with the given tooltip (title) is visible.

    N.B. tooltip may not be visible.
    """

    assert find_by_tooltip(world.browser, tooltip), \
        "Expected element with given tooltip."


@step(r'I should not see an element with tooltip "([^"]*)"')
@step(r"I should not see an element with tooltip '([^']*)'")
@wait_for
def no_see_tooltip(self, tooltip):
    """
    Assert an element with the given tooltip (title) is not visible.
    """

    assert not find_by_tooltip(world.browser, tooltip), \
        "Expected no elements with given tooltip."


@step(r'I (?:click|press) the element with tooltip "([^"]*)"')
@step(r"I (?:click|press) the element with tooltip '([^']*)'")
def press_by_tooltip(self, tooltip):
    """
    Click on a HTML element with a given tooltip.

    This is very useful if you're clicking on icon buttons, etc.
    """
    for button in find_by_tooltip(world.browser, tooltip):
        try:
            button.click()
            break
        except:  # pylint:disable=bare-except
            pass
    else:
        raise AssertionError("No button with tooltip '{0}' found"
                             .format(tooltip))

# Frames ####################################################################


@step(r'I switch to the frame with id "([^"]*)"')
def switch_to_frame_with_id(self, frame):
    """Swap Selenium's context to the given frame or iframe."""
    elem = world.browser.find_element_by_id(frame)
    world.browser.switch_to.frame(elem)


@step(r'I switch to the frame with class "([^"]*)"')
def switch_to_frame_with_class(self, frame):
    """Swap Selenium's context to the given frame or iframe."""
    elem = world.browser.find_element_by_class_name(frame)
    world.browser.switch_to.frame(elem)


@step(r'I switch back to the main view')
def switch_to_main(self):
    """Swap Selenium's context back to the main window."""
    world.browser.switch_to.default_content()
