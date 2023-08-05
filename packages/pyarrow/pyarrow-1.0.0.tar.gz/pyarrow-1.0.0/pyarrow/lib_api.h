/* Generated by Cython 0.29.21 */

#ifndef __PYX_HAVE_API__pyarrow__lib
#define __PYX_HAVE_API__pyarrow__lib
#ifdef __MINGW64__
#define MS_WIN64
#endif
#include "Python.h"
#include "lib.h"

static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_scalar)(std::shared_ptr< arrow::Scalar>  const &) = 0;
#define pyarrow_wrap_scalar __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_scalar
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_array)(std::shared_ptr< arrow::Array>  const &) = 0;
#define pyarrow_wrap_array __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_array
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_chunked_array)(std::shared_ptr< arrow::ChunkedArray>  const &) = 0;
#define pyarrow_wrap_chunked_array __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_chunked_array
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_batch)(std::shared_ptr< arrow::RecordBatch>  const &) = 0;
#define pyarrow_wrap_batch __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_batch
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_buffer)(std::shared_ptr< arrow::Buffer>  const &) = 0;
#define pyarrow_wrap_buffer __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_buffer
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_data_type)(std::shared_ptr< arrow::DataType>  const &) = 0;
#define pyarrow_wrap_data_type __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_data_type
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_field)(std::shared_ptr< arrow::Field>  const &) = 0;
#define pyarrow_wrap_field __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_field
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_resizable_buffer)(std::shared_ptr< arrow::ResizableBuffer>  const &) = 0;
#define pyarrow_wrap_resizable_buffer __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_resizable_buffer
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_schema)(std::shared_ptr< arrow::Schema>  const &) = 0;
#define pyarrow_wrap_schema __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_schema
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_table)(std::shared_ptr< arrow::Table>  const &) = 0;
#define pyarrow_wrap_table __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_table
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_tensor)(std::shared_ptr< arrow::Tensor>  const &) = 0;
#define pyarrow_wrap_tensor __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_tensor
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_coo_tensor)(std::shared_ptr< arrow::SparseCOOTensor>  const &) = 0;
#define pyarrow_wrap_sparse_coo_tensor __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_coo_tensor
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_csr_matrix)(std::shared_ptr< arrow::SparseCSRMatrix>  const &) = 0;
#define pyarrow_wrap_sparse_csr_matrix __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_csr_matrix
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_csc_matrix)(std::shared_ptr< arrow::SparseCSCMatrix>  const &) = 0;
#define pyarrow_wrap_sparse_csc_matrix __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_csc_matrix
static PyObject *(*__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_csf_tensor)(std::shared_ptr< arrow::SparseCSFTensor>  const &) = 0;
#define pyarrow_wrap_sparse_csf_tensor __pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_csf_tensor
static std::shared_ptr< arrow::Scalar>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_scalar)(PyObject *) = 0;
#define pyarrow_unwrap_scalar __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_scalar
static std::shared_ptr< arrow::Array>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_array)(PyObject *) = 0;
#define pyarrow_unwrap_array __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_array
static std::shared_ptr< arrow::ChunkedArray>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_chunked_array)(PyObject *) = 0;
#define pyarrow_unwrap_chunked_array __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_chunked_array
static std::shared_ptr< arrow::RecordBatch>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_batch)(PyObject *) = 0;
#define pyarrow_unwrap_batch __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_batch
static std::shared_ptr< arrow::Buffer>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_buffer)(PyObject *) = 0;
#define pyarrow_unwrap_buffer __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_buffer
static std::shared_ptr< arrow::DataType>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_data_type)(PyObject *) = 0;
#define pyarrow_unwrap_data_type __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_data_type
static std::shared_ptr< arrow::Field>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_field)(PyObject *) = 0;
#define pyarrow_unwrap_field __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_field
static std::shared_ptr< arrow::Schema>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_schema)(PyObject *) = 0;
#define pyarrow_unwrap_schema __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_schema
static std::shared_ptr< arrow::Table>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_table)(PyObject *) = 0;
#define pyarrow_unwrap_table __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_table
static std::shared_ptr< arrow::Tensor>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_tensor)(PyObject *) = 0;
#define pyarrow_unwrap_tensor __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_tensor
static std::shared_ptr< arrow::SparseCOOTensor>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_coo_tensor)(PyObject *) = 0;
#define pyarrow_unwrap_sparse_coo_tensor __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_coo_tensor
static std::shared_ptr< arrow::SparseCSRMatrix>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_csr_matrix)(PyObject *) = 0;
#define pyarrow_unwrap_sparse_csr_matrix __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_csr_matrix
static std::shared_ptr< arrow::SparseCSCMatrix>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_csc_matrix)(PyObject *) = 0;
#define pyarrow_unwrap_sparse_csc_matrix __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_csc_matrix
static std::shared_ptr< arrow::SparseCSFTensor>  (*__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_csf_tensor)(PyObject *) = 0;
#define pyarrow_unwrap_sparse_csf_tensor __pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_csf_tensor
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_internal_check_status)(arrow::Status const &) = 0;
#define pyarrow_internal_check_status __pyx_api_f_7pyarrow_3lib_pyarrow_internal_check_status
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_buffer)(PyObject *) = 0;
#define pyarrow_is_buffer __pyx_api_f_7pyarrow_3lib_pyarrow_is_buffer
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_data_type)(PyObject *) = 0;
#define pyarrow_is_data_type __pyx_api_f_7pyarrow_3lib_pyarrow_is_data_type
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_metadata)(PyObject *) = 0;
#define pyarrow_is_metadata __pyx_api_f_7pyarrow_3lib_pyarrow_is_metadata
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_field)(PyObject *) = 0;
#define pyarrow_is_field __pyx_api_f_7pyarrow_3lib_pyarrow_is_field
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_schema)(PyObject *) = 0;
#define pyarrow_is_schema __pyx_api_f_7pyarrow_3lib_pyarrow_is_schema
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_array)(PyObject *) = 0;
#define pyarrow_is_array __pyx_api_f_7pyarrow_3lib_pyarrow_is_array
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_chunked_array)(PyObject *) = 0;
#define pyarrow_is_chunked_array __pyx_api_f_7pyarrow_3lib_pyarrow_is_chunked_array
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_scalar)(PyObject *) = 0;
#define pyarrow_is_scalar __pyx_api_f_7pyarrow_3lib_pyarrow_is_scalar
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_tensor)(PyObject *) = 0;
#define pyarrow_is_tensor __pyx_api_f_7pyarrow_3lib_pyarrow_is_tensor
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_coo_tensor)(PyObject *) = 0;
#define pyarrow_is_sparse_coo_tensor __pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_coo_tensor
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_csr_matrix)(PyObject *) = 0;
#define pyarrow_is_sparse_csr_matrix __pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_csr_matrix
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_csc_matrix)(PyObject *) = 0;
#define pyarrow_is_sparse_csc_matrix __pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_csc_matrix
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_csf_tensor)(PyObject *) = 0;
#define pyarrow_is_sparse_csf_tensor __pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_csf_tensor
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_table)(PyObject *) = 0;
#define pyarrow_is_table __pyx_api_f_7pyarrow_3lib_pyarrow_is_table
static int (*__pyx_api_f_7pyarrow_3lib_pyarrow_is_batch)(PyObject *) = 0;
#define pyarrow_is_batch __pyx_api_f_7pyarrow_3lib_pyarrow_is_batch
#if !defined(__Pyx_PyIdentifier_FromString)
#if PY_MAJOR_VERSION < 3
  #define __Pyx_PyIdentifier_FromString(s) PyString_FromString(s)
