/**
 **************************************************************************************
 * @file    madgwick.c
 * @author  hbldh
 * @version 0.1
 * @date    2015-06-21
 * @brief   C extension wrapping Madgwick filter methods for Python.
 **************************************************************************************
 */

#include <Python.h>
#include "MadgwickAHRS.h"

static char Magdwick_AHRS_update_docs[] =
      "AHRS algorithm update\n\n"
      "Definition:\n"
      "  magdwick_AHRS_update(gx, gy, gz, ax, ay, az, mx, my, mz)\n\n"
      "Parameters::\n\n"
      "  gx\n"
      "    Gyroscope X axis value.\n\n"
      "  gy\n"
      "    Gyroscope Y axis value.\n\n"
      "  gz\n"
      "    Gyroscope Z axis value.\n\n"
      "  ax\n"
      "    Accelerometer X axis value.\n\n"
      "  ay\n"
      "    Accelerometer Y axis value.\n\n"
      "  az\n"
      "    Accelerometer Z axis value.\n\n"
      "  gx\n"
      "    Magnetometer X axis value.\n\n"
      "  gy\n"
      "    Magnetometer Y axis value.\n\n"
      "  gz\n"
      "    Magnetometer Z axis value.\n\n"
      "Return::\n\n"
      "  tuple\n"
      "    The updated quaternion.\n\n";

static PyObject *Magdwick_AHRS_update_func(PyObject *self, PyObject *args)
{
    float gx, gy, gz;
    float ax, ay, az;
    float mx, my, mz;
    float freq;
    float q[4];

    /* Parse the input.*/
    if (!PyArg_ParseTuple(args, "ffffffffffffff", &gx, &gy, &gz, &ax, &ay, &az, &mx, &my, &mz, &freq, &q[0], &q[1], &q[2], &q[3]))
        return NULL;

    MadgwickAHRSupdate(gx, gy, gz, ax, ay, az, mx, my, mz, freq, q);
    return Py_BuildValue("(ffff)", q[0], q[1], q[2], q[3]);
}

static char Magdwick_AHRS_update_IMU_docs[] =
      "IMU algorithm update\n\n"
      "Definition:\n"
      "  magdwick_AHRS_update_IMU(gx, gy, gz, ax, ay, az)\n\n"
      "Parameters::\n\n"
      "  gx\n"
      "    Gyroscope X axis value.\n\n"
      "  gy\n"
      "    Gyroscope Y axis value.\n\n"
      "  gz\n"
      "    Gyroscope Z axis value.\n\n"
      "  ax\n"
      "    Accelerometer X axis value.\n\n"
      "  ay\n"
      "    Accelerometer Y axis value.\n\n"
      "  az\n"
      "    Accelerometer Z axis value.\n\n"
      "Return::\n\n"
      "  tuple\n"
      "    The updated quaternion.\n\n";

static PyObject *Magdwick_AHRS_update_IMU_func(PyObject *self, PyObject *args)
{
    float gx, gy, gz;
    float ax, ay, az;
    float freq;
    float q[4];

    /* Parse the input.*/
    if (!PyArg_ParseTuple(args, "fffffffffff", &gx, &gy, &gz, &ax, &ay, &az, &freq, &q[0], &q[1], &q[2], &q[3]))
        return NULL;

    MadgwickAHRSupdateIMU(gx, gy, gz, ax, ay, az, freq, q);
    return Py_BuildValue("(ffff)", q[0], q[1], q[2], q[3]);
}

static PyMethodDef madgwickMethods[] = {
    {"magdwick_AHRS_update", Magdwick_AHRS_update_func, METH_VARARGS, Magdwick_AHRS_update_docs},
    {"magdwick_AHRS_update_IMU", Magdwick_AHRS_update_IMU_func, METH_VARARGS, Magdwick_AHRS_update_IMU_docs},
     {NULL, NULL, 0, NULL} /* Sentinel */
};

PyMODINIT_FUNC initmadgwick(void)
{
    char * docstring = "Python C extension of Madgwick's Sensor Fusion algorithm.";
    (void) Py_InitModule3("madgwick", madgwickMethods, docstring);
}
