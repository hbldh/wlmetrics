/**
 **************************************************************************************
 * @file    madgwick.c
 * @author  hbldh
 * @version 0.1
 * @date    2015-06-21
 * @brief   C extension.
 **************************************************************************************
 */

#include <Python.h>
#include "MadgwickAHRS.h"

static char Magdwick_AHRS_update_docs[] =
      "AHRS algorithm updateg\n\n"
      "Definition:\n"
      "  magdwick_AHRS_update(gx, gy, gz, ax, ay, az, mx, my, mz)\n\n"
      "Parameters::\n\n"
      "  data\n"
      "    Param docstring\n\n"
      "Return::\n\n"
      "  rvalue\n"
      "    The value result.\n\n";

static PyObject *Magdwick_AHRS_update_func(PyObject *self, PyObject *args)
{
    float gx, gy, gz;
    float ax, ay, az;
    float mx, my, mz;

    /* Parse the input.*/
    if (!PyArg_ParseTuple(args, "fffffffff", &gx, &gy, &gz, &ax, &ay, &az, &mx, &my, &mz))
        return NULL;

    MadgwickAHRSupdate(gx, gy, gz, ax, ay, az, mx, my, mz);
    return Py_BuildValue("(ffff)", q0, q1, q2, q3);
}

static char Magdwick_AHRS_update_IMU_docs[] =
      "Docstring\n\n"
      "Definition:\n"
      "  method_name(data)\n\n"
      "Parameters::\n\n"
      "  data\n"
      "    Param docstring\n\n"
      "Return::\n\n"
      "  rvalue\n"
      "    The value result.\n\n";

static PyObject *Magdwick_AHRS_update_IMU_func(PyObject *self, PyObject *args)
{
    float gx, gy, gz;
    float ax, ay, az;

    /* Parse the input.*/
    if (!PyArg_ParseTuple(args, "ffffff", &gx, &gy, &gz, &ax, &ay, &az))
        return NULL;

    MadgwickAHRSupdateIMU(gx, gy, gz, ax, ay, az);
    return Py_BuildValue("(ffff)", q0, q1, q2, q3);
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
