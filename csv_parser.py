"""
csv_parser.py

@author: James Fowkes

Parser class for a folder of CSV files and associated utility functions
"""

import csv
import os 

from datetime import datetime

def valid_filename(filename):
    return filename.lower().endswith(".csv") and filename.startswith("D")

def valid_file_header(fields):
    return (fields[0].strip() == "Reference") and (fields[1].strip() == "Date") and (fields[2].strip() == "Time")

def date_time_fields_to_timestamp(date_field, time_field):
    
    date_time_field = date_field.strip() + " " + time_field.strip()
    
    return datetime.strptime(date_time_field, "%d-%m-%Y %H:%M:%S")
    
class InvalidCSVException(Exception):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg
        
class ProgressBar:

    def __init__(self):
        self.pc = 0
        self.next = 10
        
    def set_new_pc(self, pc):
        self.pc = pc
        if self.pc > self.next:
            self.next = min(self.next + 10, 100)
            print("%d%%..." % self.pc)
            
class CSV_Parser:

    """
    Implementation of the Parser class - 
    When provided with a folder path at instantiation or with set_folder method
    Immediately parses the CSVs in that folder and attempts to build consistent data from them
    """
    
    def __init__(self, folder):
    
        self.folder = folder
        self.ids = []
        self.timestamps = []
        self.fields = []
        self.first_file = True
        self.parse_all_files()    
    
    def preprocess_folder(self):
        self.filenames = []
        for filename in os.listdir(self.folder):
            if valid_filename(filename):
                self.filenames.append(filename)
        
    def parse_all_files(self):
        """
        Parses all the files in the current folder into lists
        Checks filename validity before parsing
        """
        self.record_counts = []
            
        # Read in data (unsorted, any potential order)
        self.preprocess_folder()
        
        print("Parsing data...")
        progress_bar = ProgressBar()
        
        for fcount, filename in enumerate(self.filenames):
            full_path = os.path.join(self.folder, filename)
            record_count = self.parse_file(full_path)
            self.record_counts.append(record_count)
            progress_bar.set_new_pc(fcount * 100 / len(self.filenames))
            
        # Sort in time order
        for idx, dataset in enumerate(self.data):
            timestamped_data = list(zip(self.timestamps, dataset))
            sorted_data = sorted(timestamped_data, key = lambda data: data[0])
            self.data[idx] = [data[1] for data in sorted_data]
        
        # Then sort the timestamps themselves
        self.timestamps = sorted(self.timestamps)
        
    def set_fields(self, fields):
        """
        Sets the header fields for this dataset.
        Strips whitespace and checks validity before setting 
        """
        fields = [field.strip() for field in fields]
        if valid_file_header(fields):
            self.fields = fields
            self.field_count = len(fields) - 3
        else:
            raise InvalidCSVException("", "Unexpected headers")
            
    def parse_file(self, path):
        with open(path, newline='') as f:
            reader = csv.reader(f)
            
            
            ## Get the header line
            self.set_fields( next(reader) )
            
            if self.first_file:
                self.first_file = False
                ## Now field count is known, store data as list of lists (one list per field)
                self.data = [ [] for i in range(self.field_count) ]
                                
            record_count = 0
            ## Then iterate over the rest of the data
            while True:
                try:
                    data = next(reader)
                    record_count += 1
                    self.parse_record(data)
                except StopIteration:
                    break ## End of data for this file, quit loop
        
        return record_count
    
    def get_dataset(self, field):
        try:
            idx = self.fields.index(field)
        except ValueError:
            raise
    
        return self.data[idx-3]
        
    def parse_record(self, record):
        
        self.ids.append(record[0])
        self.timestamps.append(date_time_fields_to_timestamp(record[1], record[2]))
        
        for count, record_data in enumerate(record[3:]):
            # Try to convert data to a float before storing
            try:
                record_data = float(record_data)
            except:
               pass # If it doesn't work just assume it's text and carry on
            
            self.data[count].append(record_data)
            
    def print_all_data(self):
        """ Only really for debugging. Blurt out all the data in the parser """
        print("\t".join(self.fields))
        
        for data in zip(self.ids, self.timestamps, *self.data):
            data_string = "\t".join([str(d) for d in data[2:]])
            print("%s\t%d\t%s" % (data[0], data[1], data_string))
    
    @property
    def file_count(self):
        """ Return the total number of files parsed """
        return len(self.filenames)
    
    @property    
    def record_count(self):
        """ Return the total number of records parsed """
        return sum(self.record_counts)