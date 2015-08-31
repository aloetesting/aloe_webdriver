"""
Setup script.
"""

__version__ = '0.3.5'

from setuptools import setup, find_packages

if __name__ == '__main__':
    with \
            open('requirements.txt') as requirements, \
            open('test_requirements.txt') as test_requirements, \
            open('README.md') as readme:
        setup(
            name='aloe_webdriver',
            version=__version__,
            description='Selenium webdriver extension for Aloe',
            author="Alexey Kotlyarov, Nick Pilon, Ben Bangert",
            author_email="a@koterpillar.com, npilon@gmail.com, ben@groovie.org",
            url="https://github.com/koterpillar/aloe_webdriver/",
            long_description=readme.read(),
            classifiers=[
                'License :: OSI Approved :: ' +
                'GNU General Public License v3 or later (GPLv3+)',
            ],

            packages=find_packages(),
            include_package_data=True,

            install_requires=requirements.readlines(),

            test_suite='aloe_webdriver',
            tests_require=test_requirements.readlines(),
        )
