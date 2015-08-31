"""
Base functions for tests.
"""

import os
from functools import wraps

from aloe.testing import in_directory


def feature(fails=False):
    """
    Decorate a test method to test the feature contained in its docstring.

    Apply the context returned by the method to the feature.

    For example:
        @feature(failed=False)
        def test_some_feature(self):
            '''
            Feature: This name is returned
                Scenario: ...
                    When I {variable}
            '''

            return dict(variable=something)
    """

    def outer(func):
        """
        A decorator to run the function as the feature contained in docstring.
        """

        @wraps(func)
        @in_directory('tests')
        def inner(self):
            """Run the feature from docstring."""
            params = func(self)
            feature_string = func.__doc__.format(**params)

            result = self.run_feature_string(feature_string)

            if fails:
                self.assertFalse(result.success)
            else:
                self.assertTrue(result.success)

        return inner

    return outer


PAGES_DIR = os.path.join(os.path.dirname(__file__), 'html_pages')


PAGES = {}
for filename in os.listdir(PAGES_DIR):
    name = filename.split('.html')[0]
    PAGES[name] = 'file://%s' % os.path.join(PAGES_DIR, filename)
