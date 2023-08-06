/* 
# Copyright (c) 2010-2020 Andrew Dalke Scientific, AB (Sweden)
#
# All chemfp 1.x software is distributed with the following license:
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

*/
#include <Python.h>

#include "chemfp.h"
#include "chemfp_internal.h"
#include "pysearch_results.h"

static PyObject *
version(PyObject *self, PyObject *args) {
  UNUSED(self);
  UNUSED(args);

  return PyString_FromString(chemfp_version());
}


/* Slightly renamed so it won't share the same name as strerror(3) */
static PyObject *
strerror_(PyObject *self, PyObject *args) {
  int err;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "i:strerror", &err))
    return NULL;
  return PyString_FromString(chemfp_strerror(err));
}

/*************** Hex fingerprint operations  *************/

static int
bad_hex_string(int hex_size) {
  if (hex_size % 2 != 0) {
    PyErr_SetString(PyExc_ValueError, "hex string length must be a multiple of 2");
    return 1;
  }
  return 0;
}

static int
bad_hex_pair(int hex_size1, int hex_size2) {
  if (hex_size1 != hex_size2) {
    PyErr_SetString(PyExc_ValueError,
                    "hex fingerprints must have the same length");
    return 1;
  }
  return bad_hex_string(hex_size1);
}

static PyObject *
hex_isvalid(PyObject *self, PyObject *args) {
  char *s;
  int len;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#:hex_isvalid", &s, &len))
    return NULL;
  return PyInt_FromLong(chemfp_hex_isvalid(len, s));
}

static PyObject *
hex_popcount(PyObject *self, PyObject *args) {
  char *s;
  int len;
  long long popcount;
  PyObject *return_value = NULL;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#:hex_popcount", &s, &len)) {
    goto exit;
  }
  
  if (bad_hex_string(len)) {
    goto exit;
  }
  if (!len) {
    popcount = 0;
  } else {
    popcount = chemfp_hex_popcount(len, s);
    if (popcount == -1) {
      PyErr_SetString(PyExc_ValueError,
                      "hex fingerprint contains a non-hex character");
      goto exit;
    }
  }
  return_value = PyInt_FromLong((long) popcount);
  
 exit:
  return return_value;
}

static PyObject *
hex_intersect_popcount(PyObject *self, PyObject *args) {
  char *s1, *s2;
  int len1, len2;
  long long popcount;
  PyObject *return_value = NULL;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:hex_intersect_popcount", &s1, &len1, &s2, &len2)) {
    goto exit;
  }
  if (bad_hex_pair(len1, len2)) {
    goto exit;
  }
  if (!len1) {
    popcount = 0;
  } else {
    popcount = chemfp_hex_intersect_popcount(len1, s1, s2);
    if (popcount == -1) {
      PyErr_SetString(PyExc_ValueError,
                      "one of the hex fingerprints contains a non-hex character");
      goto exit;
    }
  }
  return_value = PyInt_FromLong((long) popcount);
  
 exit:
  return return_value;
}

static PyObject *
hex_tanimoto(PyObject *self, PyObject *args) {
  char *s1, *s2;
  int len1, len2;
  double score;
  UNUSED(self);
  PyObject *return_value = NULL;

  if (!PyArg_ParseTuple(args, "s#s#:hex_tanimoto", &s1, &len1, &s2, &len2)) {
    goto exit;
  }

  if (bad_hex_pair(len1, len2)) {
    goto exit;
  }
  score = chemfp_hex_tanimoto(len1, s1, s2);
  if (score == -1.0) {
      PyErr_SetString(PyExc_ValueError,
                      "one of the hex fingerprints contains a non-hex character");
      goto exit;
  }
  return_value = PyFloat_FromDouble(score);

 exit:
  return return_value;
}

int
bad_tversky(double alpha, double beta) {
  if (alpha < 0.0 || alpha > 100.0) {
    PyErr_SetString(PyExc_ValueError, "alpha must be between 0.0 and 100.0, inclusive");
    return 1;
  }
  if (beta < 0.0 || beta > 100.0) {
    PyErr_SetString(PyExc_ValueError, "beta must be between 0.0 and 100.0, inclusive");
    return 1;
  }
  /* Hmm. Perhaps this is overkill. */
  if (alpha != alpha) {
    PyErr_SetString(PyExc_ValueError, "alpha must not be a NaN");
    return 1;
  } 
  if (beta != beta) {
    PyErr_SetString(PyExc_ValueError, "beta must not be a NaN");
    return 1;
  } 
  return 0;
}


static PyObject *
hex_tversky(PyObject *self, PyObject *args) {
  char *s1, *s2;
  int len1, len2;
  double alpha=1.0, beta=1.0;
  double score;
  UNUSED(self);
  PyObject *return_value = NULL;

  if (!PyArg_ParseTuple(args, "s#s#|dd:hex_tversky",
                        &s1, &len1, &s2, &len2, &alpha, &beta)) {
    goto exit;
  }

  if (bad_hex_pair(len1, len2) || bad_tversky(alpha, beta)) {
    goto exit;
  }
  score = chemfp_hex_tversky(len1, s1, s2, alpha, beta);
  if (score == -1.0) {
      PyErr_SetString(PyExc_ValueError,
                      "one of the hex fingerprints contains a non-hex character");
      goto exit;
  }
  return_value = PyFloat_FromDouble(score);
  
 exit:
  return return_value;
}


static PyObject *
hex_contains(PyObject *self, PyObject *args) {
  char *s1, *s2;
  int len1, len2;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:hex_contains", &s1, &len1, &s2, &len2))
    return NULL;
  if (len1 != len2) {
    PyErr_SetString(PyExc_ValueError,
                    "hex fingerprints must have the same length");
    return NULL;
  }
  return PyInt_FromLong((long) chemfp_hex_contains(len1, s1, s2));
}

static PyObject *
hex_contains_bit(PyObject *self, PyObject *args) {
  char *s;
  int len;
  long bitno;
  PyObject *return_value = NULL;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#l:hex_contains_bit", &s, &len, &bitno)) {
    goto exit;
  }
  if (bad_hex_string(len)) {
    goto exit;
  }
  if (bitno < 0) {
    PyErr_SetString(PyExc_ValueError,
		    "bit index must be non-negative");
    goto exit;
  }
  if (4*((long) len) <= bitno) {
    PyErr_SetString(PyExc_ValueError,
		    "bit index is too large");
    goto exit;
  }

  return_value = PyBool_FromLong((long) chemfp_hex_contains_bit(len, s, bitno));

 exit:
  return return_value;
}

static PyObject *
hex_intersect(PyObject *self, PyObject *args) {
  char *s1, *s2;
  int len1, len2;
  PyObject *new_obj = NULL;
  int error;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:hex_intersect", &s1, &len1, &s2, &len2)) {
    goto exit;
  }
  
  if (bad_hex_pair(len1, len2)) {
    goto exit;
  }

  new_obj = PyBytes_FromStringAndSize(NULL, len1);
  if (!new_obj) {
    goto exit;
  }
  
  error = chemfp_hex_intersect(len1, PyBytes_AS_STRING(new_obj), s1, s2);
  if (error) {
    Py_DECREF(new_obj);
    PyErr_SetString(PyExc_ValueError,
		    "one of the hex fingerprints contains a non-hex character");
    new_obj = NULL;
    goto exit;
  }
 exit:
  
  return new_obj;
}

static PyObject *
hex_union(PyObject *self, PyObject *args) {
  char *s1, *s2;
  int len1, len2;
  PyObject *new_obj = NULL;
  int error;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:hex_union", &s1, &len1, &s2, &len2)) {
    goto exit;
  }

  if (bad_hex_pair(len1, len2)) {
    goto exit;
  }

  new_obj = PyBytes_FromStringAndSize(NULL, len1);
  if (!new_obj) {
    goto exit;
  }

  error = chemfp_hex_union(len1, PyBytes_AS_STRING(new_obj), s1, s2);
  if (error) {
    Py_DECREF(new_obj);
    PyErr_SetString(PyExc_ValueError,
		    "one of the hex fingerprints contains a non-hex character");
    new_obj = NULL;
    goto exit;
  }

 exit:
  return new_obj;
}
  
static PyObject *
hex_difference(PyObject *self, PyObject *args) {
  char *s1, *s2;
  int len1, len2;
  PyObject *new_obj = NULL;
  int error;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:hex_difference", &s1, &len1, &s2, &len2)) {
    goto exit;
  }

  if (bad_hex_pair(len1, len2)) {
    goto exit;
  }

  new_obj = PyBytes_FromStringAndSize(NULL, len1);
  if (!new_obj) {
    return NULL;
  }

  error = chemfp_hex_difference(len1, PyBytes_AS_STRING(new_obj), s1, s2);
  if (error) {
    Py_DECREF(new_obj);
    PyErr_SetString(PyExc_ValueError,
		    "one of the hex fingerprints contains a non-hex character");
    new_obj = NULL;
    goto exit;
  }
  
 exit:
  
  return new_obj;
}
  

/********* Byte fingerprint operations  *************/

static PyObject *
byte_popcount(PyObject *self, PyObject *args) {
  unsigned char *s;
  int len;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#:byte_popcount", &s, &len))
    return NULL;
  return PyInt_FromLong((long) chemfp_byte_popcount(len, s));
}

static PyObject *
byte_intersect_popcount(PyObject *self, PyObject *args) {
  unsigned char *s1, *s2;
  int len1, len2;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:byte_intersect_popcount", &s1, &len1, &s2, &len2))
    return NULL;
  if (len1 != len2) {
    PyErr_SetString(PyExc_ValueError,
                    "byte fingerprints must have the same length");
    return NULL;
  }
  return PyInt_FromLong((long) chemfp_byte_intersect_popcount(len1, s1, s2));
}

static PyObject *
byte_tanimoto(PyObject *self, PyObject *args) {
  unsigned char *s1, *s2;
  int len1, len2;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:byte_tanimoto", &s1, &len1, &s2, &len2))
    return NULL;
  if (len1 != len2) {
    PyErr_SetString(PyExc_ValueError,
                    "byte fingerprints must have the same length");
    return NULL;
  }
  return PyFloat_FromDouble(chemfp_byte_tanimoto(len1, s1, s2));
}


static PyObject *
byte_hex_tanimoto(PyObject *self, PyObject *args) {
  unsigned char *s1;
  int len1;
  char *s2;
  int len2;
  double score;
  PyObject *return_value = NULL;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:byte_hex_tanimoto", &s1, &len1, &s2, &len2)) {
    goto exit;
  }
  if (2*len1 != len2) {
    PyErr_SetString(PyExc_ValueError,
                    "hex fingerprint length must be twice the byte fingerprint length");
    goto exit;
  }
  score = chemfp_byte_hex_tanimoto(len1, s1, s2);
  if (score == -1.0) {
      PyErr_SetString(PyExc_ValueError,
                      "the hex fingerprint contains a non-hex character");
      goto exit;
  }

  return_value = PyFloat_FromDouble(score);
  
 exit:
  return return_value;
}

static PyObject *
byte_tversky(PyObject *self, PyObject *args) {
  unsigned char *s1, *s2;
  int len1, len2;
  double alpha=1.0, beta=1.0;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#|dd:byte_tversky", &s1, &len1, &s2, &len2, &alpha, &beta))
    return NULL;
  if (len1 != len2) {
    PyErr_SetString(PyExc_ValueError,
                    "byte fingerprints must have the same length");
    return NULL;
  }
  if (bad_tversky(alpha, beta)) {
    return NULL;
  }
  return PyFloat_FromDouble(chemfp_byte_tversky(len1, s1, s2, alpha, beta));
}

