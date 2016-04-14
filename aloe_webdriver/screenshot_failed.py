"""
Hooks to save screenshots and HTML source of the pages when tests fail.

Assumes a browser instance is stored in ``world.browser``.

Whenever a step fails, the screen shot and the HTML source of the page
displayed in the browser are saved to the current directory. The file names
include the feature file name, scenario number and name and, if applicable,
the example number.

Consider the following feature:

.. code-block:: gherkin

    # features/account.feature
    Feature: Account management

        Scenario: Log in
            Given I open the site
            And I enter username and password
            And I press "Log in"
            Then I should see "Logged in"

If there will be no "Logged in" text when expected, screenshot and the page
source will be saved to, respectively::

    failed_features_account_feature_1_Log_in.png
    failed_features_account_feature_1_Log_in.html
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

from aloe import after, before, world

# Pylint cannot infer the attributes on world
# pylint:disable=no-member


FORMAT = 'failed_{feature_file}_{scenario_index}_{scenario_name}{outline_index}'


@before.each_example
def reset_example_count(scenario, outlines, steps):
    """Count the scenario outline index for taking screenshots."""

    if outlines:
        world.outline_index = scenario.outlines.index(outlines) + 1
    else:
        world.outline_index = None


@after.each_step
def take_screenshot(self):
    """Take a screenshot after a failed step."""

    if not self.failed:
        return

    browser = getattr(world, 'browser', None)
    if not browser:
        return

    try:
        scenario_name = self.scenario.name
        scenario_index = \
            self.scenario.feature.scenarios.index(self.scenario) + 1
    except AttributeError:
        scenario_name = self.background.keyword
        scenario_index = 0

    if world.outline_index is None:
        outline_index_str = ''
    else:
        outline_index_str = '_{}'.format(world.outline_index)

    base_name = FORMAT.format(
        feature_file=os.path.relpath(self.feature.filename),
        scenario_index=scenario_index,
        scenario_name=scenario_name,
        outline_index=outline_index_str,
    )
    base_name = re.sub(r'\W', '_', base_name, flags=re.UNICODE)

    world.browser.save_screenshot('{}.png'.format(base_name))

    with open('{}.html'.format(base_name), 'w') as page_source_file:
        page_source_file.write(world.browser.page_source)
