#!/usr/bin/env python

# scrapy_webdriver distutils setup script.

import os
import sys

from scrapy_webdriver import metadata

# Auto-install and download distribute.
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requirements = [
    'selenium>=2.27.0',
]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name=metadata.title,
    version=metadata.version,
    author=metadata.authors[0],
    author_email=metadata.emails[0],
    maintainer=metadata.authors[0],
    maintainer_email=metadata.emails[0],
    url=metadata.url,
    description=metadata.description,
    long_description=read('README.md'),
    license='LICENSE.txt',
    download_url=metadata.url,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',  # Not tested. Patches welcome.
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=find_packages(),
    install_requires=install_requirements,
    zip_safe=False,
    tests_require=['mock', 'pytest', 'scrapy'],
    cmdclass={'test': PyTest},
)
