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

import numpy as np
import scipy.integrate as scint
import matplotlib.pyplot as plt

from pyberryimu.calibration.standard import StandardCalibration
from pyberryimu.container import BerryIMUDataContainer


data = BerryIMUDataContainer.load('rec_gyro.json')
sc1 = StandardCalibration.load('/home/hbldh/Dropbox/Encrypted/PyBerryIMU/.pyberryimu-BACKUP_g1')
sc1.gyro_bias_vector *= 57.2957795
sc1.gyro_scale_factor_vector *= 57.2957795
sc2 = StandardCalibration.load('/home/hbldh/Dropbox/Encrypted/PyBerryIMU/.pyberryimu-BACKUP_g2')
sc_sh = StandardCalibration.load('/home/hbldh/Dropbox/Encrypted/PyBerryIMU/.pyberryimu')
sc_sh.set_datasheet_values_for_gyroscope(data.client_settings)

g_sc1 = []
g_sc2 = []
g_sh = []
for row in data.gyroscope:
    g_sc1.append(sc1.transform_gyroscope_values(row.tolist()))
    g_sc2.append(sc2.transform_gyroscope_values(row.tolist()))
    g_sh.append(sc_sh.transform_gyroscope_values(row.tolist()))

d = 0
g_sc1 = np.array(g_sc1)
g_sc2 = np.array(g_sc2)
g_sh = np.array(g_sh)

plt.plot(g_sc1[:, d], 'b')
plt.plot(scint.cumtrapz(g_sh[:, d], dx=1/100.), 'm')
#plt.plot(g_sc2[:, d], 'g')
#plt.plot(g_sh[:, d], 'r')
plt.show()
