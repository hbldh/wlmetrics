#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`madgwick`
==================

.. module:: madgwick
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-06-21, 20:36

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import


__all__ = ['MadgwickAHRSFilter']

try:
    # noinspection PyStatementEffect
    import .madgwick as madgwick_methods
except ImportError:
    raise


class MadgwickAHRSFilter(object):
    """Python """

    def __init__(self, frequency):
        """Constructor for MadgwickAHRSFilter"""
        self.frequency = frequency
        self.quaternion = (1, 0, 0, 0)

