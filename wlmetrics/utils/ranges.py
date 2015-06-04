#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`ranges`
==================

.. module:: ranges
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-06-04, 15:12

"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from operator import itemgetter
from itertools import groupby
import numpy as np


def int_array_to_ranges(array):
    """Converts an monotonically increasing (or decreasing) array of integers into a
    list of index ranges with identical value.

    :param array: The array to segment.
    :type array: :py:class:`numpy.ndarray` or list
    :return: The list of ranges as index tuples.
    :rtype: list

    """
    diffs = np.where(np.diff(array))[0]
    if len(diffs) == 0:
        ranges = [(0, len(array))]
    elif len(diffs) == 1:
        ranges = [(0, diffs[0] + 1), (diffs[0] + 1, len(array))]
    else:
        ranges = [(x + 1, y + 1) for x, y in zip(diffs[:-1], diffs[1:])]
        ranges.insert(0, (0, ranges[0][0]))
        ranges.append((ranges[-1][1], len(array)))
    return ranges


def bool_array_to_ranges(array):
    """Converts a boolean array into a list of segments where it is ``True``

    :param array: A boolean array to segment.
    :type array: :py:class:`numpy.ndarray`
    :return: A list of tuples with start and stop index of the ranges.
    :rtype: list

    """
    ranges = []
    for k, g in groupby(enumerate(np.where(array > 0)[0]), lambda (i, x): i - x):
        group = map(itemgetter(1), g)
        ranges.append((group[0], group[-1]))
    return ranges
