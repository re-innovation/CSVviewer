CSVviewer Compilation
=========

CSVviewer is written using Python 3.4.

An executable build (which does not require Python to run) is produced using the cx_freeze Python package.

This document details the process.

The instructions here are ONLY required if you wish to compile CSVviewer for a particular system.

The system you are using to build the application still requires Python to work.

To produce a build:

* Follow the instructions in [INSTALL.md](http://www.github.com/re-innovation/CSVviewer/INSTALL.md) for "running from source".
* Confirm that CSVviewer successfully runs from source on your computer.
* Open a command prompt. Navigate to the CSVviewer folder.
* Install the cx_freeze package by running the command "pip install cx_freeze".
* Run the command "python setup.py build".
* Wait for this command to complete (may take some time).
* This will create a build folder. Inside that folder will be another folder (name will depend on your operating system and python version).
* Inside this folder are the compiled files. Run "application.exe" to start the CSVviewer program.
* The files in this folder must be kept together. The folder can be moved/copied to any location on your computer.
