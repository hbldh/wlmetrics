#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`kalman`
==================

.. module:: kalman
   :platform: Unix, Windows
   :synopsis:

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-05-30, 16:24

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import time

import numpy as np


class KalmanFilter(object):
    """A simple Kalman Filter implementation, straight from definition.

    N.B. that this filter is NOT an efficient implementation of a Kalman Filter,
    but included more as a first test to see what it might do to the BerryIMU data.

    Consider looking at the :py:module:`pykalman` module for a better implementation.

    """

    def __init__(self, transition_matrix, transition_covariance,
                 observation_matrix, observation_covariance):

        self.transition_matrix = transition_matrix
        self.transition_covariance = transition_covariance
        self.observation_matrix = observation_matrix
        self.observation_covariance = observation_covariance

        self.X = None
        self.P = None

    def set_initial_state(self, initial_state, initial_covariance):
        self.X = initial_state
        self.P = initial_covariance

    def filter(self, observations):
        states = []

        X = self.X
        P = self.P
        for observation in observations:
            X, P = self.kf_predict(X, P)
            X, P, K, IM, IS = self.kf_update(X, P, observation)
            states.append(X)

        return np.array(states)

    def kf_predict(self, X, P):
        # Predict New State, X_k = A * X_{k-1}
        X = self.transition_matrix.dot(X)
        # Predict New Covariance, P_k = A * P_{k-1} * A^T + Sigma_X
        P = self.transition_matrix.dot(P.dot(self.transition_matrix.T)) + \
            self.transition_covariance
        return X, P

    def kf_update(self, X, P, Y):
        # The Mean of predictive distribution of Y
        IM = self.observation_matrix.dot(X)
        # The Covariance or predictive mean of Y
        IS = self.observation_matrix.dot(P.dot(self.observation_matrix.T)) + \
            self.observation_covariance
        IS_inv = np.linalg.inv(IS)
        # Kalman Gain
        K = P.dot(self.observation_matrix.T.dot(IS_inv))
        # Prediction correction with observations.
        X = X + K.dot(Y - IM)
        # Covariance correction by Kalman gain and residual.
        P = P - K.dot(IS.dot(K.T))

        #LH = self.gauss_pdf(Y, IM, IS, IS_inv)
        return X, P, K, IM, IS, #LH

    def gauss_pdf(self, X, M, S, S_inv):
        if M.shape[0] == 1:
            DX = X - np.tile(M, X.shape()[1])
            E = 0.5 * sum(DX * (S_inv.dot(DX)), axis=0)
            E = (E + 0.5 * M.shape()[0] * np.log(2 * np.pi) +
                 0.5 * np.log(np.linalg.det(S)))
            P = np.exp(-E)
        elif X.shape[0] == 1:
            DX = np.tile(X, M.shape()[1]) - M
            E = 0.5 * sum(DX * (S_inv.dot(DX)), axis=0)
            E = (E + 0.5 * M.shape()[0] * np.log(2 * np.pi) +
                 0.5 * np.log(np.linalg.det(S)))
            P = np.exp(-E)
        else:
            DX = X - M
            E = 0.5 * DX.T.dot(S_inv.dot(DX))
            E = (E + 0.5 * M.shape[0] * np.log(2 * np.pi) +
                 0.5 * np.log(np.linalg.det(S)))
            P = np.exp(-E)
        return P, E

    @classmethod
    def get_accelerometer_filter_matrices(cls, data_freq):
        transition_matrix = np.eye(9)
        transition_matrix[[3, 4, 5], [0, 1, 2]] = 1 / data_freq
        transition_matrix[[6, 7, 8], [3, 4, 5]] = 1 / data_freq

        transition_covariance = np.eye(9) * 0.05

        observation_matrix = np.zeros((3, 9), 'float')
        observation_matrix[[0, 1, 2], [0, 1, 2]] = 1

        observation_covariance = np.eye(3)*2

        return transition_matrix, transition_covariance, observation_matrix, observation_covariance


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

    observations = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data.npy'))
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
        ax = pl.subplot2grid((4, 3), (0, 0))
        pl.plot(timestamps, np.array(G[:, 0]), 'r')
        pl.plot(timestamps, np.array(States[:, 0]), 'b')
        ax = pl.subplot2grid((4, 3), (0, 1), sharex=ax)
        pl.plot(timestamps, np.array(G[:, 1]), 'r')
        pl.plot(timestamps, np.array(States[:, 1]), 'b')
        ax = pl.subplot2grid((4, 3), (0, 2), sharex=ax)
        pl.plot(timestamps, np.array(G[:, 2]), 'r')
        pl.plot(timestamps, np.array(States[:, 2]), 'b')

        ax = pl.subplot2grid((4, 3), (1, 0), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 3]), 'r')
        ax = pl.subplot2grid((4, 3), (1, 1), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 4]), 'r')
        ax = pl.subplot2grid((4, 3), (1, 2), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 5]), 'r')

        ax = pl.subplot2grid((4, 3), (2, 0), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 6]), 'r')
        ax = pl.subplot2grid((4, 3), (2, 1), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 7]), 'r')
        ax = pl.subplot2grid((4, 3), (2, 2), sharex=ax)
        pl.plot(timestamps, np.array(States[:, 8]), 'r')

        ax = pl.subplot2grid((4, 3), (3, 0), colspan=2, sharex=ax)
        pl.plot(timestamps, np.array(Static_State), 'r')
        ax = pl.subplot2grid((4, 3), (3, 2), sharex=ax)
        pl.plot(timestamps, np.sqrt(np.sum(observations**2, 1)), 'b')

        pl.show()
    except ImportError:
        pass

if __name__ == '__main__':
    main()
