# -*- coding: utf-8 -*-
"""
Test saving screenshots after failed steps.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# pylint:disable=redefined-builtin,unused-wildcard-import,wildcard-import
from builtins import *
# pylint:enable=redefined-builtin,unused-wildcard-import,wildcard-import

import re
import os
import shutil
import tempfile
from glob import iglob

from aloe.testing import FeatureTest, in_directory


@in_directory(os.path.dirname(__file__))
class TestScreenshots(FeatureTest):
    """Test saving screenshots after failed steps."""

    dir_path = None

    def cleanup_screenshots(self):
        """Clean up any screenshots taken."""

        for ext in ('png', 'html'):
            for filename in iglob('failed_*.{}'.format(ext)):
                os.unlink(filename)

        # Delete temporary directory if any.
        if self.dir_path:
            shutil.rmtree(self.dir_path)

    def setUp(self):
        """Enable the hooks for taking screenshots."""

        super(TestScreenshots, self).setUp()

        self.cleanup_screenshots()

        # This environment variable controls whether the screenshot hooks are
        # registered in tests/features/steps.py
        os.environ['TAKE_SCREENSHOTS'] = '1'

    def tearDown(self):
        """Remove all the screenshot files."""

        del os.environ['TAKE_SCREENSHOTS']

        if 'SCREENSHOTS_DIR' in os.environ:
            del os.environ['SCREENSHOTS_DIR']

        self.cleanup_screenshots()

        super(TestScreenshots, self).tearDown()

    def feature_name(self, test_result):
        """
        The feature file name as visible in the failed screenshot/page source
        file name.

        Needed because the feature will be put in a temporary file with a
        different name each time.

        :param test_result: Result of running the feature
        """

        feature_filename = os.path.relpath(test_result.tests_run[0])
        return re.sub(r'\W', '_', feature_filename)

    def show_files(self):
        """
        Print all the file names matching the screenshot/page source pattern in
        the directory.
        """

        for filename in iglob('failed_*'):
            print(filename)

        # List content of temporary directory, if defined.
        if self.dir_path:
            for filename in iglob(os.path.join(self.dir_path, '*')):
                print(filename)

    def assert_file_present(self, filename, message):
        """Assert a file exists."""

        if os.path.exists(filename):
            return

        self.show_files()
        raise AssertionError(message)

    def assert_file_absent(self, filename, message):
        """Assert a file does not exist."""

        if not os.path.exists(filename):
            return

        self.show_files()
        raise AssertionError(message)

    def test_failed_screenshots(self):
        """Test that failed tests screenshots and page source are recorded."""

        feature_string = """
Feature: Test screenshots on failed steps

Scenario: This scenario succeeds
    When I visit test page "basic_page"
    Then I should see "Hello there"

Scenario: This scenario fails
    When I visit test page "basic_page"
    Then I should see "A unicorn"
"""

        result = self.run_feature_string(feature_string)
        feature = self.feature_name(result)

        self.assert_file_absent(
            'failed_{}_1_This_scenario_succeeds.png'.format(feature),
            "Successful scenario should not be screenshotted."
        )
        self.assert_file_absent(
            'failed_{}_1_This_scenario_succeeds.html'.format(feature),
            "Successful scenario page source should not be saved."
        )

        self.assert_file_present(
            'failed_{}_2_This_scenario_fails.png'.format(feature),
            "Failed scenario should be screenshotted."
        )
        with open('failed_{}_2_This_scenario_fails.html'.format(feature)) \
                as page_source:
            self.assertIn("<title>A Basic Page</title>", page_source.read(),
                          "Failed scenario page source should be saved.")

    def test_failed_background(self):
        """Test that failure of a background step is recorded."""

        feature_string = """
# language: zh-CN
功能: 背景失败

    背景:
        当I visit test page "basic_page"
        那么I should see "A unicorn"

    场景: 必须有场景
        那么I should see "Hello there"
"""

        result = self.run_feature_string(feature_string)
        feature = self.feature_name(result)

        self.assert_file_present(
            'failed_{}_0_背景.png'.format(feature),
            "Failed background should be screenshotted."
        )
        with open('failed_{}_0_背景.html'.format(feature)) as page_source:
            self.assertIn("<title>A Basic Page</title>", page_source.read(),
                          "Failed background page source should be saved.")

    def test_failed_examples(self):
        """Test that failure in an example is recorded."""

        feature_string = """
Feature: Test screenshots on examples

Scenario Outline: Succeeds sometimes
    When I visit test page "basic_page"
    Then I should see "<text>"

    Examples:
        | text        |
        | Hello there |
        | A unicorn   |
"""

        result = self.run_feature_string(feature_string)
        feature = self.feature_name(result)

        self.assert_file_absent(
            'failed_{}_1_Succeeds_sometimes_1.png'.format(feature),
            "Successful example should not be screenshotted."
        )
        self.assert_file_present(
            'failed_{}_1_Succeeds_sometimes_2.png'.format(feature),
            "Failed example should be screenshotted."
        )
        with open('failed_{}_1_Succeeds_sometimes_2.html'.format(feature)) \
                as page_source:
            self.assertIn("<title>A Basic Page</title>", page_source.read(),
                          "Failed example page source should be saved.")

    def test_failed_screenshots_to_dir(self):
        """
        Test failed tests screenshots are saved in the specified directory.
        """

        feature_string = """
Feature: Test screenshots on failed steps

Scenario: This scenario fails
    When I visit test page "basic_page"
    Then I should see "A unicorn"
"""
        self.dir_path = tempfile.mkdtemp()
        os.environ['SCREENSHOTS_DIR'] = self.dir_path
        result = self.run_feature_string(feature_string)
        feature = self.feature_name(result)

        template = 'failed_{}_1_This_scenario_fails.{}'
        png_file = os.path.join(self.dir_path, template.format(feature, 'png'))
        html_file = os.path.join(
            self.dir_path, template.format(feature, 'html'))

        self.assert_file_present(
            png_file,
            "Failed scenario should be screenshotted."
        )
        with open(html_file) as page_source:
            self.assertIn("<title>A Basic Page</title>", page_source.read(),
                          "Failed scenario page source should be saved.")
