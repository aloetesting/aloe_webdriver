"""
Compatibility file to prevent API breakage
"""

import warnings

warnings.warn("This module is deprecated. Import aloe_webdriver directly.",
              DeprecationWarning)

# pylint:disable=wildcard-import, unused-import, redefined-builtin
from . import *
