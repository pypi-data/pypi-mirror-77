#define PY_SSIZE_T_CLEAN

#include <Python.h>

static PyObject *testSystem(PyObject *self, PyObject *args) {
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return PyLong_FromLong(sts);
}

static PyMethodDef SpamMethods[] = {
        {"system", testSystem, METH_VARARGS,
                "Execute a shell command."},
        {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef testModule = {
        PyModuleDef_HEAD_INIT,
        "testModule",   /* name of module */
        NULL, /* module documentation, may be NULL */
        -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
        SpamMethods
};

PyMODINIT_FUNC
PyInit_testModule(void) {
    return PyModule_Create(&testModule);
}