#else
  #define __Pyx_PyIdentifier_FromString(s) PyUnicode_FromString(s)
#endif
#endif

#ifndef __PYX_HAVE_RT_ImportFunction
#define __PYX_HAVE_RT_ImportFunction
static int __Pyx_ImportFunction(PyObject *module, const char *funcname, void (**f)(void), const char *sig) {
    PyObject *d = 0;
    PyObject *cobj = 0;
    union {
        void (*fp)(void);
        void *p;
    } tmp;
    d = PyObject_GetAttrString(module, (char *)"__pyx_capi__");
    if (!d)
        goto bad;
    cobj = PyDict_GetItemString(d, funcname);
    if (!cobj) {
        PyErr_Format(PyExc_ImportError,
            "%.200s does not export expected C function %.200s",
                PyModule_GetName(module), funcname);
        goto bad;
    }
#if PY_VERSION_HEX >= 0x02070000
    if (!PyCapsule_IsValid(cobj, sig)) {
        PyErr_Format(PyExc_TypeError,
            "C function %.200s.%.200s has wrong signature (expected %.500s, got %.500s)",
             PyModule_GetName(module), funcname, sig, PyCapsule_GetName(cobj));
        goto bad;
    }
    tmp.p = PyCapsule_GetPointer(cobj, sig);
#else
    {const char *desc, *s1, *s2;
    desc = (const char *)PyCObject_GetDesc(cobj);
    if (!desc)
        goto bad;
    s1 = desc; s2 = sig;
    while (*s1 != '\0' && *s1 == *s2) { s1++; s2++; }
    if (*s1 != *s2) {
        PyErr_Format(PyExc_TypeError,
            "C function %.200s.%.200s has wrong signature (expected %.500s, got %.500s)",
             PyModule_GetName(module), funcname, sig, desc);
        goto bad;
    }
    tmp.p = PyCObject_AsVoidPtr(cobj);}
#endif
    *f = tmp.fp;
    if (!(*f))
        goto bad;
    Py_DECREF(d);
    return 0;
bad:
    Py_XDECREF(d);
    return -1;
}
#endif


