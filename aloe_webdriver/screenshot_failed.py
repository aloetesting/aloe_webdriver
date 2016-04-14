"""
Hooks to save screenshots and HTML source of the pages when tests fail.

Assumes a browser instance is stored in `world.browser`.
"""

import re
import os

from aloe import after, world


FORMAT = 'failed_{feature_file}_{scenario_index}_{scenario_name}'

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
        # FIXME: localize
        scenario_name = "Background"
        scenario_index = 0

    base_name = FORMAT.format(
        feature_file=os.path.relpath(self.feature.filename),
        scenario_index=scenario_index,
        scenario_name=scenario_name,
    )
    base_name = re.sub(r'\W', '_', base_name)

    world.browser.save_screenshot('{}.png'.format(base_name))

    with open('{}.html'.format(base_name), 'w') as page_source_file:
        page_source_file.write(world.browser.page_source)
