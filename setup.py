#!/usr/bin/env python3

from distutils.core import setup, Extension

example_module = Extension('_UTTT',sources = ['UTTT_wrap.cxx', 'UTTT_Library.c', "UTTT.c"])

setup (name = 'UTTT',
       version = '0.1',
       author      = "Robert Stegmann",
       description = """Library for ultimate tic tac toe""",
       ext_modules = [example_module],
       py_modules = ["UTTT"],
       )