static int import_pyarrow__lib(void) {
  PyObject *module = 0;
  module = PyImport_ImportModule("pyarrow.lib");
  if (!module) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_scalar", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_scalar, "PyObject *(std::shared_ptr< arrow::Scalar>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_array", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_array, "PyObject *(std::shared_ptr< arrow::Array>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_chunked_array", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_chunked_array, "PyObject *(std::shared_ptr< arrow::ChunkedArray>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_batch", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_batch, "PyObject *(std::shared_ptr< arrow::RecordBatch>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_buffer", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_buffer, "PyObject *(std::shared_ptr< arrow::Buffer>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_data_type", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_data_type, "PyObject *(std::shared_ptr< arrow::DataType>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_field", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_field, "PyObject *(std::shared_ptr< arrow::Field>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_resizable_buffer", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_resizable_buffer, "PyObject *(std::shared_ptr< arrow::ResizableBuffer>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_schema", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_schema, "PyObject *(std::shared_ptr< arrow::Schema>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_table", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_table, "PyObject *(std::shared_ptr< arrow::Table>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_tensor", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_tensor, "PyObject *(std::shared_ptr< arrow::Tensor>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_sparse_coo_tensor", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_coo_tensor, "PyObject *(std::shared_ptr< arrow::SparseCOOTensor>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_sparse_csr_matrix", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_csr_matrix, "PyObject *(std::shared_ptr< arrow::SparseCSRMatrix>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_sparse_csc_matrix", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_csc_matrix, "PyObject *(std::shared_ptr< arrow::SparseCSCMatrix>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_wrap_sparse_csf_tensor", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_wrap_sparse_csf_tensor, "PyObject *(std::shared_ptr< arrow::SparseCSFTensor>  const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_scalar", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_scalar, "std::shared_ptr< arrow::Scalar>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_array", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_array, "std::shared_ptr< arrow::Array>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_chunked_array", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_chunked_array, "std::shared_ptr< arrow::ChunkedArray>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_batch", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_batch, "std::shared_ptr< arrow::RecordBatch>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_buffer", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_buffer, "std::shared_ptr< arrow::Buffer>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_data_type", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_data_type, "std::shared_ptr< arrow::DataType>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_field", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_field, "std::shared_ptr< arrow::Field>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_schema", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_schema, "std::shared_ptr< arrow::Schema>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_table", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_table, "std::shared_ptr< arrow::Table>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_tensor", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_tensor, "std::shared_ptr< arrow::Tensor>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_sparse_coo_tensor", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_coo_tensor, "std::shared_ptr< arrow::SparseCOOTensor>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_sparse_csr_matrix", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_csr_matrix, "std::shared_ptr< arrow::SparseCSRMatrix>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_sparse_csc_matrix", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_csc_matrix, "std::shared_ptr< arrow::SparseCSCMatrix>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_unwrap_sparse_csf_tensor", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_unwrap_sparse_csf_tensor, "std::shared_ptr< arrow::SparseCSFTensor>  (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_internal_check_status", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_internal_check_status, "int (arrow::Status const &)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_buffer", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_buffer, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_data_type", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_data_type, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_metadata", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_metadata, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_field", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_field, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_schema", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_schema, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_array", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_array, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_chunked_array", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_chunked_array, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_scalar", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_scalar, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_tensor", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_tensor, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_sparse_coo_tensor", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_coo_tensor, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_sparse_csr_matrix", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_csr_matrix, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_sparse_csc_matrix", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_csc_matrix, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_sparse_csf_tensor", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_sparse_csf_tensor, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_table", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_table, "int (PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyarrow_is_batch", (void (**)(void))&__pyx_api_f_7pyarrow_3lib_pyarrow_is_batch, "int (PyObject *)") < 0) goto bad;
  Py_DECREF(module); module = 0;
  return 0;
  bad:
  Py_XDECREF(module);
  return -1;
}

#endif /* !__PYX_HAVE_API__pyarrow__lib */
