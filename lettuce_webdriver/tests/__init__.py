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
