"""
app_info.py

@author: James Fowkes

General application information for the CSV viewer
"""

import sys
import os

TITLE = "CSV Viewer"
VERSION = 2.6

def app_dir():

    """ Return the full path from which this script or exe is running """
    if hasattr(sys, "frozen"):
        # Application is running as exe
        app_path = os.path.dirname(os.path.realpath(sys.executable))
    else:
        # Application is running as script
        app_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    return app_path
