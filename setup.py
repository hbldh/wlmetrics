# -*- coding: utf-8 -*-
"""
:mod:`setup.py` -- wlmetrics Setup file
======================================

.. module:: setup
   :platform: Unix, Windows
   :synopsis: The Python Packaging setup file for wlmetrics.

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2013-09-14, 19:31

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import wlmetrics
from setuptools import setup, find_packages, Extension

madgwick = Extension('wlmetrics.filter.madgwick.madgwick',
                     include_dirs=['wlmetrics/filter/madgwick/src'],
                     sources=['wlmetrics/filter/madgwick/src/madgwick.c',
                              'wlmetrics/filter/madgwick/src/MadgwickAHRS.c'])
mahony = Extension('wlmetrics.filter.mahony.mahony',
                     include_dirs=['wlmetrics/filter/mahony/src'],
                     sources=['wlmetrics/filter/mahony/src/mahony.c',
                              'wlmetrics/filter/mahony/src/MahonyAHRS.c'])

setup(
    name='wlmetrics',
    version=wlmetrics.__version__,
    author=wlmetrics.author,
    author_email=wlmetrics.author_email,
    maintainer=wlmetrics.maintainer,
    maintainer_email=wlmetrics.maintainer_email,
    url=wlmetrics.url,
    download_url=wlmetrics.download_url,
    description=wlmetrics.description,
    long_description=wlmetrics.long_description,
    license=wlmetrics.license,
    platforms=wlmetrics.platforms,
    keywords=wlmetrics.keywords,
    classifiers=wlmetrics.classifiers,
    packages=find_packages(),
    package_data={
        'docs': [
            '*',
        ],
    },
    install_requires=[
        'numpy>=1.9.0',
    ],
    dependency_links=[],
    ext_modules=[
        madgwick,
        mahony
        ],
    entry_points={
        'console_scripts': [
        ]
    }
)

