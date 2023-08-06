
#include <Python.h>
#include "header.h"


static PyMethodDef methods[] = {
	{"hello", hello, METH_NOARGS, NULL},
	{NULL, NULL, 0, NULL}
};


static PyModuleDef mod = {
	PyModuleDef_HEAD_INIT,
	.m_name = "test",
	.m_methods = methods
};


PyMODINIT_FUNC PyInit_test(void)
{
	return PyModule_Create(&mod);
}
