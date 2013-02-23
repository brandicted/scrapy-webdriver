#!/usr/bin/env python

# scrapy_webdriver distutils setup script

import os
from scrapy_webdriver import metadata

# auto-install and download distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requirements = [
    'selenium>=2.27.0',
]

setup(name=metadata.title,
      version=metadata.version,
      author=metadata.authors[0],
      author_email=metadata.emails[0],
      maintainer=metadata.authors[0],
      maintainer_email=metadata.emails[0],
      url=metadata.url,
      description=metadata.description,
      long_description=read('README.rst'),
      download_url=metadata.url,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
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
      zip_safe=False, # don't use eggs
      )
