# CSV Viewer

## Summary
A Python application for graphically displaying data in .CSV files from datalogging hardware

## Requirements:
*Python 3.3+
*pandas
*matplotlib

## Version Information:

### Version 2.0
* Removed csv_parser.py and replaced with csv_datamanager.py
* Uses pandas library to provide better dataset math functionality
* Should make development of advanced features much easier
* This version has no functional difference to verion 1.0

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

