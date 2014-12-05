import sys
import os

TITLE = "CSV Viewer"
VERSION = 2.6

def dir():

    if hasattr(sys, "frozen"):
        # Application is running as exe
        app_path = os.path.dirname(os.path.realpath(sys.executable))
    else:
        # Application is running as script
        app_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    
    return app_path
