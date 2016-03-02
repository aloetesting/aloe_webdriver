"""
Base functions for tests.
"""

import os
from functools import wraps

from aloe.testing import in_directory


PAGES_DIR = os.path.join(os.path.dirname(__file__), 'html_pages')


# The dictionary of pages that can be used in tests
PAGES = {}
for filename in os.listdir(PAGES_DIR):
    name = filename.split('.html')[0]
    PAGES[name] = 'file://%s' % os.path.join(PAGES_DIR, filename)


def feature(fails=False):
    """
    Decorate a test method to test the feature contained in its docstring.

    For example:
        @feature(failed=False)
        def test_some_feature(self):
            '''
            When I visit "{page1}"
            Then I should ...
            '''
    """

    def outer(func):
        """
        A decorator to run the function as the feature contained in docstring.
        """

        @wraps(func)
        @in_directory('tests')
        def inner(self):
            """Run the scenario from docstring."""

            scenario_string = func.__doc__.format(**PAGES)

            feature_string = """
            Feature: {func.__name__}
            Scenario: {func.__name__}
            {scenario_string}
            """.format(func=func, scenario_string=scenario_string)

            result = self.run_feature_string(feature_string)

            if fails:
                self.assertFalse(result.success)
            else:
                self.assertTrue(result.success)

        return inner

    return outer