static PyObject *
byte_hex_tversky(PyObject *self, PyObject *args) {
  unsigned char *s1;
  int len1;
  char *s2;
  int len2;
  double alpha=1.0, beta=1.0, score;
  UNUSED(self);
  PyObject *return_value = NULL;

  if (!PyArg_ParseTuple(args, "s#s#|dd:byte_hex_tversky", &s1, &len1, &s2, &len2,
                        &alpha, &beta)) {
    goto exit;
  }
  if (2*len1 != len2) {
    PyErr_SetString(PyExc_ValueError,
                    "hex fingerprint length must be twice the byte fingerprint length");
    goto exit;
  }
  if (bad_tversky(alpha, beta)) {
    goto exit;
  }
  score = chemfp_byte_hex_tversky(len1, s1, s2, alpha, beta);
  if (score == -1.0) {
      PyErr_SetString(PyExc_ValueError,
                      "the hex fingerprint contains a non-hex character");
      goto exit;
  }
  return_value = PyFloat_FromDouble(score);
 exit:
  return return_value;
}


static PyObject *
byte_contains(PyObject *self, PyObject *args) {
  unsigned char *s1, *s2;
  int len1, len2;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:byte_contains", &s1, &len1, &s2, &len2))
    return NULL;
  if (len1 != len2) {
    PyErr_SetString(PyExc_ValueError,
                    "byte fingerprints must have the same length");
    return NULL;
  }
  return PyInt_FromLong(chemfp_byte_contains(len1, s1, s2));
}

static PyObject *
byte_contains_bit(PyObject *self, PyObject *args) {
  char *s;
  int len;
  long bitno;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#l:byte_contain_bit", &s, &len, &bitno))
    return NULL;
  if (bitno < 0) {
    PyErr_SetString(PyExc_ValueError,
		    "bit index must be non-negative");
    return NULL;
  }
  if (8*((long) len) <= bitno) {
    PyErr_SetString(PyExc_ValueError,
		    "bit index is too large");
    return NULL;
  }
  /*return PyBool_FromLong(s[bitno/8] & (1 << (bitno%8) ));*/
  return PyBool_FromLong(chemfp_byte_contains_bit(len, s, bitno));
}

static PyObject *
byte_intersect(PyObject *self, PyObject *args) {
  unsigned char *s, *s1, *s2;
  int i, len1, len2;
  PyObject *new_obj;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:byte_intersect", &s1, &len1, &s2, &len2))
    return NULL;
  if (len1 != len2) {
    PyErr_SetString(PyExc_ValueError,
                    "byte fingerprints must have the same length");
    return NULL;
  }
  new_obj = PyString_FromStringAndSize(NULL, len1);
  if (!new_obj) {
    return NULL;
  }
  s = (unsigned char *) PyString_AS_STRING(new_obj);
  for (i=0; i<len1; i++) {
    s[i] = s1[i] & s2[i];
  }
  return new_obj;
}

static PyObject *
byte_union(PyObject *self, PyObject *args) {
  unsigned char *s, *s1, *s2;
  int i, len1, len2;
  PyObject *new_obj;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:byte_union", &s1, &len1, &s2, &len2))
    return NULL;
  if (len1 != len2) {
    PyErr_SetString(PyExc_ValueError,
                    "byte fingerprints must have the same length");
    return NULL;
  }
  new_obj = PyString_FromStringAndSize(NULL, len1);
  if (!new_obj) {
    return NULL;
  }
  s = (unsigned char *) PyString_AS_STRING(new_obj);
  for (i=0; i<len1; i++) {
    s[i] = s1[i] | s2[i];
  }
  return new_obj;
}

static PyObject *
byte_difference(PyObject *self, PyObject *args) {
  unsigned char *s, *s1, *s2;
  int i, len1, len2;
  PyObject *new_obj;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#s#:byte_difference", &s1, &len1, &s2, &len2))
    return NULL;
  if (len1 != len2) {
    PyErr_SetString(PyExc_ValueError,
                    "byte fingerprints must have the same length");
    return NULL;
  }
  new_obj = PyString_FromStringAndSize(NULL, len1);
  if (!new_obj) {
    return NULL;
  }
  s = (unsigned char *) PyString_AS_STRING(new_obj);
  for (i=0; i<len1; i++) {
    s[i] = s1[i] ^ s2[i];
  }
  return new_obj;
}

/*************** Internal validation routines  *************/

static int
bad_num_bits(int num_bits) {
  if (num_bits <= 0) {
    PyErr_SetString(PyExc_ValueError, "num_bits must be positive");
    return 1;
  }
  return 0;
}

static int
bad_k(int k) {
  if (k < 0) {
    PyErr_SetString(PyExc_ValueError, "k must not be negative");
    return 1;
  }
  return 0;
}

static int
bad_threshold(double threshold) {
  if (threshold < 0.0 || threshold > 1.0) {
    PyErr_SetString(PyExc_ValueError, "threshold must between 0.0 and 1.0, inclusive");
    return 1;
  }
  return 0;
}

static int
bad_alignment(int alignment) {
  if (chemfp_byte_popcount(sizeof(int), (unsigned char *) &alignment) != 1) {
    PyErr_SetString(PyExc_ValueError, "alignment must be a positive power of two");
    return 1;
  }
  return 0;
}

static int
bad_padding(const char *which, int start_padding, int end_padding,
            const unsigned char **arena, int *arena_size) {
  char msg[150];
  /*  printf("PADDING: %d %d for %d\n", start_padding, end_padding, *arena_size);*/
  if (start_padding < 0) {
    sprintf(msg, "%sstart_padding must not be negative", which);
    PyErr_SetString(PyExc_ValueError, msg);
    return 1;
  }
  if (end_padding < 0) {
    sprintf(msg, "%send_padding must not be negative", which);
    PyErr_SetString(PyExc_ValueError, msg);
    return 1;
  }
  if ((start_padding + end_padding) > *arena_size) {
    sprintf(msg, "%sarena_size is too small for the paddings", which);
    PyErr_SetString(PyExc_ValueError, msg);
    return 1;
  }
  *arena += start_padding;
  *arena_size -= (start_padding + end_padding);
  return 0;
}



/* The arena num bits and storage size must be compatible */
static int
bad_arena_size(const char *which, int num_bits, int storage_size) {
  char msg[150];
  int fp_size = (num_bits+7) / 8;
  if (storage_size < 0) {
    sprintf(msg, "%sstorage_size must be positive", which);
    PyErr_SetString(PyExc_ValueError, msg);
    return 1;
  }
  if (fp_size > storage_size) {
    sprintf(msg, "num_bits of %d (%d bytes) does not fit into %sstorage_size of %d",
            num_bits, fp_size, which, storage_size);
    PyErr_SetString(PyExc_ValueError, msg);
    return 1;
  }
  return 0;
}

/* There must be enough cells for at least num queries (in an FPS threshold search) */
static int 
bad_fps_cells(int *num_cells, int cells_size, int num_queries) {
  char msg[100];
  *num_cells = (int)(cells_size / sizeof(chemfp_tanimoto_cell));
  if (*num_cells < num_queries) {
    sprintf(msg, "%d queries requires at least %d cells, not %d",
            num_queries, num_queries, *num_cells);
    PyErr_SetString(PyExc_ValueError, msg);
    return 1;
  }
  return 0;
}

static int
bad_results(SearchResults *results, int results_offset, int batch_size) {
  
  if (!PyObject_TypeCheck(results, &chemfp_py_SearchResultsType)) {
    PyErr_SetString(PyExc_TypeError, "results is not a SearchResult instance");
    return 1;
  }
  if (results_offset < 0) {
    PyErr_SetString(PyExc_ValueError, "results_offset must be non-negative");
    return 1;
  }
  if (results_offset >= results->num_results) {
    PyErr_SetString(PyExc_ValueError, "results_offset is larger than the number of available results");
    return 1;
  }
  if (results_offset + batch_size > results->num_results) {
    PyErr_SetString(PyExc_ValueError, "SearchResults is not large enough for the expected number of results");
    return 1;
  }
  return 0;
}

static int
bad_num_results(int num_results) {
  if (num_results <= 0) {
    PyErr_SetString(PyExc_ValueError, "num_results must be positive");
    return 1;
  }
  return 0;
}


static int
bad_knearest_search_size(int knearest_search_size) {
  if (knearest_search_size < (int) sizeof(chemfp_fps_knearest_search)) {
    PyErr_SetString(PyExc_ValueError,
                    "Not enough space allocated for a chemfp_fps_knearest_search");
    return 1;
  }
  return 0;
}

/* Check/adjust the start and end positions into an FPS block */
static int
bad_block_limits(int block_size, int *start, int *end) {
  if (*start < 0) {
    PyErr_SetString(PyExc_ValueError, "block start must not be negative");
    return 1;
  }
  if (*end == -1 || *end > block_size) {
    *end = block_size;
  } else if (*end < 0) {
    PyErr_SetString(PyExc_ValueError, "block end must either be -1 or non-negative");
    return 1;
  }

  if (*start > block_size) {
    *start = block_size;
  }
  return 0;
}

/* Check/adjust the start and end positions into an arena */
static int
bad_arena_limits(const char *which, int arena_size, int storage_size, int *start, int *end) {
  char msg[150];
  int max_index;
  if (arena_size % storage_size != 0) {
    sprintf(msg, "%sarena size (%d) is not a multiple of its storage size (%d)",
            which, arena_size, storage_size);
    PyErr_SetString(PyExc_ValueError, msg);
    return 1;
  }
  if (*start < 0) {
    sprintf(msg, "%sstart must not be negative", which);
    PyErr_SetString(PyExc_ValueError, msg);
    return 1;
  }
  max_index = arena_size / storage_size;
  if (*start > max_index) {  /* I'll later ignore if start is too large */
    *start = max_index;
  }
  if (*end == -1 || *end > max_index) {
    *end = max_index;
  } else if (*end < 0) {
    sprintf(msg, "%send must either be -1 or non-negative", which);
    PyErr_SetString(PyExc_ValueError, msg);
    return 1;
  }
  return 0;
}

static int
bad_fingerprint_sizes(int num_bits, int query_storage_size, int target_storage_size) {
  return (bad_arena_size("query_", num_bits, query_storage_size) ||
          bad_arena_size("target_", num_bits, target_storage_size));
}

static int
bad_popcount_indices(const char *which, int check_indices, int num_bits,
                      int popcount_indices_size, int **popcount_indices_ptr) {
  char msg[150];
  int num_popcounts;
  int prev, i;
  int *popcount_indices;

  if (popcount_indices_size == 0) {
    /* Special case: this means to ignore this field */
    *popcount_indices_ptr = NULL;
    return 0;
  }
  if ((popcount_indices_size % sizeof(int)) != 0) {
    sprintf(msg,
            "%spopcount indices length (%d) is not a multiple of the native integer size",
            which, popcount_indices_size);
    PyErr_SetString(PyExc_ValueError, msg);
    return 1;
  }

  /* If there is 1 bit then there must be three indices: */
  /*   indices[0]...indices[1] ==> fingerprints with 0 bits set */
  /*   indices[1]...indices[2] ==> fingerprints with 1 bit set */

  num_popcounts = (int)(popcount_indices_size / sizeof(int));

  if (num_bits > num_popcounts - 2) {
    sprintf(msg, "%d bits requires at least %d %spopcount indices, not %d",
            num_bits, num_bits+2, which, num_popcounts);
    PyErr_SetString(PyExc_ValueError, msg);
    return 1;
  }

  if (check_indices) {
    popcount_indices = *popcount_indices_ptr;
    if (popcount_indices[0] != 0) {
      sprintf(msg, "%s popcount indices[0] must be 0", which);
      PyErr_SetString(PyExc_ValueError, "%spopcount_indices[0] must be 0");
      return 1;
    }
    prev = 0;
    for (i=1; i<num_popcounts; i++) {
      if (popcount_indices[i] < prev) {
        sprintf(msg, "%spopcount indices must never decrease", which);
        PyErr_SetString(PyExc_ValueError, msg);
        return 1;
      }
      prev = popcount_indices[i];
    }
  }
  return 0;
}




