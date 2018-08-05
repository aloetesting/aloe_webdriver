"""
Setup script.
"""

from setuptools import setup, find_packages

if __name__ == '__main__':
    with \
            open('requirements.txt') as requirements, \
            open('test_requirements.txt') as test_requirements, \
            open('README.md') as readme:
        setup(
            name='aloe_webdriver',
            use_scm_version=True,
            description='Selenium webdriver extension for Aloe',
            author=", ".join((
                'Alexey Kotlyarov',
                'Danielle Madeley',
                'Nick Pilon',
                'Ben Bangert',
            )),
            author_email=', '.join((
                'a@koterpillar.com',
                'danielle@madeley.id.au',
                'npilon@gmail.com',
                'ben@groovie.org',
            )),
            url="https://github.com/aloetesting/aloe_webdriver/",
            long_description=readme.read(),
            classifiers=[
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 3',
            ],

            packages=find_packages(),
            include_package_data=True,

            setup_requires=['setuptools_scm'],

            install_requires=requirements.readlines(),

            test_suite='aloe_webdriver',
            tests_require=test_requirements.readlines(),
        )
