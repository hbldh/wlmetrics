# WLMetrics

A toolkit for handling data from IMU units when measuring movements during weight lifting.

Has primarily been tested with [PyBerryIMU](http://github.com/hbldh/pyberryimu) data. 

## Bundled code

This library includes bundled code from [x-io Technologies webpage]
(http://www.x-io.co.uk/open-source-imu-and-ahrs-algorithms/), namely the C implementations
of the [Madgwick AHRS filter algorithm](http://www.x-io.co.uk/res/doc/madgwick_internal_report.pdf) 
and the [Mahony AHRS filter algorithm](http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4608934). 

These have been modified slightly to make the C functions stateless and keep the states in the
corresponding Python object wrappers instead.