static int
bad_counts(int count_size, int num_queries) {
  if ((int)(count_size / sizeof(int)) < num_queries) {
    PyErr_SetString(PyExc_ValueError, "Insufficient space to store all of the counts");
    return 1;
  }
  return 0;
}


/*************** FPS functions  *************/
static int
bad_fps_size(long long line_size) {
  if (line_size > 1024*1024*1024) {
    PyErr_SetString(PyExc_ValueError, "fps line must not exceed 1 GB");
    return 1;
  }
  return 0;
}

static int
bad_hex_size(int hex_size) {
  if (hex_size == -1) {
    return 0;
  }
  if (hex_size < 1) {
    PyErr_SetString(PyExc_ValueError, "hex_size must be positive or -1");
    return 1;
  }
  if (hex_size % 2 != 0) {
    PyErr_SetString(PyExc_ValueError, "hex_size must be a multiple of 2");
    return 1;
  }
  return 0;
}

/* Is this something I really need? Peering into a block might be better */
static PyObject *
fps_line_validate(PyObject *self, PyObject *args) {
  int hex_size, line_size;
  char *line;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "is#:fps_line_validate", &hex_size, &line, &line_size))
    return NULL;
  if (bad_hex_size(hex_size) ||
      bad_fps_size(line_size))
    return NULL;
  return PyInt_FromLong(chemfp_fps_line_validate(hex_size, line_size, line));
}

/* Extract the binary fingerprint and identifier from the line */

/* This assume only the characters 0-9, A-F and a-f will be used */
static const int _hex_digit_to_value[] = {
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, /*  0-15 */
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, /* 16-31 */
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, /* 32-47 */
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, /* 48-63 */
  0,10,11,12,13,14,15, 0, 0, 0, 0, 0, 0, 0, 0, 0, /* 64-79 */
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, /* 80-95 */
  0,10,11,12,13,14,15};                           /* 96-102 */

static PyObject *
fps_parse_id_fp(PyObject *self, PyObject *args) {
  long long_hex_size;
  int hex_size;
  int err, i;
  Py_ssize_t line_size;
  char *line;
  const char *id_start, *id_end;
  PyObject *fp, *obj;
  char *s;
  PyObject *err_obj=NULL, *id=NULL, *id_fp=NULL, *return_obj=NULL;
  UNUSED(self);

  /* The parser calls this for every single line of the FPS file. */
  /* Timing shows that PyArg_ParseTuple took about 10% of the time, */
  /* Replacing it with a manual API saves 0.18 seconds across 1 million lines. */
  /*
  if (!PyArg_ParseTuple(args, "is#:fps_parse_id_fp", &hex_size, &line, &line_size))
    return NULL;
  */

  if (PyTuple_GET_SIZE(args) != 2) {
    PyErr_SetString(PyExc_TypeError, "fps_parse_id_fp expected 2 arguments");
    return NULL;
  }
  obj = PyTuple_GET_ITEM(args, 0);
  long_hex_size = PyInt_AsLong(obj);
  if (long_hex_size == -1) {
    if (PyErr_Occurred()) {
      return NULL;
    }
  }
  if (long_hex_size > 2147483647) {
    PyErr_SetString(PyExc_TypeError, "fps_parse_id_fp hex fingerprint too large");
    return NULL;
  }
  hex_size = (int) long_hex_size;
  
  obj = PyTuple_GET_ITEM(args, 1);
  if (PyString_AsStringAndSize(obj, &line, &line_size) == -1) {
    return NULL;
  }
  /* end of manual tuple parser */

  if (bad_hex_size(hex_size) ||
      bad_fps_size(line_size))
    return NULL;

  if (line_size == 0 || line[line_size-1] != '\n') {
    return Py_BuildValue("i(ss)", CHEMFP_MISSING_NEWLINE, NULL, NULL);
  }
  err = chemfp_fps_find_id((int) hex_size, line, &id_start, &id_end);
  if (err != CHEMFP_OK) {
    return Py_BuildValue("i(ss)", err, NULL, NULL);
  }
  if (hex_size == -1) {
    hex_size = (int)(id_start-line)-1;
  }
  fp = PyString_FromStringAndSize(NULL, hex_size/2);
  if (!fp)
    return NULL;
  s = PyString_AS_STRING(fp);
  for (i=0; i<hex_size; i+=2) {
    *s++ = (char)((_hex_digit_to_value[(int)line[i]]<<4)+_hex_digit_to_value[(int)line[i+1]]);
  }

  /* The following replaces
       return Py_BuildValue("i(s#N)", err, id_start, (int)(id_end-id_start), fp);
     because it gives an overall 4% performance boost in reading records
     (about 1 second for every 10 million records) */

  err_obj = PyInt_FromLong(err);
  if (!err_obj) {
    goto err;
  }

  id = PyString_FromStringAndSize(id_start, id_end-id_start);
  if (!id) {
    goto err;
  }

  id_fp = PyTuple_New(2);
  if (!id_fp) {
    goto err;
  }
  return_obj = PyTuple_New(2);
  if (!return_obj) {
    goto err;
  }
  PyTuple_SET_ITEM(id_fp, 0, id);
  PyTuple_SET_ITEM(id_fp, 1, fp);

  PyTuple_SET_ITEM(return_obj, 0, err_obj);
  PyTuple_SET_ITEM(return_obj, 1, id_fp);

  return return_obj;

 err:
  Py_XDECREF(return_obj);
  Py_XDECREF(id_fp);
  Py_XDECREF(id);
  Py_XDECREF(err_obj);
  Py_XDECREF(fp);
  return NULL;
}



/* In Python this is
 (err, num_lines_processed) = fps_tanimoto_count(
     num_bits, query_storage_size, query_arena,
     target_block, target_start, target_end,
     threshold, counts)
*/
static PyObject *
fps_count_tanimoto_hits(PyObject *self, PyObject *args) {
  int num_bits, query_storage_size, query_arena_size, query_start, query_end;
  int query_start_padding, query_end_padding;
  const unsigned char *query_arena;
  const char *target_block;
  int target_block_size, target_start, target_end;
  double threshold;
  int *counts, counts_size;
  int num_lines_processed = 0;
  int err;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "iiiit#iit#iidw#:fps_count_tanimoto_hits",
                        &num_bits,
                        &query_start_padding, &query_end_padding,
                        &query_storage_size, &query_arena, &query_arena_size,
                        &query_start, &query_end,
                        &target_block, &target_block_size,
                        &target_start, &target_end,
                        &threshold,
                        &counts, &counts_size))
    return NULL;

  if (bad_num_bits(num_bits) ||
      bad_padding("query_", query_start_padding, query_end_padding,
                  &query_arena, &query_arena_size) ||
      bad_arena_size("query_", num_bits, query_storage_size) ||
      bad_arena_limits("query ", query_arena_size, query_storage_size,
                       &query_start, &query_end) ||
      bad_block_limits(target_block_size, &target_start, &target_end) ||
      bad_threshold(threshold) ||
      bad_counts(counts_size, query_arena_size / query_storage_size)) {
    return NULL;
  }

  if (target_start >= target_end) {
    /* start of next byte to process, num lines processed, num cells */
    return Py_BuildValue("iiii", CHEMFP_OK, target_end, 0, 0);
  }
  Py_BEGIN_ALLOW_THREADS;
  err = chemfp_fps_count_tanimoto_hits(
        num_bits, 
        query_storage_size, query_arena, query_start, query_end,
        target_block+target_start, target_end-target_start,
        threshold, counts, &num_lines_processed);
  Py_END_ALLOW_THREADS;

  return Py_BuildValue("ii", err, num_lines_processed);
                       
}

/* The threshold search processes N queries at a time by adjusting the block location */
/* The C-level results are off by target_size. Fix them. */
static void adjust_cell_ids(long target_start, chemfp_tanimoto_cell *cells, int num_cells) {
  int cell_i;
  /* Fix up the id start/end positions */
  if (target_start) {
    for (cell_i=0; cell_i<num_cells; cell_i++) {
      cells[cell_i].id_start += target_start;
      cells[cell_i].id_end += target_start;
    }
  }
}

/* In Python this is
 (err, next_start, num_lines_processed, num_cells_processed) = 
     fps_threshold_tanimoto_search(num_bits, query_storage_size, query_arena,
                                   target_block, target_start, target_end,
                                   threshold, cells)
*/
static PyObject *
fps_threshold_tanimoto_search(PyObject *self, PyObject *args) {
  int num_bits, query_start_padding, query_end_padding;
  int query_storage_size, query_arena_size, query_start, query_end;
  const unsigned char *query_arena;
  const char *target_block, *stopped_at;
  int target_block_size, target_start, target_end;
  chemfp_tanimoto_cell *cells;
  double threshold;
  int cells_size;
  int num_lines_processed = 0, num_cells_processed = 0;
  int num_cells, err;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "iiiit#iit#iidw#:fps_threshold_tanimoto_search",
                        &num_bits,
                        &query_start_padding, &query_end_padding,
                        &query_storage_size, &query_arena, &query_arena_size,
                        &query_start, &query_end,
                        &target_block, &target_block_size,
                        &target_start, &target_end,
                        &threshold,
                        &cells, &cells_size))
    return NULL;

  if (bad_num_bits(num_bits) ||
      bad_padding("query_", query_start_padding, query_end_padding,
                  &query_arena, &query_arena_size) ||
      bad_arena_size("query_", num_bits, query_storage_size) ||
      bad_arena_limits("query ", query_arena_size, query_storage_size,
                       &query_start, &query_end) ||
      bad_block_limits(target_block_size, &target_start, &target_end) ||
      bad_threshold(threshold) ||
      bad_fps_cells(&num_cells, cells_size, query_arena_size / query_storage_size)) {
    return NULL;
  }
  if (target_start >= target_end) {
    /* start of next byte to process, num lines processed, num cells */
    return Py_BuildValue("iiii", CHEMFP_OK, target_end, 0, 0);
  }
  Py_BEGIN_ALLOW_THREADS;
  err = chemfp_fps_threshold_tanimoto_search(
        num_bits, 
        query_storage_size, query_arena, query_start, query_end,
        target_block+target_start, target_end-target_start,
        threshold,
        num_cells, cells,
        &stopped_at, &num_lines_processed, &num_cells_processed);
  adjust_cell_ids(target_start, cells, num_cells_processed);
  Py_END_ALLOW_THREADS;

  return Py_BuildValue("iiii", err, stopped_at - target_block,
                       num_lines_processed, num_cells_processed);
}

static PyObject *
fps_knearest_search_init(PyObject *self, PyObject *args) {
  chemfp_fps_knearest_search *knearest_search;
  int start_padding, end_padding;
  int knearest_search_size, num_bits, query_storage_size;
  unsigned const char *query_arena;
  int query_arena_size, query_start, query_end, k;
  double threshold;
  int err;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "w#iiiit#iiid:fps_knearest_search_init",
                        &knearest_search, &knearest_search_size,
                        &num_bits, &start_padding, &end_padding, &query_storage_size,
                        &query_arena, &query_arena_size, &query_start, &query_end,
                        &k, &threshold))
    return NULL;

  if (bad_knearest_search_size(knearest_search_size) ||
      bad_num_bits(num_bits) ||
      bad_padding("", start_padding, end_padding, &query_arena, &query_arena_size) ||
      bad_arena_size("query_", num_bits, query_storage_size) ||
      bad_arena_limits("query ", query_arena_size, query_storage_size,
                       &query_start, &query_end) ||
      bad_k(k) ||
      bad_threshold(threshold)) {
    return NULL;
  }

  Py_BEGIN_ALLOW_THREADS;
  err = chemfp_fps_knearest_search_init(
          knearest_search, num_bits, query_storage_size, 
          query_arena, query_start, query_end,
          k, threshold);
  Py_END_ALLOW_THREADS;
  if (err) {
    PyErr_SetString(PyExc_ValueError, chemfp_strerror(err));
    return NULL;
  }
  return Py_BuildValue("");
}

