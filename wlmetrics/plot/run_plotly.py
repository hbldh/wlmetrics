#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`run_plotly`
==================

.. module:: run_plotly
   :platform: Unix, Windows
   :synopsis:

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-08-17

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

# Assumes credentials file exists.
import plotly.plotly as py
import plotly.graph_objs as pygraph
from pyberryimu.client import BerryIMUClient
from pyberryimu.calibration.standard import StandardCalibration

def plot_data():
    c = py.get_credentials()
    trace1 = pygraph.Scatter(
        x=[], y=[],
        mode='lines',
        line=pygraph.Line(color='rgba(31,119,180,0.15)'),
        stream=dict(token=c.get('stream_ids')[0], maxpoints=100))
    trace2 = pygraph.Scatter(
        x=[], y=[],
        mode='lines',
        line=pygraph.Line(color='rgba(180,119,31,0.15)'),
        stream=dict(token=c.get('stream_ids')[1], maxpoints=100))
    trace3 = pygraph.Scatter(
        x=[], y=[],
        mode='lines',
        line=pygraph.Line(color='rgba(119,180,31,0.15)'),
        stream=dict(token=c.get('stream_ids')[2], maxpoints=100))

    data = pygraph.Data([trace1, trace2, trace3])
    layout = pygraph.Layout(
        title='Streaming PyBerryIMU Data'
    )
    fig = pygraph.Figure(data=data, layout=layout)
    print(py.plot(fig, filename='PyBerryIMU'))
    s_x = py.Stream(c.get('stream_ids')[0])
    s_y = py.Stream(c.get('stream_ids')[1])
    s_z = py.Stream(c.get('stream_ids')[2])
    s_x.open()
    s_y.open()
    s_z.open()

    with BerryIMUClient() as c:
        c.calibration_object = StandardCalibration.load()
        t_start = c.timestamp
        while (c.timestamp - t_start) < 60:
            t = c.timestamp - t_start
            acc = c.read_accelerometer()
            s_x.write(dict(x=t, y=acc[0]))
            s_y.write(dict(x=t, y=acc[1]))
            s_z.write(dict(x=t, y=acc[2]))
    s_x.close()
    s_y.close()
    s_z.close()


if __name__ == '__main__':
    plot_data()