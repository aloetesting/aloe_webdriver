"""
Base functions for tests.
"""

from functools import wraps

from aloe.testing import in_directory


def feature(fails=False):
    """
    Decorate a test method to test the feature contained in its docstring.

    For example:
        @feature(failed=False)
        def test_some_feature(self):
            '''
            When I ...
            Then I ...
            '''

    The method code is ignored.
    """

    def outer(func):
        """
        A decorator to run the function as the feature contained in docstring.
        """

        @wraps(func)
        @in_directory('tests')
        def inner(self):
            """Run the scenario from docstring."""

            feature_string = """
            Feature: {name}
            Scenario: {name}
            {scenario_string}
            """.format(name=func.__name__, scenario_string=func.__doc__)

            result = self.run_feature_string(feature_string)

            if fails:
                self.assertFalse(result.success)
            else:
                self.assertTrue(result.success)

        return inner

    return outer