static PyObject *
fps_knearest_tanimoto_search_feed(PyObject *self, PyObject *args) {
  chemfp_fps_knearest_search *knearest_search;  
  int knearest_search_size;
  const char *target_block;
  int target_block_size, target_start, target_end;
  int err;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "w#t#ii:fps_knearest_tanimoto_search_feed",
                        &knearest_search, &knearest_search_size,
                        &target_block, &target_block_size, &target_start, &target_end))
    return NULL;

  if (bad_knearest_search_size(knearest_search_size) ||
      bad_block_limits(target_block_size, &target_start, &target_end))
    return NULL;

  Py_BEGIN_ALLOW_THREADS;
  err = chemfp_fps_knearest_tanimoto_search_feed(knearest_search, target_block_size, target_block);
  Py_END_ALLOW_THREADS;
  return PyInt_FromLong(err);
}

static PyObject *
fps_knearest_search_finish(PyObject *self, PyObject *args) {
  chemfp_fps_knearest_search *knearest_search;  
  int knearest_search_size;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "w#:fps_knearest_search_finish",
                        &knearest_search, &knearest_search_size))
    return NULL;
  if (bad_knearest_search_size(knearest_search_size))
    return NULL;

  Py_BEGIN_ALLOW_THREADS;
  chemfp_fps_knearest_search_finish(knearest_search);
  Py_END_ALLOW_THREADS;

  return Py_BuildValue("");
}


static PyObject *
fps_knearest_search_free(PyObject *self, PyObject *args) {
  chemfp_fps_knearest_search *knearest_search;  
  int knearest_search_size;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "w#:fps_knearest_search_free",
                        &knearest_search, &knearest_search_size))
    return NULL;
  if (bad_knearest_search_size(knearest_search_size))
    return NULL;

  Py_BEGIN_ALLOW_THREADS;
  chemfp_fps_knearest_search_free(knearest_search);
  Py_END_ALLOW_THREADS;

  return Py_BuildValue("");
}



/**************** The library-based searches **********/

/* Always allocate space. This must overallocate because */
/* there is no guarantee the start alignment. */
/* (Though on my Mac it's always 4-byte aligned. */
static PyObject *
alloc_aligned_arena(ssize_t size, int alignment,
                    int *start_padding, int *end_padding) {
  PyObject *new_py_string;
  char *s;
  uintptr_t i;

  new_py_string = PyString_FromStringAndSize(NULL, size+alignment-1);
  if (!new_py_string) {
    return NULL;
  }
  s = PyString_AS_STRING(new_py_string);
  i = ALIGNMENT(s, alignment);
  if (i == 0) {
    *start_padding = 0;
    *end_padding = alignment-1;
  } else {
    *start_padding = (int)(alignment - i);
    *end_padding = (int)(i-1);
  }
  memset(s, 0, *start_padding);
  memset(s+size+*start_padding, 0, *end_padding);
  return new_py_string;
}

static PyObject *
align_arena(PyObject *input_arena_obj, int alignment,
            int *start_padding, int *end_padding) {
  const char *input_arena;
  char *output_arena;
  Py_ssize_t input_arena_size;
  uintptr_t i;
  PyObject *output_arena_obj;

  if (PyObject_AsCharBuffer(input_arena_obj, &input_arena, &input_arena_size)) {
    PyErr_SetString(PyExc_ValueError, "arena must be a character buffer");
    return NULL;
  }
  i = ALIGNMENT(input_arena, alignment);
  
  /* Already aligned */
  if (i == 0) {
    *start_padding = 0;
    *end_padding = 0;
    Py_INCREF(input_arena_obj);
    return input_arena_obj;
  }
  /* Not aligned. We'll have to move it to a new string */
  output_arena_obj = alloc_aligned_arena(input_arena_size, alignment,
                                         start_padding, end_padding);
  output_arena = PyString_AS_STRING(output_arena_obj);

  /* Copy over into the new string */
  memcpy(output_arena+*start_padding, input_arena, input_arena_size);

  return output_arena_obj;
}

static PyObject *
make_unsorted_aligned_arena(PyObject *self, PyObject *args) {
  int alignment;
  int start_padding=0, end_padding=0;
  PyObject *input_arena_obj, *output_arena_obj;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "Oi:make_unsorted_aligned_arena",
                        &input_arena_obj, &alignment)) {
    return NULL;
  }
  if (bad_alignment(alignment)) {
    return NULL;
  }
  output_arena_obj = align_arena(input_arena_obj, alignment,
                                 &start_padding, &end_padding);
  if (!output_arena_obj) {
    return NULL;
  }
  return Py_BuildValue("iiN", start_padding, end_padding, output_arena_obj);
}

static PyObject *
align_fingerprint(PyObject *self, PyObject *args) {
  PyObject *input_fp_obj, *new_fp_obj;
  const char *fp;
  char *new_fp;
  Py_ssize_t fp_size;
  int alignment, start_padding, storage_size, end_padding;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "Oii:align_fingerprint",
                        &input_fp_obj, &alignment, &storage_size)) {
    return NULL;
  }
  if (bad_alignment(alignment)) {
    return NULL;
  }

  if (PyObject_AsCharBuffer(input_fp_obj, &fp, &fp_size)) {
    PyErr_SetString(PyExc_ValueError, "fingerprint must be a character buffer");
    return NULL;
  }
  if (storage_size < 1) {
    PyErr_SetString(PyExc_ValueError, "storage size must be positive");
    return NULL;
  }
  if (storage_size < fp_size) {
    PyErr_SetString(PyExc_ValueError, "storage size is too small for the query");
    return NULL;
  }

  /* Are we lucky? */
  if (storage_size == fp_size) {
    new_fp_obj = align_arena(input_fp_obj, alignment, &start_padding, &end_padding);
  } else {
    /* Unlucky. Need to allocate more space */
    new_fp_obj = alloc_aligned_arena(storage_size, alignment, &start_padding, &end_padding);
    if (!new_fp_obj) {
      return NULL;
    }
    new_fp = PyString_AS_STRING(new_fp_obj);
    /* Copy over into the new string */
    memcpy(new_fp+start_padding, fp, fp_size);
    /* Zero out the remaining bytes */
    memset(new_fp+start_padding+fp_size, 0, storage_size-fp_size);
  }
  return Py_BuildValue("iiN", start_padding, end_padding, new_fp_obj);
}

static int
calculate_arena_popcounts(int num_bits, int storage_size, const unsigned char *arena,
                          int num_fingerprints, ChemFPOrderedPopcount *ordering) {
  chemfp_popcount_f calc_popcount;
  const unsigned char *fp;
  int fp_index, popcount, prev_popcount;
  /* Compute the popcounts. (Alignment isn't that important here.) */

  calc_popcount = chemfp_select_popcount(num_bits, storage_size, arena);
  fp = arena;
  for (fp_index = 0; fp_index < num_fingerprints; fp_index++, fp += storage_size) {
    popcount = calc_popcount(storage_size, fp);
    ordering[fp_index].popcount = popcount;
    ordering[fp_index].index = fp_index;
  }

  /* Check if the values are already ordered */

  prev_popcount = ordering[0].popcount;
  for (fp_index = 1; fp_index < num_fingerprints; fp_index++) {
    if (ordering[fp_index].popcount < prev_popcount) {
      return 1; /* Need to sort */
    }
    prev_popcount = ordering[fp_index].popcount;
  }
  return 0; /* Don't need to sort */
}


static int compare_by_popcount(const void *left_p, const void *right_p) {
  const ChemFPOrderedPopcount *left = (ChemFPOrderedPopcount *) left_p;
  const ChemFPOrderedPopcount *right = (ChemFPOrderedPopcount *) right_p;
  if (left->popcount < right->popcount) {
    return -1;
  }
  if (left->popcount > right->popcount) {
    return 1;
  }
  if (left->index < right->index) {
    return -1;
  }
  if (left->index > right->index) {
    return 1;
  }
  return 0;
}


static void
set_popcount_indicies(int num_fingerprints, int num_bits,
                      ChemFPOrderedPopcount *ordering, int *popcount_indices) {
  int popcount, i;

  /* We've sorted by popcount so this isn't so difficult */
  popcount = 0;
  popcount_indices[0] = 0;
  for (i=0; i<num_fingerprints; i++) {
    while (popcount < ordering[i].popcount) {
      popcount++;
      popcount_indices[popcount] = i;
      if (popcount == num_bits) {
        /* We are at or above the limit. We can stop now. */
        i = num_fingerprints;
        break;
        /* Note: with corrupted data it is possible
           that ->popcount can be > num_bits. This is
           undefined behavior. I get to do what I want.
           I decided to treat them as having "max_popcount" bits.
           After all, I don't want corrupt data to crash the
           system, and no one is going to validate the input
           fingerprints for correctness each time.  */
      }
    }
  }
  /* Finish up the high end */
  while (popcount <= num_bits) {
    popcount_indices[++popcount] = num_fingerprints;
  }
}


static PyObject *
make_sorted_aligned_arena(PyObject *self, PyObject *args) {
  int start = 0;
  int num_bits, storage_size, num_fingerprints, ordering_size, popcount_indices_size;
  int start_padding, end_padding;
  PyObject *input_arena_obj, *output_arena_obj;
  const unsigned char *input_arena;
  unsigned char *output_arena;
  Py_ssize_t input_arena_size;
  ChemFPOrderedPopcount *ordering;
  int *popcount_indices;
  int need_to_sort, i;
  int alignment;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "iiOiw#w#i:make_sorted_aligned_arena",
                        &num_bits,
                        &storage_size, &input_arena_obj,
                        &num_fingerprints,
                        &ordering, &ordering_size,
                        &popcount_indices, &popcount_indices_size,
                        &alignment
                        )) {
    return NULL;
  }

  if (PyObject_AsCharBuffer(input_arena_obj,
                             (const char **) &input_arena, &input_arena_size)) {
    PyErr_SetString(PyExc_ValueError, "arena must be a character buffer");
    return NULL;
  }
  if (bad_num_bits(num_bits) ||
      bad_arena_limits("", (int) input_arena_size, storage_size, &start, &num_fingerprints) ||
      bad_popcount_indices("", 0, num_bits, popcount_indices_size, NULL)) {
    return NULL;
  }
  if ((int)(ordering_size / sizeof(ChemFPOrderedPopcount)) < num_fingerprints) {
    PyErr_SetString(PyExc_ValueError, "allocated ordering space is too small");
    return NULL;
  }

  /* Handle the trivial case of no fingerprints */

  if (num_fingerprints == 0) {
    return Py_BuildValue("iiO", 0, 0, input_arena_obj);
  }


  need_to_sort = calculate_arena_popcounts(num_bits, storage_size, input_arena,
                                           num_fingerprints, ordering);

  if (!need_to_sort) {
    /* Everything is ordered. Just need the right alignment .... */
    output_arena_obj = align_arena(input_arena_obj, alignment,
                                   &start_padding, &end_padding);
    if (!output_arena_obj) {
      return NULL;
    }

    /* ... and to set the popcount indicies */
    set_popcount_indicies(num_fingerprints, num_bits, ordering, popcount_indices);
    
    /* Everything is aligned and ordered, so we're done */
    return Py_BuildValue("iiN", start_padding, end_padding, output_arena_obj);
  }

  /* Not ordered. Make space for the results. */
  output_arena_obj = alloc_aligned_arena(input_arena_size, alignment,
                                         &start_padding, &end_padding);
  if (!output_arena_obj) {
    return NULL;
  }
  output_arena = (unsigned char *)(PyString_AS_STRING(output_arena_obj) + start_padding);

  Py_BEGIN_ALLOW_THREADS;
  qsort(ordering, num_fingerprints, sizeof(ChemFPOrderedPopcount), compare_by_popcount);


  /* Build the new arena based on the values in the old arena */
  for (i=0; i<num_fingerprints; i++) {
    memcpy(output_arena+(i*storage_size), input_arena+(ordering[i].index * storage_size),
           storage_size);
  }

  /* Create the popcount indicies */
  set_popcount_indicies(num_fingerprints, num_bits, ordering, popcount_indices);


  Py_END_ALLOW_THREADS;
  return Py_BuildValue("iiN", start_padding, end_padding, output_arena_obj);
}


