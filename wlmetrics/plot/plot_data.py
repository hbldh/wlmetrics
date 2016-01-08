#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`plot_data`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-01-06

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from pkg_resources import resource_filename

import numpy as np
from scipy.integrate import cumtrapz
import matplotlib.pyplot as plt

from wlmetrics.filter.madgwick import MadgwickAHRSFilter

from wlmetrics.container import WLMetricsContainer


def plot_rec_1():
    _plot(resource_filename('wlmetrics.data', 'rec_1.json'))


def plot_rec_2_1():
    _plot(resource_filename('wlmetrics.data', 'rec_2_1.json'))


def plot_rec_2_2():
    _plot(resource_filename('wlmetrics.data', 'rec_2_2.json'))


def plot_rec_3():
    _plot(resource_filename('wlmetrics.data', 'rec_3.json'))


def _plot(file_path):
    data = WLMetricsContainer.load(file_path)

    freq = 1/np.mean(np.diff(data.timestamps))
    mfilter = MadgwickAHRSFilter(freq)
    observations = np.concatenate((data.accelerometer, data.gyroscope, data.magnetometer), axis=1)
    orientation = mfilter.filter(observations)

    plt.subplot(231)
    plt.plot(data.timestamps - data.timestamps[0], data.accelerometer)
    plt.title('Accelerometer')
    plt.ylabel('Acceleration (g)')

    plt.subplot(232)
    plt.plot(data.timestamps - data.timestamps[0], data.gyroscope)
    plt.title('Gyroscope')
    plt.ylabel('Rot. Speed (deg/s)')

    plt.subplot(233)
    plt.plot(data.timestamps - data.timestamps[0], data.magnetometer)
    plt.title('Magnetometer')
    plt.ylabel('Mag. Field Str. (?)')

    plt.subplot(234)
    plt.plot((data.timestamps - data.timestamps[0])[1:], cumtrapz(data.accelerometer * 9.81, x=(data.timestamps - data.timestamps[0]), axis=0))
    plt.title('Velocity')
    plt.ylabel('Velocity (m/s)')

    plt.subplot(235)
    plt.plot((data.timestamps - data.timestamps[0])[1:], cumtrapz(data.accelerometer * 9.81, x=data.timestamps - data.timestamps[0], axis=0))
    plt.title('Speed')
    plt.ylabel('Speed (m/s)')

    plt.subplot(236)
    plt.plot((data.timestamps - data.timestamps[0])[2:],
             cumtrapz(cumtrapz(data.accelerometer * 9.81, x=data.timestamps - data.timestamps[0], axis=0),
                      x=(data.timestamps - data.timestamps[0])[1:], axis=0))
    plt.title('Position')
    plt.ylabel('Distance from origin (m)')

    plt.show()

def main():
    # Nbr 1: Ryck
    # Nbr 2.1: Knäböj, hel acceleration
    # Nbr 2.2: Knäböj, Acceleration från mitten
    # Nbr 3: Stöt
    plot_rec_1()
    #plot_rec_2_1()
    #plot_rec_2_2()
    plot_rec_3()

if __name__ == '__main__':
    main()
