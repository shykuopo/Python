import cx_Freeze
from cx_Freeze import setup, Executable
import sys
import os
import matplotlib

os.environ['TCL_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tk8.6"

base = None

if sys.platform == 'win3.2':
    base = 'win32GUI'

executables = [Executable("RentingSys.py", base=base)]
packages = ['tkinter','csv']

options = {'build_exe': {'packages':packages}}

setup(
    name = "<租借系統>",
    options = options,
    version = "<1.0.1>",
    description = '<test>',
    executables = executables
)