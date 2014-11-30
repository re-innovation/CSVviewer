CSVviewer Installation
=========

CSVviewer is written using Python 3.4.

There are two basic options for running the program:

* Downloading and running the compiled CSVviewer program - this option requires least setup
* Running from source using a Python 3 installation on your computer - this option requires most setup

Both options are covered in this document.

## Downloading the program

* The latest release is kept in the re-innov GitHub repository.
* Visit http://github.com/re-innovation/CSVviewer. On the right-hand side of the screen, there will be a "Download ZIP" button. Click this.
* When the ZIP file has downloaded, extract it.
* The Releases/Latest folder contains the program files. You may move this folder to a location of your choice. There is no preferred location for the program.
* To run CSV viewer, run "application.exe" in that folder.
* The other files from the ZIP file are not required (you may delete them if you wish)

## Running from source

Before running the code, you must install Python 3.

### Installing Python 3

Follow the instructions for your operating system:

#### Windows 

##### Installing Python and Required Packages
* Go to www.python.com/download and install the Python 3 distribution for Windows (NOT Python 2!).
* Make a note of the python version you have installed (for example Python 3.4.2)
* CSVviewer needs a number of Python packages. There are pre-built Windows versions of these packages at http://www.lfd.uci.edu/~gohlke/pythonlibs/ (with thanks to Christoph Gohlke for maintaining this service)

The following packages are required. Download these are install them. You must pick the correct .exe for your computer and for the python version you installed.

*For example if you have a 64-bit computer and you installed Python 3.4.2, you would use the packages ending ".win-amd64-py3.4.exe".*

* pandas (http://www.lfd.uci.edu/~gohlke/pythonlibs/#pandas)
* matplotlib (http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib)
* numpy (http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)
* dateutil (http://www.lfd.uci.edu/~gohlke/pythonlibs/#dateutil)
* pytz (http://www.lfd.uci.edu/~gohlke/pythonlibs/#pytz)
* pyparsing (http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyparsing)
* setuptools (http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools)

##### Downloading and running CSVviewer
* The latest release is kept in the re-innov GitHub repository.
* Visit http://github.com/re-innovation/CSVviewer. On the right-hand side of the screen, there will be a "Download ZIP" button. Click this.
* When the ZIP file has downloaded, extract it to a location of your choice
* Open a command prompt and navigate to that location.
* Run the command "python application.py" to run CSVviewer.

#### Linux

##### Installing Python

Most modern Linux systems will come with a version of Python already installed.

CSVviewer requires Python 3, which may not be installed.

To check which version you have, open a terminal and run the command "python3", which will open a Python 3 shell.

* If a Python shell opens, you have Python 3 installed. Use Ctrl-D to exit the Python shell.
* If you get "command not found" or a similar error:
  * Run the command "python".
  * If you get "command not found" or a similar error, you don't have Python 3 installed
    * Install Python 3 using your distribution's packaging tools.
  * If a Python shell opens:
    * Note the version number in the top line of the shell (for example "Python 2.7.8").
    * Use Ctrl-D to exit the Python shell 
    * If the version number was less than 3.0:
      * Install Python 3 using your distribution's packaging tools

##### Installing Required Packages

Your Python installation should come with *pip*, which is a package manager for Python.
Run the following commands in a terminal to install the requirements for CSVviewer.
*You may need to run these commands as root.*

```
pip install pandas
pip install matplotlib
pip install numpy
pip install dateutil
pip install pytz
pip install pyparsing
pip install setuptools
```

##### Downloading and running CSVviewer
* The latest release is kept in the re-innov GitHub repository.
* Visit http://github.com/re-innovation/CSVviewer. On the right-hand side of the screen, there will be a "Download ZIP" button. Click this.
* When the ZIP file has downloaded, extract it to a location of your choice
* Open a command prompt and navigate to that location.
* Run the command "python3 application.py" to run CSVviewer.
