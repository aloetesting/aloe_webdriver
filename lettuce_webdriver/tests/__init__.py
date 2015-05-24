import os
from contextlib import contextmanager

from selenium import webdriver

from aloe import around, world

here = os.path.dirname(__file__)
html_pages = os.path.join(here, 'html_pages')


@around.each_feature
@contextmanager
def with_browser(feature):
    world.browser = webdriver.Firefox()
    world.browser.get('')
    yield
    world.browser.quit()
