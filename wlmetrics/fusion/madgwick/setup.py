#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`setup.py`
==================

.. module:: setup.py
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-06-21, 20:36

"""

from __future__ import division
from __future__ import print_function
#from __future__ import unicode_literals
from __future__ import absolute_import

from distutils.core import setup, Extension

madgwick = Extension('madgwick',
                    include_dirs=['src'],
                    sources=['madgwick.c', 'src/MahonyAHRS.c'])

setup(name='Madgwick Extension',
      version='0.0.1',
      description='This is a demo package',
      ext_modules=[madgwick])
