#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`processing`
==================

.. module:: processing
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-08-26, 14:48

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from pyberryimu.container import BerryIMUDataContainer

data = BerryIMUDataContainer.load('rec_gyro.json')
