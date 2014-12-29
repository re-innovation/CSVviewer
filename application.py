"""
application.py

@author: James Fowkes

Entry file for the CSV viewer application
"""

import argparse
import logging
import configparser
import codecs

from datamanager import DataManager
from gui import GUI, ask_directory, run_gui, show_info_dialog
from csv_plotter import CSV_Plotter, CSV_WindPlotter, CSV_Histogram

import queue
import threading

from app_info import VERSION, TITLE

def get_arg_parser():
    """ Return a command line argument parser for this module """
    arg_parser = argparse.ArgumentParser(
        description='Datalogger CSV Viewer')

    arg_parser.add_argument(
        '--start_folder', dest='start_folder', default=None,
        help="The folder to look for CSVs in")

    return arg_parser

def get_module_logger():

    """ Returns logger for this module """
    return logging.getLogger(__name__)

#pylint: disable=too-many-instance-attributes
# Accept this warning, as application is not likely to grow
# beyond current # of attributes on the short term. Refactoring
# is likely to cause more confusion.
# Consider refactoring if application grows significantly.

class Application:

    """
    Handles interaction between GUI events, GUI drawing, plotting, file reading etc.
    """

    def __init__(self, _, config):

        """
        Args:
        _ : Command line arguments (not currently used)
        config : configparser object containing configuration information
        """

        self.config = config

        self.plotter = CSV_Plotter(config)
        self.windplotter = CSV_WindPlotter(config)
        self.histogram = CSV_Histogram(config)

        self.msg_queue = None
        self.loading_timer = None
        self.data_manager = None

        self.gui = GUI(self)

    def action_about_dialog(self):
        """ Show information about this program """
        info = """
        %s
        Version %s

        Created by:
        Matt Little
        James Fowkes

        http://www.re-innovation.co.uk
        Nottingham, UK

        windrose code adapted from
        http://sourceforge.net/projects/windrose/files/windrose/
        by joshua_fr
        """ % (TITLE, VERSION)

        show_info_dialog(info)

    def action_subplot1_change(self, dataset_choice):
        """ Pass through to action_subplot_change """
        self.action_subplot_change(0, dataset_choice)

    def action_subplot2_change(self, dataset_choice):
        """ Pass through to action_subplot_change """
        self.action_subplot_change(1, dataset_choice)

    def action_subplot3_change(self, dataset_choice):
        """ Pass through to action_subplot_change """
        self.action_subplot_change(2, dataset_choice)

    def action_subplot_change(self, subplot_index, display_name):

        """ Handles request to change subplot data
        Args:
        subplot_index : The index of the subpolot (0 to 2) to change
        display_name : The display name of the requested data series
        """

        get_module_logger().info("Changing subplot %d to %s", subplot_index, display_name)

        self.plotter.set_visibility(subplot_index, display_name != "None")
        self.gui.set_displayed_field(display_name, subplot_index)

        self.gui.set_dataset_choices(self.data_manager.get_numeric_display_names())

        if display_name != "None":
            self.plotter.set_dataset(
                self.data_manager.get_timestamps(display_name), self.data_manager.get_dataset(display_name),
                display_name, subplot_index)

        self.gui.draw(self.plotter)

    def action_average_data(self):

        """ Handles request to show the average of a dataset """

        # Get the dataset of interest
        display_name = self.gui.get_selected_dataset_name()

        # Get the time period over which to average
        try:
            time_period = self.gui.get_averaging_time_period()
        except ValueError:
            return # Could not convert time period to float

        if time_period == 0:
            return # Cannot average over zero time!

        # Get the units the time period is in (seconds, minutes etc.)
        time_units = self.gui.get_averaging_time_units()

        get_module_logger().info("Averaging %s over %d %s", display_name, time_period, time_units.lower())

        time_multipliers = {"Seconds":1, "Minutes":60, "Hours":60*60, "Days":24*60*60, "Weeks":7*24*60*60}

        time_period_seconds = time_period * time_multipliers[time_units]

        (data, timestamps) = self.data_manager.get_dataset_average(display_name, time_period_seconds)

        index = self.gui.get_index_of_displayed_plot(display_name)

        self.plotter.set_dataset(timestamps, data, display_name, index)

        self.gui.draw(self.plotter)

    def reset_average_data(self):

        """ Get the dataset of interest and reset the original data """

        display_name = self.gui.get_selected_dataset_name()
        subplot_index = self.gui.get_index_of_displayed_plot(display_name)

        get_module_logger().info("Resetting dataset %s on subplot %d", display_name, subplot_index)

        self.plotter.set_dataset(
            self.data_manager.get_timestamps(display_name), self.data_manager.get_dataset(display_name),
            display_name, subplot_index)

        self.gui.draw(self.plotter)

    def action_new_data(self):

        """ Handles request to show open a new set of CSV files """

        new_directory = ask_directory("Choose directory to process")

        if new_directory != '' and DataManager.directory_has_data_files(new_directory):
            get_module_logger().info("Parsing directory %s", new_directory)
            self.gui.reset_and_show_progress_bar(new_directory)

            self.msg_queue = queue.Queue()
            self.data_manager = DataManager(self.msg_queue, new_directory)
            self.data_manager.start()

            self.loading_timer = threading.Timer(0.1, self.check_data_manager_status)
            self.loading_timer.start()

    def check_data_manager_status(self):

        """ When the data manager is loading new data, updates the progress bar """

        dataloader_finished = False
        try:
            msg = self.msg_queue.get(0)
            if msg == 100:
                dataloader_finished = True
                self.gui.hide_progress_bar()
                self.plot_default_datasets()
            else:
                self.gui.set_progress_percent(msg)
        except queue.Empty:
            pass
        except:
            raise

        if not dataloader_finished:
            self.loading_timer = threading.Timer(0.1, self.check_data_manager_status)
            self.loading_timer.start()

    def action_special_option(self):

        """ Handles requests for special options
        e.g. histogram, windrose plot """

        action = self.gui.get_special_action()

        if action == "Windrose":

            get_module_logger().info("Plotting windrose")
            self.gui.add_new_window('Windrose', (7, 6))

            # Get the wind direction and speed data
            speed = self.data_manager.get_dataset('Wind Speed')
            direction = self.data_manager.get_dataset('Direction')

            self.windplotter.set_data(speed, direction)

            # Add window and axes to the GUI
            try:
                self.gui.draw(self.windplotter, 'Windrose')
            except Exception as exc: #pylint: disable=broad-except
                get_module_logger().info("Could not plot windrose (%s)", exc)
                show_info_dialog(
                    "Could not plot windrose - check that the windspeed and direction data are valid")

        elif action == "Histogram":
            get_module_logger().info("Plotting histogram")
            self.gui.add_new_window('Histogram', (7, 6))

            # Get the windspeed data
            speed = self.data_manager.get_dataset('Wind Speed')

            self.histogram.set_data(speed)

            # Add window and axes to the GUI
            self.gui.draw(self.histogram, 'Histogram')

    def get_special_dataset_options(self, dataset):
        """ Callback fron other modules to get the special dataset names (via data manager) """
        return self.data_manager.get_special_dataset_options(dataset)

    def plot_default_datasets(self):

        """ Plots the default set of data (from configuration file) """

        self.plotter.clear_data()

        # Get the default fields from config
        default_fields = self.config['DEFAULT']['DefaultFields']
        default_fields = [field.strip() for field in default_fields.split(",")]

        # Drawing mutiple plots, so turn off drawing until all three are processed
        self.plotter.suspend_draw(True)

        field_count = 0
        numeric_fields = self.data_manager.get_numeric_field_names()
        for field in default_fields:
            if field in numeric_fields:
                display_name = self.data_manager.get_display_name(field)
                self.action_subplot_change(field_count, display_name)
                field_count += 1

        # Now the plots can be drawn
        self.gui.set_dataset_choices(self.data_manager.get_numeric_display_names())
        self.plotter.suspend_draw(False)
        self.gui.draw(self.plotter)

def main():

    """ Application start """

    logging.basicConfig(level=logging.INFO)

    get_module_logger().setLevel(logging.INFO)

    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    conf_parser = configparser.RawConfigParser()
    conf_parser.read_file(codecs.open("config.ini", "r", "utf8"))

    app = Application(args, conf_parser)
    
    # The call to run() does not return.
    # All events are handled via GUI handlers and application callbacks.
    run_gui()

if __name__ == "__main__":
    main()

