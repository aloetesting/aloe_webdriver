__version__ = '0.3.5'

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(name='aloe_webdriver',
      version=__version__,
      description='Selenium webdriver extension for Aloe',
      long_description=README,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        'Topic :: Software Development :: Testing',
        ],
      author="Nick Pilon, Ben Bangert",
      author_email="npilon@gmail.com, ben@groovie.org",
      url="https://github.com/bbangert/aloe_webdriver/",
      license="MIT",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require = ['aloe', 'nose', 'selenium'],
      install_requires = ['aloe', 'nose', 'selenium'],
      test_suite="aloe_webdriver",
      )
