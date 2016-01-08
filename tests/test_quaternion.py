#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`test_quaternion`
==================

.. module:: test_quaternion
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-06-04, 09:45

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import copy

import numpy as np

from wlmetrics.quaternion import Quaternion


class TestSuiteQuaternion(object):
    """Test Suite for Quaternion class."""

    def setUp(self):
        """No setup as of right now."""
        pass

    @staticmethod
    def _reference_multiply(q1, q2):
        return Quaternion(
            [q1.w * q2.w - q1.imag.dot(q2.imag), ] +
            (q1.w * q2.imag + q2.w * q1.imag + np.cross(q1.imag, q2.imag)).tolist())

    def test_add_1(self):
        def test_fcn(x, y):
            np.testing.assert_allclose((x + y).to_array() - (x.to_array() + y.to_array()), 0.0)
        for fcn_1 in [Quaternion.i, Quaternion.j, Quaternion.k]:
            for fcn_2 in [Quaternion.i, Quaternion.j, Quaternion.k]:
                yield test_fcn, fcn_1(), fcn_2()

    def test_add_2(self):
        q1 = Quaternion(np.random.rand(4))
        q2 = Quaternion(np.random.rand(4))
        np.testing.assert_allclose((q1 + q2).to_array() - (q1.to_array() + q2.to_array()), 0.0)

    def test_sub_1(self):
        def test_fcn(x, y):
            np.testing.assert_allclose((x - y).to_array() - (x.to_array() - y.to_array()), 0.0)

        for fcn_1 in [Quaternion.i, Quaternion.j, Quaternion.k]:
            for fcn_2 in [Quaternion.i, Quaternion.j, Quaternion.k]:
                yield test_fcn, fcn_1(), fcn_2()

    def test_sub_2(self):
        q1 = Quaternion(np.random.rand(4))
        q2 = Quaternion(np.random.rand(4))
        np.testing.assert_allclose((q1 - q2).to_array() - (q1.to_array() - q2.to_array()), 0.0)

    def test_multiply_1(self):

        def test_fcn(q1, q2):
            np.testing.assert_allclose((self._reference_multiply(q1, q2) - (q1 * q2)).to_array(), 0.0)
            np.testing.assert_allclose(self._reference_multiply(q1, q2).to_array() - (q1 * q2).to_array(), 0.0)

        for fcn_1 in [Quaternion.i, Quaternion.j, Quaternion.k]:
            for fcn_2 in [Quaternion.i, Quaternion.j, Quaternion.k]:
                yield test_fcn, fcn_1(), fcn_2()

    def test_multiply_2(self):
        quat_1 = Quaternion(np.random.rand(4))
        quat_2 = Quaternion(np.random.rand(4))

        np.testing.assert_allclose((self._reference_multiply(quat_1, quat_2) - (quat_1 * quat_2)).to_array(), 0.0, atol=1e-16)
        np.testing.assert_allclose(self._reference_multiply(quat_1, quat_2).to_array() - (quat_1 * quat_2).to_array(), 0.0, atol=1e-16)

    def test_norm_1(self):
        def test_fcn(q):
            np.testing.assert_allclose(q.norm(), 1.0)
        for fcn_1 in [Quaternion.i, Quaternion.j, Quaternion.k]:
            yield test_fcn, fcn_1()

    def test_norm_2(self):
        x = np.random.rand(4)
        q = Quaternion(x)
        np.testing.assert_allclose(q.norm(), np.sqrt(np.sum(x ** 2)))

    def test_normalize(self):
        x = np.random.rand(4)
        q = Quaternion(x)
        q.normalize()
        norm_post = q.norm()
        np.testing.assert_allclose(norm_post, 1.0)

    def test_nomalize_untouched_array(self):
        q = Quaternion(np.random.rand(4))
        q_arr_pre = q.to_array()
        q_arr_pre_pre = copy.deepcopy(q_arr_pre)
        q.normalize()

        np.testing.assert_allclose(q_arr_pre, q_arr_pre_pre)

    def test_conjugate(self):
        q = Quaternion(np.random.rand(4))
        q.normalize()
        np.testing.assert_allclose((q.conjugate() - Quaternion([q.w, -q.x, -q.y, -q.z])).to_array(), 0.0)

