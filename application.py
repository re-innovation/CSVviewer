"""
application.py

@author: James Fowkes

Entry file for the CSV viewer application
"""

import sys
import argparse
import logging
import configparser
import codecs

from tkinter import *
from tkinter.filedialog import askdirectory

from csv_parser import CSV_Parser
#from csv_gui import CSV_GUI, Actions
from csv_plotter import CSV_Plotter

from menu import Menu, MenuOption

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

class Application:
    
    def __init__(self, args, config):
    
        ## Try to get a parser for the provided folder.
        ## The folder might not exist - in which case start application anyway
        ## and the user can select a folder from menus.
        
        self.parser = CSV_Parser(args.start_folder)
        self.config = config
        
        self.plotter = CSV_Plotter()
        
        self.menu = Menu()
        self.menu.add_title(['0'], "Main Menu")
        self.menu.add_options(['0'], 
            [
                MenuOption("Display graph", None, self.action_display_graph),
                MenuOption("Print data summary", None, self.action_print_summary),
                MenuOption("Exit", 'x', self.action_exit)
            ]
        )
        
        
        #self.wx_app = wx.PySimpleApp()
        #self.gui = CSV_GUI(self.wx_app, self.action_handler)
    
    def action_print_summary(self, menu_level):
        print("Current directory: %s" % self.parser.folder)
        print("Found %d valid .csv files" % self.parser.file_count)
        print("Total records: %d" % self.parser.record_count)
        print("Data fields:")
        for field in self.parser.fields:
            print("\t" + field)
        
    def action_display_graph(self, menu_level):
        self.display_graph = True
        
    def action_exit(self, menu_level):
            self.plotter.close()
            sys.exit(0)
          
    def get_and_process_menu_input(self):
        self.menu.print_title()
        self.menu.print_menu()
        
        next_input = input()
        self.menu.process_input(next_input)
        
    def run(self):
        self.display_graph = False
        
        # Display the default fields
        default_fields = self.config['DEFAULT']['DefaultFields']
        default_fields = [field.strip() for field in default_fields.split(",")]
        
        # Read in any unit strings
        units = self.config['UNITS']
        
        for field in default_fields:
            if field in self.parser.fields:
                try:
                    label = field + " " + units[field].strip()
                except KeyError:
                    label = field
                    
                self.plotter.add_dataset(self.parser.timestamps, self.parser.get_dataset(field), axis_label = label)
                
        while True:
            self.get_and_process_menu_input()
            if self.display_graph:
                self.display_graph = False
                self.plotter.show()
        
def main():

    """ Application start """

    logging.basicConfig(level=logging.INFO)

    get_module_logger().setLevel(logging.INFO)

    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()
    
    conf_parser = configparser.ConfigParser()
    conf_parser.read_file(codecs.open("config.ini", "r", "utf8"))
    
    if args.start_folder is None:
        root = Tk()
        root.withdraw()
        args.start_folder = askdirectory()
        
    app = Application(args, conf_parser)
    
    app.run()
    
if __name__ == "__main__":
    main()