/* count_tanimoto_arena */
static PyObject *
count_tanimoto_arena(PyObject *self, PyObject *args) {
  double threshold;
  int num_bits;
  const unsigned char *query_arena, *target_arena;
  int query_start_padding, query_end_padding;
  int query_storage_size, query_arena_size=0, query_start=0, query_end=0;
  int target_start_padding, target_end_padding;
  int target_storage_size, target_arena_size=0, target_start=0, target_end=0;
  int *target_popcount_indices, target_popcount_indices_size;
  int result_counts_size, *result_counts;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "diiiis#iiiiis#iis#w#:count_tanimoto_arena",
                        &threshold,
                        &num_bits,
                        &query_start_padding, &query_end_padding,
                        &query_storage_size, &query_arena, &query_arena_size,
                        &query_start, &query_end,
                        &target_start_padding, &target_end_padding,
                        &target_storage_size, &target_arena, &target_arena_size,
                        &target_start, &target_end,
                        &target_popcount_indices, &target_popcount_indices_size,
                        &result_counts, &result_counts_size))
    return NULL;

  if (bad_threshold(threshold) ||
      bad_num_bits(num_bits) ||
      bad_padding("query ", query_start_padding, query_end_padding,
                  &query_arena, &query_arena_size) ||
      bad_padding("target ", target_start_padding, target_end_padding,
                  &target_arena, &target_arena_size) ||
      bad_fingerprint_sizes(num_bits, query_storage_size, target_storage_size) ||
      bad_arena_limits("query ", query_arena_size, query_storage_size,
                       &query_start, &query_end) ||
      bad_arena_limits("target ", target_arena_size, target_storage_size,
                       &target_start, &target_end) ||
      bad_popcount_indices("target ", 1, num_bits, 
                            target_popcount_indices_size, &target_popcount_indices)) {
    return NULL;
  }

  if (query_start > query_end) {
    Py_RETURN_NONE;
  }

  if (result_counts_size < (int)((query_end - query_start)*sizeof(int))) {
    PyErr_SetString(PyExc_ValueError, "not enough space allocated for result_counts");
    return NULL;
  }

  Py_BEGIN_ALLOW_THREADS;
  chemfp_count_tanimoto_arena(threshold,
                              num_bits,
                              query_storage_size, query_arena, query_start, query_end,
                              target_storage_size, target_arena, target_start, target_end,
                              target_popcount_indices,
                              result_counts);
  Py_END_ALLOW_THREADS;

  Py_RETURN_NONE;
}
    
/* threshold_tanimoto_arena */
static PyObject *
threshold_tanimoto_arena(PyObject *self, PyObject *args) {
  double threshold;
  int num_bits;
  int query_start_padding, query_end_padding;
  int query_storage_size, query_arena_size, query_start, query_end;
  const unsigned char *query_arena;
  int target_start_padding, target_end_padding;
  int target_storage_size, target_arena_size, target_start, target_end;
  const unsigned char *target_arena;

  int *target_popcount_indices, target_popcount_indices_size;

  int errval, results_offset;
  SearchResults *results;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "diiiit#iiiiit#iit#Oi:threshold_tanimoto_arena",
                        &threshold,
                        &num_bits,
                        &query_start_padding, &query_end_padding,
                        &query_storage_size, &query_arena, &query_arena_size,
                        &query_start, &query_end,
                        &target_start_padding, &target_end_padding,
                        &target_storage_size, &target_arena, &target_arena_size,
                        &target_start, &target_end,
                        &target_popcount_indices, &target_popcount_indices_size,
                        &results, &results_offset)) {
    return NULL;
  }

  if (bad_threshold(threshold) ||
      bad_num_bits(num_bits) ||
      bad_fingerprint_sizes(num_bits, query_storage_size, target_storage_size) ||
      bad_padding("query ", query_start_padding, query_end_padding, 
                  &query_arena, &query_arena_size) ||
      bad_padding("target ", target_start_padding, target_end_padding, 
                  &target_arena, &target_arena_size) ||
      bad_arena_limits("query ", query_arena_size, query_storage_size,
                       &query_start, &query_end) ||
      bad_arena_limits("target ", target_arena_size, target_storage_size,
                       &target_start, &target_end) ||
      bad_popcount_indices("target ", 1, num_bits,
                            target_popcount_indices_size, &target_popcount_indices) ||
      bad_results(results, results_offset, query_end-query_start)
      ) {
    return NULL;
  }

  Py_BEGIN_ALLOW_THREADS;
  errval = chemfp_threshold_tanimoto_arena(
        threshold,
        num_bits,
        query_storage_size, query_arena, query_start, query_end,
        target_storage_size, target_arena, target_start, target_end,
        target_popcount_indices,
        results->results + results_offset);
  Py_END_ALLOW_THREADS;

  return PyInt_FromLong(errval);
}

/* knearest_tanimoto_arena */
static PyObject *
knearest_tanimoto_arena(PyObject *self, PyObject *args) {
  int k;
  double threshold;
  int num_bits;
  int query_start_padding, query_end_padding;
  int query_storage_size, query_arena_size, query_start, query_end;
  const unsigned char *query_arena;
  int target_start_padding, target_end_padding;
  int target_storage_size, target_arena_size, target_start, target_end;
  const unsigned char *target_arena;

  int *target_popcount_indices, target_popcount_indices_size;

  int errval, results_offset;
  SearchResults *results;

  UNUSED(self);
    
  if (!PyArg_ParseTuple(args, "idiiiit#iiiiit#iit#Oi:knearest_tanimoto_arena",
                        &k, &threshold,
                        &num_bits,
                        &query_start_padding, &query_end_padding,
                        &query_storage_size, &query_arena, &query_arena_size,
                        &query_start, &query_end,
                        &target_start_padding, &target_end_padding,
                        &target_storage_size, &target_arena, &target_arena_size,
                        &target_start, &target_end,
                        &target_popcount_indices, &target_popcount_indices_size,
                        &results, &results_offset)) {
    return NULL;
  }

  if (bad_k(k) ||
      bad_threshold(threshold) ||
      bad_num_bits(num_bits) ||
      bad_padding("query ", query_start_padding, query_end_padding,
                  &query_arena, &query_arena_size) ||
      bad_padding("target ", target_start_padding, target_end_padding,
                  &target_arena, &target_arena_size) ||
      bad_fingerprint_sizes(num_bits, query_storage_size, target_storage_size) ||
      bad_arena_limits("query ", query_arena_size, query_storage_size,
                       &query_start, &query_end) ||
      bad_arena_limits("target ", target_arena_size, target_storage_size,
                       &target_start, &target_end) ||
      bad_popcount_indices("target ", 1, num_bits,
                            target_popcount_indices_size, &target_popcount_indices) ||
      bad_results(results, results_offset, query_end-query_start)) {
    return NULL;
  }
  
  Py_BEGIN_ALLOW_THREADS;
  errval = chemfp_knearest_tanimoto_arena(
        k, threshold,
        num_bits,
        query_storage_size, query_arena, query_start, query_end,
        target_storage_size, target_arena, target_start, target_end,
        target_popcount_indices,
        results->results);
  Py_END_ALLOW_THREADS;
  
  return PyInt_FromLong(errval);
}

static PyObject *
knearest_results_finalize(PyObject *self, PyObject *args) {
  int results_offset, num_results;
  SearchResults *results;
  UNUSED(self);
    
  if (!PyArg_ParseTuple(args, "Oii",
                        &results, &results_offset, &num_results)) {
    return NULL;
  }
  if (bad_results(results, results_offset, num_results) ||
      bad_num_results(num_results)) {
    return NULL;
  }
  Py_BEGIN_ALLOW_THREADS;
  chemfp_knearest_results_finalize(results->results+results_offset,
                                   results->results+results_offset+num_results);
  Py_END_ALLOW_THREADS;
  return Py_BuildValue("");
}

/***** Symmetric search code ****/

static PyObject *
count_tanimoto_hits_arena_symmetric(PyObject *self, PyObject *args) {
  double threshold;
  int num_bits, start_padding, end_padding, storage_size, arena_size;
  int query_start, query_end, target_start, target_end;
  const unsigned char *arena;
  int *popcount_indices, *result_counts;
  int popcount_indices_size, result_counts_size;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "diiiis#iiiis#w#:count_tanimoto_arena",
                        &threshold,
                        &num_bits,
                        &start_padding, &end_padding,
                        &storage_size, &arena, &arena_size,
                        &query_start, &query_end,
                        &target_start, &target_end,
                        &popcount_indices, &popcount_indices_size,
                        &result_counts, &result_counts_size)) {
    return NULL;
  }
  if (bad_threshold(threshold) ||
      bad_num_bits(num_bits) ||
      bad_padding("", start_padding, end_padding, &arena, &arena_size) ||
      bad_fingerprint_sizes(num_bits, storage_size, storage_size) ||
      bad_arena_limits("query ", arena_size, storage_size, &query_start, &query_end) ||
      bad_arena_limits("target ", arena_size, storage_size, &target_start, &target_end) ||
      bad_popcount_indices("", 1, num_bits, popcount_indices_size, &popcount_indices)) {
    return NULL;
  }
  if (result_counts_size < (arena_size / storage_size) * sizeof(int) ) {
    PyErr_SetString(PyExc_ValueError, "not enough space allocated for result_counts");
    return NULL;
  }
  if (query_start > query_end) {
    Py_RETURN_NONE;
  }
  Py_BEGIN_ALLOW_THREADS;
  chemfp_count_tanimoto_hits_arena_symmetric(threshold,
                                             num_bits,
                                             storage_size, arena,
                                             query_start, query_end,
                                             target_start, target_end,
                                             popcount_indices,
                                             result_counts);
  Py_END_ALLOW_THREADS;
  
  Py_RETURN_NONE;
}

static PyObject *
threshold_tanimoto_arena_symmetric(PyObject *self, PyObject *args) {
  double threshold;
  int num_bits, start_padding, end_padding, storage_size, arena_size;
  int query_start, query_end, target_start, target_end;
  const unsigned char *arena;
  int *popcount_indices;
  int popcount_indices_size;
  SearchResults *results;
  int results_offset;
  int errval;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "diiiis#iiiis#Oi:threshold_tanimoto_arena_symmetric",
                        &threshold,
                        &num_bits,
                        &start_padding, &end_padding,
                        &storage_size, &arena, &arena_size,
                        &query_start, &query_end,
                        &target_start, &target_end,
                        &popcount_indices, &popcount_indices_size,
                        &results, &results_offset)) {
    return NULL;
  }
  if (bad_threshold(threshold) ||
      bad_num_bits(num_bits) ||
      bad_padding("", start_padding, end_padding, &arena, &arena_size) ||
      bad_fingerprint_sizes(num_bits, storage_size, storage_size) ||
      bad_arena_limits("query ", arena_size, storage_size, &query_start, &query_end) ||
      bad_arena_limits("target ", arena_size, storage_size, &target_start, &target_end) ||
      bad_popcount_indices("", 1, num_bits, popcount_indices_size, &popcount_indices) ||
      bad_results(results, results_offset, query_end-query_start)) {
    return NULL;
  }
  Py_BEGIN_ALLOW_THREADS;
  errval = chemfp_threshold_tanimoto_arena_symmetric(threshold,
                                                     num_bits,
                                                     storage_size, arena,
                                                     query_start, query_end,
                                                     target_start, target_end,
                                                     popcount_indices,
                                                     results->results+results_offset);
  Py_END_ALLOW_THREADS;
  
  if (errval < CHEMFP_OK) {
    if (errval == CHEMFP_NO_MEM) {
      return PyErr_NoMemory();
    }
    PyErr_SetString(PyExc_RuntimeError, chemfp_strerror(errval));
    return NULL;
  }  
  Py_RETURN_NONE;
}

