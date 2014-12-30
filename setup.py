"""
setup.py

@author: James Fowkes

Setup/disyutils/cx_freeze file for the CSV viewer application
"""

import sys
from cx_Freeze import setup, Executable
from app_info import VERSION

#pylint: disable=invalid-name
# Forget about invalid names in setup file

build_exe_options = {
    'packages':["pandas"],
    'includes' : ["pandas.msgpack"],
    'include_files' : ['config.ini', 'logo.png'],
    'excludes' : ['_gtkagg', '_wxagg'], ## Exclude some backends to reduce size
    }

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="CSVviewer",
    version=VERSION,
    description="A CSV datafile viewer",
    author="Matt Little, James Fowkes",
    options={'build_exe': build_exe_options},
    executables=[Executable("application.py", base=base)]
)
