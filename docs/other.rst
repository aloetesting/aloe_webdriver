Other Steps
###########

.. toctree::
    :maxdepth: 2

.. currentmodule:: aloe_webdriver

Alerts
======

.. code-block:: python

    import aloe_webdriver

Validate the behaviour of popup alerts.

.. autofunction:: check_alert
.. autofunction:: check_no_alert
.. autofunction:: accept_alert
.. autofunction:: dismiss_alert

Tooltips
========

.. code-block:: python

    import aloe_webdriver

.. autofunction:: see_tooltip
.. autofunction:: no_see_tooltip
.. autofunction:: press_by_tooltip

Checks based on HTML ``id``
===========================

.. code-block:: python

    import aloe_webdriver

Using the HTML ``id`` is generally considered bad BDD, but sometimes it is
the only way to unambiguously refer to an element. It is strongly recommended
to find a more behavioral mechanism to describe your test.
See :ref:`good-bdd`.

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
description. See :ref:`good-bdd`.

.. autofunction:: switch_to_frame
.. autofunction:: switch_to_main

CSS Selectors
=============

.. code-block:: python

    import aloe_webdriver.css

.. automodule:: aloe_webdriver.css

Screenshots
===========

.. code-block:: python

    import aloe_webdriver.screenshot_failed

.. automodule:: aloe_webdriver.screenshot_failed
