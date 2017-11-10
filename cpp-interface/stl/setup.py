"""
setup.py
"""
 
from distutils.core import setup, Extension
 
 
example_module = Extension('_cpp_stl',
                           sources=['cpp_stl_wrap.cxx'],
                           )
 
setup (name = 'cpp_stl',
       version = '0.1',
       author      = "SWIG Docs",
       description = """Simple swig example from docs""",
       ext_modules = [example_module],
       py_modules = ["cpp_stl"],
       )