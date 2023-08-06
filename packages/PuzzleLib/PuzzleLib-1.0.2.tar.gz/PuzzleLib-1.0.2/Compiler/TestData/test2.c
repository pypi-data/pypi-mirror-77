
#include <Python.h>
#include "header.h"


PyObject *hello(PyObject *self, PyObject *args)
{
	(void)self, (void)args;

	puts("Hello, Build!");
	fflush(stdout);

	Py_RETURN_NONE;
}
