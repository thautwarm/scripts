/* File: cpp_stl.i */
%module cpp_stl

%{
#define SWIG_FILE_WITH_INIT
#include "Python.h"
%}


%include "std_list.i"
%include "std_vector.i"
%include "std_map.i"
%include "std_string.i"


namespace std {
   %template(List) list<PyObject*>;
   %template(Vector) vector<PyObject*>;
};



