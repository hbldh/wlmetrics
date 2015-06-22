/**
 **************************************************************************************
 * @file    mahony.c
 * @author  hbldh
 * @version 0.1
 * @date    2015-06-21
 * @brief   C extension wrapping Mahony filter methods for Python.
 **************************************************************************************
 */

#include <Python.h>
#include "MahonyAHRS.h"

static char Mahony_AHRS_update_docs[] =
      "AHRS algorithm update\n\n"
      "Definition:\n"
      "  Mahony_AHRS_update(gx, gy, gz, ax, ay, az, mx, my, mz)\n\n"
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

static PyObject *Mahony_AHRS_update_func(PyObject *self, PyObject *args)
{
    float gx, gy, gz;
    float ax, ay, az;
    float mx, my, mz;

    /* Parse the input.*/
    if (!PyArg_ParseTuple(args, "fffffffff", &gx, &gy, &gz, &ax, &ay, &az, &mx, &my, &mz))
        return NULL;

    MahonyAHRSupdate(gx, gy, gz, ax, ay, az, mx, my, mz);
    return Py_BuildValue("(ffff)", q0, q1, q2, q3);
}

static char Mahony_AHRS_update_IMU_docs[] =
      "IMU algorithm update\n\n"
      "Definition:\n"
      "  Mahony_AHRS_update_IMU(gx, gy, gz, ax, ay, az)\n\n"
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

static PyObject *Mahony_AHRS_update_IMU_func(PyObject *self, PyObject *args)
{
    float gx, gy, gz;
    float ax, ay, az;

    /* Parse the input.*/
    if (!PyArg_ParseTuple(args, "ffffff", &gx, &gy, &gz, &ax, &ay, &az))
        return NULL;

    MahonyAHRSupdateIMU(gx, gy, gz, ax, ay, az);
    return Py_BuildValue("(ffff)", q0, q1, q2, q3);
}

static PyMethodDef mahonyMethods[] = {
    {"Mahony_AHRS_update", Mahony_AHRS_update_func, METH_VARARGS, Mahony_AHRS_update_docs},
    {"Mahony_AHRS_update_IMU", Mahony_AHRS_update_IMU_func, METH_VARARGS, Mahony_AHRS_update_IMU_docs},
     {NULL, NULL, 0, NULL} /* Sentinel */
};

PyMODINIT_FUNC initmahony(void)
{
    char * docstring = "Python C extension of Mahony's AHRS Filter";
    (void) Py_InitModule3("mahony", mahonyMethods, docstring);
}
