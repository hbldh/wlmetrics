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

import numpy as np

from wlmetrics.quaternion import Quaternion

__all__ = ['MadgwickAHRSFilter']

try:
    from . import madgwick
except Exception as e:
    raise


class MadgwickAHRSFilter(object):
    """Python """

    def __init__(self, frequency):
        """Constructor for MadgwickAHRSFilter"""
        self.frequency = frequency
        self.quaternion = Quaternion([1, 0, 0, 0])

    def update_filter(self, a, g, m=None):
        if m is None:
            self.quaternion = Quaternion(madgwick.magdwick_AHRS_update_IMU(
                a[0], a[1], a[2], g[0], g[1], g[2],
                self.frequency, *self.quaternion.to_array()))
        else:
            self.quaternion = Quaternion(madgwick.magdwick_AHRS_update(
                a[0], a[1], a[2], g[0], g[1], g[2], m[0], m[1], m[2],
                self.frequency, *self.quaternion.to_array()))

    def filter(self, observations):
        states = []
        for observation in observations:
            if len(observation) == 9:
                self.update_filter(observation[:3], observation[3:6], observation[6:])
            elif len(observation) == 6:
                self.update_filter(observation[:3], observation[3:6])
            states.append(self.quaternion.to_array())

        return np.array(states)