/* knearest_tanimoto_arena */
static PyObject *
knearest_tanimoto_arena_symmetric(PyObject *self, PyObject *args) {
  double threshold;
  int k, num_bits, start_padding, end_padding, storage_size, arena_size;
  int query_start, query_end, target_start, target_end;
  const unsigned char *arena;
  int *popcount_indices;
  int popcount_indices_size;
  SearchResults *results;
  int results_offset;
  int errval;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "idiiiis#iiiis#Oi:knearest_tanimoto_arena_symmetric",
                        &k, &threshold,
                        &num_bits,
                        &start_padding, &end_padding,
                        &storage_size, &arena, &arena_size,
                        &query_start, &query_end,
                        &target_start, &target_end,
                        &popcount_indices, &popcount_indices_size,
                        &results, &results_offset)) {
    return NULL;
  }
  if (bad_k(k) ||
      bad_threshold(threshold) ||
      bad_num_bits(num_bits) ||
      bad_padding("", start_padding, end_padding, &arena, &arena_size) ||
      bad_fingerprint_sizes(num_bits, storage_size, storage_size) ||
      bad_arena_limits("query ", arena_size, storage_size, &query_start, &query_end) ||
      bad_arena_limits("target ", arena_size, storage_size, &target_start, &target_end) ||
      bad_popcount_indices("", 1, num_bits, popcount_indices_size, &popcount_indices) ||
      bad_results(results, results_offset, query_end-query_start)) {
    return NULL;
  }
  Py_BEGIN_ALLOW_THREADS;
  errval = chemfp_knearest_tanimoto_arena_symmetric(
                                           k, threshold,
                                           num_bits,
                                           storage_size, arena,
                                           query_start, query_end,
                                           target_start, target_end,
                                           popcount_indices,
                                           results->results+results_offset);
  Py_END_ALLOW_THREADS;
  
  if (errval < CHEMFP_OK) {
    if (errval == CHEMFP_NO_MEM) {
      return PyErr_NoMemory();
    }
    PyErr_SetString(PyExc_RuntimeError, chemfp_strerror(errval));
    return NULL;
  }  
  Py_RETURN_NONE;
}

/* End of Tanimoto */

static PyObject *
contains_arena(PyObject *self, PyObject *args) {
  int num_bits;
  int query_start_padding, query_end_padding;
  int query_storage_size, query_start, query_end;
  int query_arena_size, target_arena_size;
  const unsigned char *query_arena;
  int target_start_padding, target_end_padding;
  int target_storage_size, target_start, target_end;
  const unsigned char *target_arena;

  int *target_popcount_indices;
  int target_popcount_indices_size;

  int errval, results_offset;
  SearchResults *results;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "iiiit#iiiiit#iit#Oi:contains_arena",
                        &num_bits,
                        &query_start_padding, &query_end_padding,
                        &query_storage_size, &query_arena, &query_arena_size,
                        &query_start, &query_end,
                        &target_start_padding, &target_end_padding,
                        &target_storage_size, &target_arena, &target_arena_size,
                        &target_start, &target_end,
                        &target_popcount_indices, &target_popcount_indices_size,
                        &results, &results_offset)) {
    return NULL;
  }

  if (bad_num_bits(num_bits) ||
      bad_fingerprint_sizes(num_bits, query_storage_size, target_storage_size) ||
      bad_padding("query ", query_start_padding, query_end_padding, 
                  &query_arena, &query_arena_size) ||
      bad_padding("target ", target_start_padding, target_end_padding, 
                  &target_arena, &target_arena_size) ||
      bad_arena_limits("query ", query_arena_size, query_storage_size,
                       &query_start, &query_end) ||
      bad_arena_limits("target ", target_arena_size, target_storage_size,
                       &target_start, &target_end) ||
      bad_popcount_indices("target ", 1, num_bits,
                            target_popcount_indices_size, &target_popcount_indices) ||
      bad_results(results, results_offset, query_end-query_start)
      ) {
    return NULL;
  }

  Py_BEGIN_ALLOW_THREADS;
  errval = chemfp_contains_arena(
        num_bits,
        query_storage_size, query_arena, query_start, query_end,
        target_storage_size, target_arena, target_start, target_end,
        target_popcount_indices,
        results->results + results_offset);
  Py_END_ALLOW_THREADS;
  if (errval < CHEMFP_OK) {
    if (errval == CHEMFP_NO_MEM) {
      return PyErr_NoMemory();
    }
    PyErr_SetString(PyExc_RuntimeError, chemfp_strerror(errval));
    return NULL;
  }
  Py_RETURN_NONE;
}


static PyObject *
fill_lower_triangle(PyObject *self, PyObject *args) {
  int num_results, errval;
  SearchResults *results;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "Oi:fill_lower_triangle",
                        &results, &num_results)) {
    return NULL;
  }
  if (bad_results(results, 0, num_results) ||
      bad_num_results(num_results)) {
    return NULL;
  }
  Py_BEGIN_ALLOW_THREADS;
  errval = chemfp_fill_lower_triangle(num_results, results->results);
  Py_END_ALLOW_THREADS;

  if (errval) {
    PyErr_SetString(PyExc_ValueError, chemfp_strerror(errval));
    return NULL;
  }
  Py_RETURN_NONE;
}


/* Select the popcount methods */

static PyObject *
get_num_methods(PyObject *self, PyObject *args) {
  UNUSED(self);
  UNUSED(args);

  return PyInt_FromLong(chemfp_get_num_methods());
}

static PyObject *
get_method_name(PyObject *self, PyObject *args) {
  int method;
  const char *s;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "i:get_method_name", &method)) {
    return NULL;
  }
  s = chemfp_get_method_name(method);
  if (s == NULL) {
    PyErr_SetString(PyExc_IndexError, "method index is out of range");
    return NULL;
  }
  return PyString_FromString(s);
}

static PyObject *
get_num_alignments(PyObject *self, PyObject *args) {
  UNUSED(self);
  UNUSED(args);

  return PyInt_FromLong(chemfp_get_num_alignments());
}

static PyObject *
get_alignment_name(PyObject *self, PyObject *args) {
  int alignment;
  const char *s;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "i:get_alignment_name", &alignment)) {
    return NULL;
  }
  s = chemfp_get_alignment_name(alignment);
  if (s == NULL) {
    PyErr_SetString(PyExc_IndexError, "alignment index is out of range");
    return NULL;
  }
  return PyString_FromString(s);
}

static PyObject *
get_alignment_method(PyObject *self, PyObject *args) {
  int alignment, method;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "i:get_alignment_method", &alignment)) {
    return NULL;
  }
  method = chemfp_get_alignment_method(alignment);
  if (method < 0) {
    PyErr_SetString(PyExc_ValueError, chemfp_strerror(method));
    return NULL;
  }
  return PyInt_FromLong(method);
}


static PyObject *
set_alignment_method(PyObject *self, PyObject *args) {
  int alignment, method;
  int result;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "ii:get_alignment_method", &alignment, &method)) {
    return NULL;
  }
  result = chemfp_set_alignment_method(alignment, method);
  if (result < 0) {
    PyErr_SetString(PyExc_ValueError, chemfp_strerror(result));
    return NULL;
  }
  return Py_BuildValue("");
}

static PyObject *
select_fastest_method(PyObject *self, PyObject *args) {
  int alignment, repeat, result;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "ii:select_fastest_method", &alignment, &repeat)) {
    return NULL;
  }
  result = chemfp_select_fastest_method(alignment, repeat);
  if (result < 0) {
    PyErr_SetString(PyExc_ValueError, chemfp_strerror(result));
    return NULL;
  }
  return PyInt_FromLong(result);
}


static PyObject *
get_num_options(PyObject *self, PyObject *args) {
  UNUSED(self);
  UNUSED(args);
  return PyInt_FromLong(chemfp_get_num_options());
}

static PyObject *
get_option_name(PyObject *self, PyObject *args) {
  int i;
  const char *s;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "i:get_option_name", &i)) {
    return NULL;
  }
  s = chemfp_get_option_name(i);
  if (s == NULL) {
    PyErr_SetString(PyExc_IndexError, "option name index out of range");
    return NULL;
  }
  return PyString_FromString(s);
}

static PyObject *
get_option(PyObject *self, PyObject *args) {
  const char *option;
  int value;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s:get_option", &option)) {
    return NULL;
  }
  value = chemfp_get_option(option);
  if (value == CHEMFP_BAD_ARG) {
    /* Nothing can currently return -1, so this is an error */
    PyErr_SetString(PyExc_ValueError, "Unknown option name");
    return NULL;
  }
  return PyInt_FromLong(value);
}

static PyObject *
set_option(PyObject *self, PyObject *args) {
  const char *option;
  int value, result;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "si:set_option", &option, &value)) {
    return NULL;
  }

  /* Make sure it's a valid name */
  if (chemfp_get_option(option) == CHEMFP_BAD_ARG) {
    PyErr_SetString(PyExc_ValueError, "Unknown option name");
    return NULL;
  }

  result = chemfp_set_option(option, value);
  if (result != CHEMFP_OK) {
    PyErr_SetString(PyExc_ValueError, "Bad option value");
    return NULL;
  }
  return Py_BuildValue("");
}

static PyObject*
get_num_threads(PyObject *self, PyObject *args) {
  UNUSED(self);
  UNUSED(args);
  return PyInt_FromLong(chemfp_get_num_threads());
}

static PyObject*
set_num_threads(PyObject *self, PyObject *args) {
  int num_threads;
  UNUSED(args);
  
  if (!PyArg_ParseTuple(args, "i:set_num_threads", &num_threads)) {
    return NULL;
  }
  chemfp_set_num_threads(num_threads);

  Py_RETURN_NONE;
}

static PyObject*
get_max_threads(PyObject *self, PyObject *args) {
  UNUSED(self);
  UNUSED(args);
  return PyInt_FromLong(chemfp_get_max_threads());
}


