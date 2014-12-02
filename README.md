CSVviewer
=========

## Summary
A Python application for graphically displaying data in .CSV files from datalogging hardware

## Requirements:
* Python 3.3+
* pandas
* matplotlib

## Installation:

See [INSTALL.md](http://www.github.com/re-innovation/CSVviewer/INSTALL.md)

## Version Information:

### Version 2.6
* Added progress bar when loading new data from folder
  * Datamanager now runs in seperate thread to allow this
* Windrose plot is only an option when speed and direction data are matched

### Version 2.5
* Added histogram plot

### Version 2.4
* Added windrose plot

### Version 2.3
* Added about dialog

### Version 2.2
* Averaging can be reset for a plot

### Version 2.1
* Averaging is now functional

### Version 2.0
* Removed csv_parser.py and replaced with csv_datamanager.py
* Uses pandas library to provide better dataset math functionality
* Should make development of advanced features much easier
* This version has no functional difference to version 1.0

### Version 1.0
* Removed menu driven interface in favour of GUI
* GUI allows:
  * Selection of folder to load CSV files from
  * Selection of data series to display on each subplot
  * Configuring and applying time-series averaging (to be implemented)

### Version 0.0
* Basic graphing capability
* Command line (textual) menu driven interface
* Limited to three fixed data series (windspeed, temperature, voltage)

