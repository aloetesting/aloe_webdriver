Other Steps
###########

.. toctree::
    :maxdepth: 2

.. currentmodule:: aloe_webdriver

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