static PyObject *
byte_to_bitlist(PyObject *self, PyObject *args) {
  unsigned char byte, *fp;
  int len;
  int offset;
  long long popcount;
  PyObject *list = NULL, *bitno_obj;
  int list_index = 0;

  if (!PyArg_ParseTuple(args, "s#:byte_to_bitlist", &fp, &len)) {
    goto exit;
  }
  popcount = chemfp_byte_popcount(len, fp);
  list = PyList_New((long) popcount);
  if (!list) {
    goto exit;
  }
  if (popcount == 0) {
    goto exit;
  }
  for (offset=0; offset<len; offset++) {
    byte = fp[offset];

#define ADD_BITNO(bitno)				\
    bitno_obj = PyInt_FromLong(bitno);			\
    if (!bitno_obj) goto int_error;			\
    PyList_SET_ITEM(list, list_index++, bitno_obj);	\
    if (list_index > popcount) goto wrong_popcount;
    
    if (byte &   1) { ADD_BITNO(offset*8 + 0); }
    if (byte &   2) { ADD_BITNO(offset*8 + 1); }
    if (byte &   4) { ADD_BITNO(offset*8 + 2); }
    if (byte &   8) { ADD_BITNO(offset*8 + 3); }
    if (byte &  16) { ADD_BITNO(offset*8 + 4); }
    if (byte &  32) { ADD_BITNO(offset*8 + 5); }
    if (byte &  64) { ADD_BITNO(offset*8 + 6); }
    if (byte & 128) { ADD_BITNO(offset*8 + 7); }
  }
  if (list_index != popcount) {
    goto wrong_popcount;
  }
  goto exit;

 wrong_popcount:
  PyErr_SetString(PyExc_RuntimeError, "popcount changed during evaluation");
  /* fall through */

 int_error:
  Py_DECREF(list);
  list = NULL;

 exit:
  return list;
}

static int hex_char_to_value[256] = {
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  0,  0,  0,  0,  0,  0,
  0, 10, 11, 12, 13, 14, 15,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0, 10, 11, 12, 13, 14, 15,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
};

static PyObject *
hex_to_bitlist(PyObject *self, PyObject *args) {
  int len;
  unsigned char byte;
  char *hex_fp;
  int offset;
  long long popcount;
  PyObject *list = NULL, *bitno_obj;
  int list_index = 0;

  if (!PyArg_ParseTuple(args, "s#:hex_to_bitlist", &hex_fp, &len)) {
    goto exit;
  }
  if (bad_hex_string(len)) {
    goto exit;
  }
  popcount = chemfp_hex_popcount(len, hex_fp);
  if (popcount == -1) {
    PyErr_SetString(PyExc_ValueError,
		    "hex fingerprint contains a non-hex character");
    goto exit;
  }
  list = PyList_New((long) popcount);
  if (!list) {
    goto exit;
  }
  if (popcount == 0) {
    goto exit;
  }
  for (offset=0; offset<len; offset+=2) {
    byte = 16*hex_char_to_value[(int) hex_fp[offset]] + hex_char_to_value[(int) hex_fp[offset+1]];
    if (byte &   1) { ADD_BITNO(offset*4 + 0); }
    if (byte &   2) { ADD_BITNO(offset*4 + 1); }
    if (byte &   4) { ADD_BITNO(offset*4 + 2); }
    if (byte &   8) { ADD_BITNO(offset*4 + 3); }
    if (byte &  16) { ADD_BITNO(offset*4 + 4); }
    if (byte &  32) { ADD_BITNO(offset*4 + 5); }
    if (byte &  64) { ADD_BITNO(offset*4 + 6); }
    if (byte & 128) { ADD_BITNO(offset*4 + 7); }
  }
  if (list_index != popcount) {
    goto wrong_popcount;
  }
  goto exit;

 wrong_popcount:
  PyErr_SetString(PyExc_RuntimeError, "popcount changed during evaluation");
  /* fall through */

 int_error:  /* there's a goto to here inside of ADD_BITNO() */
  Py_DECREF(list);
  list = NULL;

 exit:
  return list;

}

static PyObject *
byte_from_bitlist(PyObject *self, PyObject *args, PyObject *kwargs) {
  static char *keywords[] = {"fp", "num_bits", NULL};
  unsigned char *fp;
  long num_bits = 1024, fp_size;
  PyObject *container, *iter, *item;
  PyObject *fp_obj = NULL;
  long item_value;
  ssize_t byte_offset;
  int bit_offset;
  
  if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|l:byte_from_bitlist", keywords,
				   &container, &num_bits)) {
    return NULL;
  }
  if (num_bits == 0) {
    return PyBytes_FromStringAndSize(NULL, 0);
  } else if (num_bits < 0) {
    PyErr_SetString(PyExc_ValueError, "num_bits must not be negative");
    return NULL;
  }

  iter = PyObject_GetIter(container);
  if (iter == NULL) {
    return NULL;
  }

  fp_size = (num_bits+7) / 8;
  fp_obj = PyBytes_FromStringAndSize(NULL, fp_size);
  if (!fp_obj) {
    return NULL;
  }
  fp = (unsigned char *) PyBytes_AS_STRING(fp_obj);
  memset(fp, 0, fp_size);

  for (;;) {
    item = PyIter_Next(iter);
    if (!item) {
      /* Either an exception or the end of iteration */
      if (PyErr_Occurred()) {
	goto error;
      }
      break;
    }
    item_value = PyInt_AsLong(item);
    if (item_value < 0) {
      if (item_value == -1) {
	if (PyErr_Occurred()) {
	  goto error;
	}
      }
      PyErr_SetString(PyExc_ValueError, "bit numbers must be non-negative");
      goto error;
    }
    
    item_value = item_value % num_bits;  /* fold when the input is too large */
    bit_offset = (int)(item_value % 8);
    byte_offset = item_value / 8;
    fp[byte_offset] |= (1<<bit_offset);
    
    Py_DECREF(item);
  }
  Py_DECREF(iter);
  return fp_obj;

 error:
  Py_DECREF(iter);
  Py_DECREF(fp_obj);
  return NULL;
}

static char to_hex[16] = "0123456789abcdef";

static PyObject *
hex_from_bitlist(PyObject *self, PyObject *args, PyObject *kwargs) {
  static char *keywords[] = {"fp", "num_bits", NULL};
  unsigned char *fp;
  long num_bits = 1024, fp_size;
  PyObject *container, *iter, *item;
  PyObject *fp_obj = NULL;
  long item_value;
  ssize_t byte_offset;
  int bit_offset;
  
  if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|l:hex_from_bitlist", keywords,
				   &container, &num_bits)) {
    return NULL;
  }
  if (num_bits == 0) {
    return PyBytes_FromStringAndSize(NULL, 0);
  } else if (num_bits < 0) {
    PyErr_SetString(PyExc_ValueError, "num_bits must not be negative");
    return NULL;
  }

  iter = PyObject_GetIter(container);
  if (iter == NULL) {
    return NULL;
  }

  fp_size = num_bits / 8;  /* length of the byte fingerprint */
  if (num_bits % 8) {
    fp_size++;
  }
  fp_obj = PyBytes_FromStringAndSize(NULL, fp_size*2); /* length of the hex fingerprint */
  if (!fp_obj) {
    return NULL;
  }
  fp = (unsigned char *) PyBytes_AS_STRING(fp_obj);
  memset(fp, 0, fp_size);
  
  /* The following creates a byte fingerprint */
  for (;;) {
    item = PyIter_Next(iter);
    if (!item) {
      /* Either an exception or the end of iteration */
      if (PyErr_Occurred()) {
	goto error;
      }
      break;
    }
    item_value = PyInt_AsLong(item);
    if (item_value < 0) {
      if (item_value == -1) {
	if (PyErr_Occurred()) {
	  goto error;
	}
      }
      PyErr_SetString(PyExc_ValueError, "bit numbers must be non-negative");
      goto error;
    }
    
    item_value = item_value % num_bits;  /* fold when the input is too large */
    bit_offset = (int)(item_value % 8);
    byte_offset = item_value / 8;
    fp[byte_offset] |= (1<<bit_offset);
    
    Py_DECREF(item);
  }
  Py_DECREF(iter);

  /* Convert the byte fingerprint into a hex fingerprint */
  /* In-place modification, so go from the end backwards */
  for (byte_offset=fp_size-1; byte_offset>=0; byte_offset--) {
    item_value = fp[byte_offset];
    fp[2*byte_offset] = to_hex[item_value/16];
    fp[2*byte_offset+1] = to_hex[item_value%16];
  }
  return fp_obj;

 error:
  Py_DECREF(iter);
  Py_DECREF(fp_obj);
  return NULL;
}


/*************** Convert to/from hex strings  *************/

/* This is similar to binascii.hexlify/unhexlify except I allow 7-bit strings as input 
   in addition to bytes. */

const char *hexdigits = "0123456789abcdef";

static PyObject *
hex_encode(PyObject *self, PyObject *args) {
  PyObject *return_value = NULL;
  int i, j, len;
  unsigned char c, *input_string, *output_string;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#:hex_encode", &input_string, &len)) {
    goto exit;
  }

  return_value = PyBytes_FromStringAndSize(NULL, 2*len);
  if (!return_value) {
    goto exit;
  }
  output_string = (unsigned char *) PyBytes_AS_STRING(return_value);

  for (i=j=0; i<len; i++, j+=2) {
    c = input_string[i];
    output_string[j  ] = hexdigits[(c>>4) & 0x0f];  /* high nibble */
    output_string[j+1] = hexdigits[ c     & 0x0f];  /* low nibble */
  }
  
 exit:
  return return_value;
}


static PyObject *
hex_encode_as_bytes(PyObject *self, PyObject *args) {
  PyObject *return_value = NULL;
  int i, j, len;
  unsigned char c, *input_string, *output_string;
  UNUSED(self);

  if (!PyArg_ParseTuple(args, "s#:hex_encode_as_bytes", &input_string, &len)) {
    goto exit;
  }

  return_value = PyBytes_FromStringAndSize(NULL, 2*len);
  if (!return_value) {
    goto exit;
  }
  output_string = (unsigned char *) PyBytes_AS_STRING(return_value);

  for (i=j=0; i<len; i++, j+=2) {
    c = input_string[i];
    output_string[j  ] = hexdigits[(c>>4) & 0x0f];  /* high nibble */
    output_string[j+1] = hexdigits[ c     & 0x0f];  /* low nibble */
  }
  
 exit:
  return return_value;
}

static int VALID_HEX[256] = {
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
  0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
};

static PyObject *
hex_decode(PyObject *self, PyObject *args) {
  PyObject *return_value = NULL;
  PyObject *fp = NULL;
  unsigned char *s, c1, c2;
  const unsigned char *hex_buf;
  int valid_hex = 1;
  int hex_len, i;

  if (!PyArg_ParseTuple(args, "s#:hex_decode", &hex_buf, &hex_len)) {
    goto exit;
  }
  if (hex_len % 2 == 1) {
    PyErr_SetString(PyExc_ValueError,
                    "Odd-length string");
    goto exit;
  }
  fp = PyBytes_FromStringAndSize(NULL, hex_len/2);
  if (!fp) {
    goto exit;
  }
  s = (unsigned char *) PyBytes_AS_STRING(fp);
  for (i=0; i<hex_len; i+=2) {
    c1 = hex_buf[i];
    c2 = hex_buf[i+1];
    valid_hex &= VALID_HEX[c1] & VALID_HEX[c2];
    *s++ = (char)((_hex_digit_to_value[c1]<<4)+_hex_digit_to_value[c2]);
  }
  if (!valid_hex) {
    PyErr_SetString(PyExc_ValueError,
                    "Non-hexadecimal digit found");
    Py_DECREF(fp);
    goto exit;
  }
  return_value = fp;

 exit:
  return return_value;
}


