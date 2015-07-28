#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`static`
==================

.. module:: static
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-06-21, 23:12

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import time

import numpy as np

from wlmetrics.filter.kalman.kalman import KalmanFilter


class StaticDetectingPositionKalmanFilter(KalmanFilter):

    def __init__(self, data_freq, static_threshold=0.1, static_time=0.25):

        self.f = data_freq
        self.static_threshold = static_threshold
        self.static_time = static_time

        transition_matrix = np.eye(9)
        transition_matrix[[3, 4, 5], [0, 1, 2]] = 1 / data_freq
        transition_matrix[[6, 7, 8], [3, 4, 5]] = 1 / data_freq

        transition_covariance = np.eye(9)

        observation_matrix = np.zeros((3, 9), 'float')
        observation_matrix[[0, 1, 2], [0, 1, 2]] = 1

        observation_covariance = np.eye(3) * 20

        super(StaticDetectingPositionKalmanFilter, self).__init__(
            transition_matrix, transition_covariance, observation_matrix, observation_covariance)

        self._static_counter = self.f

        self.set_initial_state(np.zeros((len(transition_matrix), ), 'float'),
                               np.zeros((len(transition_matrix), len(transition_matrix)), 'float'))

    def filter(self, observations):
        states = []
        gravity = []
        static_array = []
        static_position = None

        current_gravity_vector = observations[0, :]
        static_since = 0

        X = self.X
        P = self.P

        for i, observation in enumerate(observations):
            if np.abs(1 - np.linalg.norm(observation)) < self.static_threshold and self.is_static():
                current_gravity_vector = np.mean(observations[static_since:i+1, :], 0)
                static_array.append(1)
                X[3:6] = 0
                static_position = X[6:].copy()
            else:
                if np.abs(1 - np.linalg.norm(observation)) < self.static_threshold:
                    self._static_counter += 1
                    if self.is_static():
                        static_since = i
                        current_gravity_vector = np.mean(observations[static_since:i + 1, :], 0)
                        static_array.append(1)
                        X[3:6] = 0
                        static_position = X[6:].copy()

                    else:
                        static_array.append(0.5)
                else:
                    self._static_counter = 0
                    static_since = None
                    static_array.append(0)
            gravity.append(current_gravity_vector.copy())
            X, P = self.kf_predict(X, P)
            if self.is_static():
                X[3:6] = 0
                X[6:] = static_position
            X, P, K, IM, IS = self.kf_update(X, P, (observation - current_gravity_vector) * 9.81)
            if self.is_static():
                X[3:6] = 0
                X[6:] = static_position
            states.append(X)

        return np.array(states), np.array(static_array), np.array(gravity)

    def is_static(self):
        return self._static_counter > (self.f * self.static_time)


def main():
    import os

    observations = np.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test_data.npy'))
    timestamps = observations[:, 0]
    observations = observations[:, 1:]

    # A, transition_covariance, C, observation_covariance = KalmanFilter.get_accelerometer_filter_matrices(200)
    #
    # initial_state_mean = np.zeros((9, ), 'float')
    # initial_state_covariance = np.ones((9, 9), 'float')
    #
    # kf = StaticDetectingPositionKalmanFilter(A, transition_covariance, C, observation_covariance)
    # kf.set_initial_state(initial_state_mean, initial_state_covariance)
    #
    # print("Kalman Filter")
    # t = time.time()
    # States = kf.filter(observations)
    # print("Time taken: {0} s".format(time.time() - t))

    kf = StaticDetectingPositionKalmanFilter(200, 0.025, 0.2)

    print("Static Kalman Filter")
    t = time.time()
    States, Static_State, G = kf.filter(observations)
    print("Time taken: {0} s".format(time.time() - t))

    try:
        # Draw estimates
        import matplotlib.pyplot as pl

        pl.figure()
        ax = pl.subplot2grid((4, 3), (0, 0), colspan=3)
        pl.plot(timestamps, np.array(States[:, 0]), 'r')
        pl.plot(timestamps, np.array(States[:, 1]), 'b')
        pl.plot(timestamps, np.array(States[:, 2]), 'y')

        ax = pl.subplot2grid((4, 3), (1, 0), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 3]), 'r')
        ax = pl.subplot2grid((4, 3), (1, 1), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 4]), 'b')
        ax = pl.subplot2grid((4, 3), (1, 2), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 5]), 'y')

        ax = pl.subplot2grid((4, 3), (2, 0), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 6]), 'r')
        ax = pl.subplot2grid((4, 3), (2, 1), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 7]), 'b')
        ax = pl.subplot2grid((4, 3), (2, 2), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 8]), 'y')

        ax = pl.subplot2grid((4, 3), (3, 0), colspan=23, sharex=ax)
        MASS = 1
        pl.plot(timestamps, np.sum(np.abs(MASS * States[:, :3] * States[:, 3:6]), axis=1))

        # ax = pl.subplot2grid((4, 3), (3, 0), colspan=2, sharex=ax)
        # pl.plot(timestamps, np.array(Static_State), 'r')
        # ax = pl.subplot2grid((4, 3), (3, 2), sharex=ax)
        # pl.plot(timestamps, np.sqrt(np.sum(observations ** 2, 1)), 'b')

        pl.show()
    except ImportError:
        pass


if __name__ == '__main__':
    main()
