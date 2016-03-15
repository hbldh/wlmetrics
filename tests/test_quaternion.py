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
import itertools

import pytest
import numpy as np

from wlmetrics.quaternion import Quaternion


def _reference_multiply(q1, q2):
    return Quaternion(
        [q1.w * q2.w - q1.imag.dot(q2.imag), ] +
        (q1.w * q2.imag + q2.w * q1.imag + np.cross(q1.imag, q2.imag)).tolist())


@pytest.mark.parametrize('q1,q2', itertools.combinations_with_replacement([Quaternion.i(), Quaternion.j(), Quaternion.k()], 2))
def test_add_1(q1, q2):
    np.testing.assert_allclose((q1 + q2).to_array() - (q1.to_array() + q2.to_array()), 0.0)


def test_add_2():
    q1 = Quaternion(np.random.rand(4))
    q2 = Quaternion(np.random.rand(4))
    np.testing.assert_allclose((q1 + q2).to_array() - (q1.to_array() + q2.to_array()), 0.0)


@pytest.mark.parametrize('q1,q2', itertools.combinations_with_replacement([Quaternion.i(), Quaternion.j(), Quaternion.k()], 2))
def test_sub_1(q1, q2):
    np.testing.assert_allclose((q1 - q2).to_array() - (q1.to_array() - q2.to_array()), 0.0)


def test_sub_2():
    q1 = Quaternion(np.random.rand(4))
    q2 = Quaternion(np.random.rand(4))
    np.testing.assert_allclose((q1 - q2).to_array() - (q1.to_array() - q2.to_array()), 0.0)


@pytest.mark.parametrize('q1,q2', itertools.combinations_with_replacement([Quaternion.i(), Quaternion.j(), Quaternion.k()], 2))
def test_multiply_1(q1, q2):
    np.testing.assert_allclose((_reference_multiply(q1, q2) - (q1 * q2)).to_array(), 0.0)
    np.testing.assert_allclose(_reference_multiply(q1, q2).to_array() - (q1 * q2).to_array(), 0.0)


def test_multiply_2():
    quat_1 = Quaternion(np.random.rand(4))
    quat_2 = Quaternion(np.random.rand(4))

    np.testing.assert_allclose((_reference_multiply(quat_1, quat_2) - (quat_1 * quat_2)).to_array(), 0.0, atol=1e-15)
    np.testing.assert_allclose(_reference_multiply(quat_1, quat_2).to_array() - (quat_1 * quat_2).to_array(), 0.0, atol=1e-15)


@pytest.mark.parametrize('q', [Quaternion.i(), Quaternion.j(), Quaternion.k()])
def test_norm_1(q):
    np.testing.assert_allclose(q.norm(), 1.0)


def test_norm_2():
    x = np.random.rand(4)
    q = Quaternion(x)
    np.testing.assert_allclose(q.norm(), np.sqrt(np.sum(x ** 2)))


def test_normalize():
    x = np.random.rand(4)
    q = Quaternion(x)
    q.normalize()
    norm_post = q.norm()
    np.testing.assert_allclose(norm_post, 1.0)


def test_nomalize_untouched_array():
    q = Quaternion(np.random.rand(4))
    q_arr_pre = q.to_array()
    q_arr_pre_pre = copy.deepcopy(q_arr_pre)
    q.normalize()
    np.testing.assert_allclose(q_arr_pre, q_arr_pre_pre)


def test_conjugate():
    q = Quaternion(np.random.rand(4))
    q.normalize()
    np.testing.assert_allclose((q.conjugate() - Quaternion([q.w, -q.x, -q.y, -q.z])).to_array(), 0.0)

