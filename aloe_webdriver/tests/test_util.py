# -*- coding: utf-8 -*-
"""Test step functions directly."""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import unittest

from selenium import webdriver

from aloe import world
from aloe_webdriver.tests.base import PAGES

# pylint:disable=missing-docstring


class TestUtil(unittest.TestCase):
    def setUp(self):
        world.browser = webdriver.Firefox()
        world.browser.get(PAGES['basic_page'])

    def tearDown(self):
        world.browser.quit()
        delattr(world, 'browser')

    def test_find_by_id(self):
        from aloe_webdriver.util import find_field_by_id
        assert find_field_by_id(world.browser, 'password', 'pass')

    def test_find_by_name(self):
        from aloe_webdriver.util import find_field_by_name
        assert find_field_by_name(world.browser, 'submit', 'submit')
        assert find_field_by_name(world.browser, 'select', 'car_choice')
        assert find_field_by_name(world.browser, 'textarea', 'bio')

    def test_find_by_label(self):
        from aloe_webdriver.util import find_field_by_label
        assert find_field_by_label(world.browser, 'text', 'Username:')

    def test_no_label(self):
        from aloe_webdriver.util import find_field_by_label
        assert not find_field_by_label(world.browser, 'text', 'NoSuchLabel')

    def test_find_field(self):
        from aloe_webdriver.util import find_field
        assert find_field(world.browser, 'text', 'username')
        assert find_field(world.browser, 'text', 'Username:')
        assert find_field(world.browser, 'text', 'user')
        assert find_field(world.browser, 'text', 'ชื่อ:')

    def test_find_button(self):
        from aloe_webdriver.util import find_button
        assert find_button(world.browser, 'submit')
        assert find_button(world.browser, 'Submit!')
        assert find_button(world.browser, 'submit_tentative')
        assert find_button(world.browser, 'Submit as tentative')
        assert find_button(world.browser, 'ส่งฟอร์ม')

    def test_option_in_select(self):
        from aloe_webdriver.util import option_in_select
        assert option_in_select(world.browser, 'Favorite Colors:', 'Blue')
        assert option_in_select(world.browser, 'Favorite Colors:', 'ฟ้า')

    def test_wait_for(self):
        from aloe_webdriver.util import wait_for

        counter = [0]

        @wait_for
        def lazy_function(i):
            counter[0] += 1
            return counter[0] > i

        # pylint:disable=unexpected-keyword-arg
        # wait_for decorator parses the argument
        assert not lazy_function(10, timeout=1)
        assert lazy_function(5, timeout=1)
