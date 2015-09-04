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

Use :meth:`step.behave_as` to call these steps from ones of your own step to
abstract the mechanics of your website into something more descriptive. This
also makes it easier if you ever change the login process.
For example:

.. code-block:: python

    @step("I log in")
    def i_log_in():
        '''Log in to the site'''
        step.when('I switch to the frame with id "login-frame"')
        step.when('I fill in "Username" with "alexey"')
        step.when('I submit the only form')

.. autofunction:: element_contains
.. autofunction:: element_not_contains
.. autofunction:: should_see_id
.. autofunction:: should_see_id_in_seconds
.. autofunction:: should_not_see_id
.. autofunction:: submit_form_id

Focus
-----

.. autofunction:: element_focused
.. autofunction:: element_not_focused

Frames
------

Use these steps to switch frames if you need to work in a different frame or
iframe. It is recommended you wrap these steps up in a more behavioural
description.

.. autofunction:: switch_to_frame
.. autofunction:: switch_to_main

CSS Selectors
=============

.. automodule:: aloe_webdriver.css

Screenshots
===========

.. automodule:: aloe_webdriver.screenshot
