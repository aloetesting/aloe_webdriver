Getting Started
===============

Create a file in your `steps/` directory, i.e. `steps/browser.py` and import
the `Aloe-Webdriver` steps.

You are also responsible for building and maintaining the lifecycle of your
:mod:`selenium.webdriver` referenced ``world.browser``.

.. code-block:: python

    from contextlib import contextmanager

    import aloe_webdriver
    from aloe import around, world
    from selenium import webdriver

    @around.all
    @contextmanager
    def with_browser():
        world.browser = webdriver.Firefox()
        yield
        world.browser.quit()
        delattr(world, 'browser')
