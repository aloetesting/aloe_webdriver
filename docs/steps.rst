Basic Steps
===========

.. toctree::
    :maxdepth: 2

.. currentmodule:: aloe_webdriver

Navigation
----------

.. autofunction:: visit
.. autofunction:: url_should_be
.. autofunction:: url_should_contain
.. autofunction:: url_should_not_contain
.. autofunction:: page_title

Text
----

.. autofunction:: should_see
.. autofunction:: should_see_in_seconds
.. autofunction:: should_not_see

Links
-----

.. autofunction:: click
.. autofunction:: should_see_link
.. autofunction:: should_include_link_text

Forms
=====

Steps for referring to form controls typically support three methods to
identify the control:

1. The label of the control. This is the recommended way to refer to a control
   as it is the most descriptive.
2. The control's ``name``. This can be used if you have multiple controls with
   the same label (i.e. in formsets).
3. The control's ``id``.

.. autofunction:: see_form
.. autofunction:: click_on_label
.. autofunction:: submit_the_only_form
.. autofunction:: submit_form_action

Text Fields
-----------

.. autofunction:: fill_in_textfield
.. autofunction:: input_has_value

Buttons
-------

.. autofunction:: press_button

Checkboxes
----------

.. autofunction:: check_checkbox
.. autofunction:: uncheck_checkbox
.. autofunction:: assert_checked_checkbox
.. autofunction:: assert_not_checked_checkbox

Radio Buttons
-------------

.. autofunction:: choose_radio
.. autofunction:: assert_radio_selected
.. autofunction:: assert_radio_not_selected

Selects (Comboboxes)
--------------------

.. autofunction:: select_single_item
.. autofunction:: select_multi_items
.. autofunction:: assert_single_selected
.. autofunction:: assert_multi_selected
.. autofunction:: select_contains
.. autofunction:: select_does_not_contain

Alerts
======

Validate the behaviour of popup alerts.

.. autofunction:: check_alert
.. autofunction:: check_no_alert
.. autofunction:: accept_alert
.. autofunction:: dismiss_alert

Frames
======

Use these steps to switch frames if you need to work in a different frame or
iframe. It is recommended you wrap these steps up in a more behavioural
description.

.. autofunction:: switch_to_frame
.. autofunction:: switch_to_main

Tooltips
========

.. autofunction:: see_tooltip
.. autofunction:: no_see_tooltip
.. autofunction:: press_by_tooltip

Checks based on HTML ``id``
===========================

Using the HTML ``id`` is generally considered bad BDD, but sometimes it is
the only way to unambiguously refer to an element. It is strongly recommended
to find a more behaviour mechanism to describe your test.

.. autofunction:: element_contains
.. autofunction:: element_not_contains
.. autofunction:: should_see_id
.. autofunction:: should_see_id_in_seconds
.. autofunction:: should_not_see_id
.. autofunction:: element_focused
.. autofunction:: element_not_focused
.. autofunction:: submit_form_id
