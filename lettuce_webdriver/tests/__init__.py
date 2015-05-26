from __future__ import print_function

import os
from contextlib import contextmanager

from selenium import webdriver

from aloe import around, before, world

here = os.path.dirname(__file__)
html_pages = os.path.join(here, 'html_pages')


@around.all
@contextmanager
def with_browser():
    world.browser = webdriver.Firefox()
    world.browser.get('')
    yield
    world.browser.quit()
    delattr(world, 'browser')


@before.each_feature
def reset_page(feature):
    world.browser.get('')


@around.each_step
@contextmanager
def print_source(step):
    try:
        yield
    except:
        try:
            step_container = step.scenario
        except AttributeError:
            step_container = step.background

        print(step_container.feature.name)
        print(step_container.name)
        print(step.sentence)
        print(world.browser.page_source)
        print(world.browser.get_screenshot_as_base64())
        raise
