Forms
=====

.. toctree::
    :maxdepth: 2

.. currentmodule:: aloe_webdriver

.. code-block:: python

    import aloe_webdriver

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