static PyMethodDef chemfp_methods[] = {
  {"version", version, METH_NOARGS,
   "version()\n\nReturn the chemfp library version, as a string like '1.0'"},
  {"strerror", strerror_, METH_VARARGS,
   "strerror(n)\n\nConvert the error code integer to more descriptive text"},

  {"hex_isvalid", hex_isvalid, METH_VARARGS,
   "hex_isvalid(s)\n\nReturn 1 if the string is a valid hex fingerprint, otherwise 0"},
  {"hex_popcount", hex_popcount, METH_VARARGS, 
   "hex_popcount(fp)\n\nReturn the number of bits set in a hex fingerprint, or -1 for non-hex strings"},
  {"hex_intersect_popcount", hex_intersect_popcount, METH_VARARGS,
   "hex_intersect_popcount(fp1, fp2)\n\nReturn the number of bits set in the intersection of the two hex fingerprint,\nor -1 if either string is a non-hex string"},
  {"hex_tanimoto", hex_tanimoto, METH_VARARGS,
   "hex_tanimoto(fp1, fp2)\n\nCompute the Tanimoto similarity between two hex fingerprints.\nReturn a float between 0.0 and 1.0, or -1.0 if either string is not a hex fingerprint"},
  {"hex_tversky", hex_tversky, METH_VARARGS,
   "hex_tversky(fp1, fp2, alpha=1.0, beta=1.0)\n\n"
   "Compute the Tversky index between two hex fingerprints. Return a float\n"
   "between 0.0 and 1.0, or raise a ValueError if either string is not a hex fingerprint"},
  {"hex_contains", hex_contains, METH_VARARGS,
   "hex_contains(super_fp, sub_fp)\n\nReturn 1 if the on bits of sub_fp are also 1 bits in super_fp, otherwise 0.\nReturn -1 if either string is not a hex fingerprint"},
  {"hex_contains", hex_contains, METH_VARARGS,
   "hex_contains(sub_fp, super_fp)\n\n"
   "Return 1 if the on bits of sub_fp are also on bits in super_fp, otherwise 0.\n"
   "Return -1 if either string is not a hex fingerprint"},
  {"hex_contains_bit", hex_contains_bit, METH_VARARGS,
   "hex_contains_bit(fp, bit_index)\n\n"
   "Return True if the the given bit position is on, otherwise False.\n\n"
   "This function does not validate that the hex fingerprint is actually in hex."},
  {"hex_intersect", hex_intersect, METH_VARARGS,
   "hex_intersect(fp1, fp2)\n\n"
   "Return the intersection of the two hex strings, *fp1* & *fp2*.\n"
   "Raises a ValueError for non-hex fingerprints."},
  {"hex_union", hex_union, METH_VARARGS,
   "hex_union(fp1, fp2)\n\n"
   "Return the union of the two hex strings, *fp1* | *fp2*.\n"
   "Raises a ValueError for non-hex fingerprints."},
  {"hex_difference", hex_difference, METH_VARARGS,
   "hex_difference(fp1, fp2)\n\n"
   "Return the absolute difference (xor) between the two hex strings, *fp1* ^ *fp2*.\n"
   "Raises a ValueError for non-hex fingerprints."},

  {"byte_popcount", byte_popcount, METH_VARARGS,
   "byte_popcount(fp)\n\nReturn the number of bits set in a byte fingerprint"},
  {"byte_intersect_popcount", byte_intersect_popcount, METH_VARARGS,
   "byte_intersect_popcount(fp1, fp2)\n\nReturn the number of bits set in the instersection of the two byte fingerprints"},
  {"byte_tanimoto", byte_tanimoto, METH_VARARGS,
   "byte_tanimoto(fp1, fp2)\n\nCompute the Tanimoto similarity between two byte fingerprints"},
  {"byte_hex_tanimoto", byte_hex_tanimoto, METH_VARARGS,
   "byte_hex_tanimoto(fp1, fp2)\n\n"
   "Compute the Tanimoto similarity between the byte fingerprint *fp1* and the hex fingerprint *fp2*.\n"
   "Return a float between 0.0 and 1.0, or raise a ValueError if *fp2* is not a hex fingerprint"},
  {"byte_tversky", byte_tversky, METH_VARARGS,
   "byte_tversky(fp1, fp2, alpha=1.0, beta=1.0)\n\n"
   "Compute the Tversky index between the two byte fingerprints *fp1* and *fp2*"},
  {"byte_hex_tversky", byte_hex_tversky, METH_VARARGS,
   "byte_hex_tversky(fp1, fp2, alpha=1.0, beta=1.0)\n\n"
   "Compute the Tversky index between the byte fingerprint *fp1* and the hex fingerprint *fp2*.\n"
   "Return a float between 0.0 and 1.0, or raise a ValueError if *fp2* is not a hex fingerprint"},
  
  {"byte_contains", byte_contains, METH_VARARGS,
   "byte_contains(super_fp, sub_fp)\n\nReturn 1 if the on bits of sub_fp are also 1 bits in super_fp"},
  {"byte_contains_bit", byte_contains_bit, METH_VARARGS,
   "byte_contains_bit(fp, bit_index)\n\n"
   "Return True if the the given bit position is on, otherwise False"},
  {"byte_intersect", byte_intersect, METH_VARARGS,
   "byte_intersect(fp1, fp2)\n\n"
   "Return the intersection of the two byte strings, *fp1* & *fp2*"},
  {"byte_union", byte_union, METH_VARARGS,
   "byte_union(fp1, fp2)\n\n"
   "Return the union of the two byte strings, *fp1* | *fp2*"},
  {"byte_difference", byte_difference, METH_VARARGS,
   "byte_difference(fp1, fp2)\n\n"
   "Return the absolute difference (xor) between the two byte strings, fp1 ^ fp2"},

  /* FPS */
  {"fps_line_validate", fps_line_validate, METH_VARARGS,
   "fps_line_validate (TODO: document)"},
  {"fps_parse_id_fp", fps_parse_id_fp, METH_VARARGS,
   "fps_parse_id_fp (TODO: document)"},

  {"fps_threshold_tanimoto_search", fps_threshold_tanimoto_search, METH_VARARGS,
   "fps_threshold_tanimoto_search (TODO: document)"},

  {"fps_count_tanimoto_hits", fps_count_tanimoto_hits, METH_VARARGS,
   "fps_count_tanimoto_hits (TODO: document)"},


  {"fps_knearest_search_init", fps_knearest_search_init, METH_VARARGS,
   "fps_knearest_search_init (TODO: document)"},
  {"fps_knearest_tanimoto_search_feed", fps_knearest_tanimoto_search_feed, METH_VARARGS,
   "fps_knearest_tanimoto_search_feed (TODO: document)"},
  {"fps_knearest_search_finish", fps_knearest_search_finish, METH_VARARGS,
   "fps_knearest_search_finish (TODO: document)"},
  {"fps_knearest_search_free", fps_knearest_search_free, METH_VARARGS,
   "fps_knearest_search_free (TODO: document)"},

  {"count_tanimoto_arena", count_tanimoto_arena, METH_VARARGS,
   "count_tanimoto_arena (TODO: document)"},

  {"threshold_tanimoto_arena", threshold_tanimoto_arena, METH_VARARGS,
   "threshold_tanimoto_arena (TODO: document)"},

  {"knearest_tanimoto_arena", knearest_tanimoto_arena, METH_VARARGS,
   "knearest_tanimoto_arena (TODO: document)"},
  {"knearest_results_finalize", knearest_results_finalize, METH_VARARGS,
   "knearest_results_finalize (TODO: document)"},

  {"count_tanimoto_hits_arena_symmetric", count_tanimoto_hits_arena_symmetric, METH_VARARGS,
   "count_tanimoto_hits_arena_symmetric (TODO: document)"},
  {"threshold_tanimoto_arena_symmetric", threshold_tanimoto_arena_symmetric, METH_VARARGS,
   "threshold_tanimoto_arena_symmetric (TODO: document)"},
  {"knearest_tanimoto_arena_symmetric", knearest_tanimoto_arena_symmetric, METH_VARARGS,
   "knearest_tanimoto_arena_symmetric (TODO: document)"},

  /* End of Tanimoto */

  {"contains_arena", contains_arena, METH_VARARGS,
   "contains_arena (TODO: contains_arena)"},

  {"fill_lower_triangle", fill_lower_triangle, METH_VARARGS,
   "fill_lower_triangle (TODO: document)"},

  {"make_sorted_aligned_arena", make_sorted_aligned_arena, METH_VARARGS,
   "make_sorted_aligned_arena (TODO: document)"},

  {"make_unsorted_aligned_arena", make_unsorted_aligned_arena, METH_VARARGS,
   "make_unsorted_aligned_arena (TODO: document)"},

  {"align_fingerprint", align_fingerprint, METH_VARARGS,
   "align_fingerprint (TODO: document)"},

  /* Select the popcount methods */
  {"get_num_methods", get_num_methods, METH_NOARGS,
   "get_num_methods (TODO: document)"},

  {"get_method_name", get_method_name, METH_VARARGS,
   "get_method_name (TODO: document)"},

  {"get_num_alignments", get_num_alignments, METH_NOARGS,
   "get_num_alignments (TODO: document)"},

  {"get_alignment_name", get_alignment_name, METH_VARARGS,
   "get_alignment_name (TODO: document)"},

  {"get_alignment_method", get_alignment_method, METH_VARARGS,
   "get_alignment_method (TODO: document)"},

  {"set_alignment_method", set_alignment_method, METH_VARARGS,
   "set_alignment_method (TODO: document)"},

  {"select_fastest_method", select_fastest_method, METH_VARARGS,
   "select_fastest_method (TODO: document)"},

  {"get_num_options", get_num_options, METH_NOARGS,
   "get_num_options (TODO: document)"},

  {"get_option_name", get_option_name, METH_VARARGS,
   "get option name (TODO: document)"},

  {"get_option", get_option, METH_VARARGS,
   "get option (TODO: document)"},

  {"set_option", set_option, METH_VARARGS,
   "set option (TODO: document)"},

  {"get_num_threads", get_num_threads, METH_NOARGS,
   "get_num_threads()\n\nSet the number of OpenMP threads to use in a search"},

  {"set_num_threads", set_num_threads, METH_VARARGS,
   "set_num_threads()\n\nGet the number of OpenMP threads to use in a search"},

  {"get_max_threads", get_max_threads, METH_NOARGS,
   "get_max_threads()\n\nGet the maximum number of OpenMP threads available"},

  /* byte string to/from a bitlist */

  {"byte_to_bitlist", byte_to_bitlist, METH_VARARGS,
   "byte_to_bitlist(bitlist)\n\nReturn a sorted list of the on-bit positions in the byte fingerprint"},

  {"hex_to_bitlist", hex_to_bitlist, METH_VARARGS,
   "hex_to_bitlist(bitlist)\n\nReturn a sorted list of the on-bit positions in the hex fingerprint"},

  {"byte_from_bitlist", (PyCFunction) byte_from_bitlist, METH_VARARGS | METH_KEYWORDS,
   "byte_from_bitlist(fp[, num_bits=1024])\n\nConvert a list of bit positions into a byte fingerprint, including modulo folding"},

  {"hex_from_bitlist", (PyCFunction) hex_from_bitlist, METH_VARARGS | METH_KEYWORDS,
   "hex_from_bitlist(fp[, num_bits=1024])\n\nConvert a list of bit positions into a hex fingerprint, including modulo folding"},

  {"hex_encode", (PyCFunction) hex_encode, METH_VARARGS,
   "hex_encode(s)\n\nEncode the byte string or ASCII string to hex. Returns a text string."},
  {"hex_encode_as_bytes", (PyCFunction) hex_encode_as_bytes, METH_VARARGS,
   "hex_encode_as_bytes(s)\n\nEncode the byte string or ASCII string to hex. Returns a byte string."},
  {"hex_decode", (PyCFunction) hex_decode, METH_VARARGS,
   "hex_decode(s)\n\nDecode the hex-encoded value to a byte string"},
  

  {NULL, NULL, 0, NULL}        /* Sentinel */

};

PyMODINIT_FUNC
init_chemfp(void)
{
  PyObject *m;
  if (PyType_Ready(&chemfp_py_SearchResultsType) < 0) {
    return ;
  }
  m = Py_InitModule3("_chemfp", chemfp_methods, "Documentation goes here");
  Py_INCREF(&chemfp_py_SearchResultsType);
  PyModule_AddObject(m, "SearchResults", (PyObject *)&chemfp_py_SearchResultsType);
}
