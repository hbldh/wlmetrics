#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`quaternion`
==================

.. module:: quaternion
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-06-03, 21:55

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np


class Quaternion(object):
    """A simple quaternion class."""
    
    def __init__(self, values):
        """Constructor for Quaternion"""
        if len(values) != 4:
            raise ValueError("Quaternion init vector must be of length 4.")
        self._elements = np.array(values, 'float')

    @classmethod
    def i(cls):
        return cls([0, 1, 0, 0])

    @classmethod
    def j(cls):
        return cls([0, 0, 1, 0])

    @classmethod
    def k(cls):
        return cls([0, 0, 0, 1])

    def __repr__(self):
        return "{0} + {1}i + {2}j + {3}k".format(*self._elements)

    def __str__(self):
        return repr(self)

    def __iter__(self):
        for value in self._elements:
            yield value

    def __getitem__(self, item):
        return self._elements[item]

    def __add__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(self.to_array() + other.to_array())
        elif isinstance(other, (int, float)):
            return Quaternion(self._elements + other)
        else:
            raise NotImplementedError("Cannot add Quaternion with type {0}".format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(self.to_array() - other.to_array())
        elif isinstance(other, (int, float)):
            return Quaternion(self._elements - other)
        else:
            raise NotImplementedError("Cannot subtract Quaternion with type {0}".format(type(other)))

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion([self.w * other.w - (self.x * other.x) - (self.y * other.y) - (self.z * other.z),
                               self.w * other.x + self.x * other.w + self.y * other.z - (self.z * other.y),
                               self.w * other.y - (self.x * other.z) + self.y * other.w + self.z * other.x,
                               self.w * other.z + self.x * other.y - (self.y * other.x) + self.z * other.w])
        elif isinstance(other, (int, float)):
            return Quaternion(self._elements * other)
        else:
            raise NotImplementedError("Cannot multiply Quaternion with type {0}".format(type(other)))

    def __div__(self, other):
        if isinstance(other, Quaternion):
            raise NotImplementedError('TBD...')
        elif isinstance(other, (int, float)):
            return Quaternion(self._elements / other)
        else:
            raise NotImplementedError("Cannot multiply Quaternion with type {0}".format(type(other)))

    def __abs__(self):
        return self.norm()

    @property
    def w(self):
        return self._elements[0]

    @property
    def x(self):
        return self._elements[1]

    @property
    def y(self):
        return self._elements[2]

    @property
    def z(self):
        return self._elements[3]

    @property
    def real(self):
        return self._elements[0]

    @property
    def imag(self):
        return self._elements[1:]

    def to_array(self):
        return self._elements.copy()

    def conjugate(self):
        return Quaternion([self.w, -self.x, -self.y, -self.z])

    def norm(self):
        return np.linalg.norm(self._elements)

    def normalize(self):
        self._elements /= self.norm()


