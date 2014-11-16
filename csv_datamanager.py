"""
csv_datamanager.py

@author: James Fowkes

Datamanger class for data from CSV files
"""

import pandas as pd
import os
import logging

from csv_special_fields import CSV_Windspeed, CSV_Humidity, CSV_WindDirection

special_fields = {
    "Humidity" : CSV_Humidity("Humidity"),
    "Wind Pulses" : CSV_Windspeed("Wind Pulses",  0.7),
    "Direction" : CSV_WindDirection("Direction")
}

def valid_filename(filename):
    return filename.lower().endswith(".csv")

def get_module_logger():

    """ Returns logger for this module """
    return logging.getLogger(__name__)
    
class CSV_DataManager:
    
    def __init__(self, folder = None):
        self.folder = folder
        if self.folder is not None:
            self.parse()
            
    def preprocess_folder(self):
        self.filenames = []
        for filename in os.listdir(self.folder):
            if valid_filename(filename):
                self.filenames.append(filename)
                
    def parse(self, folder):
        """
        Parse the file with pandas
        Use columns 1 and 2 to get datetime from
        This creates a new column 0, which is the combined datetime used as index
        """
        
        self.folder = folder
        self.preprocess_folder()
               
        frames = []
        
        for fcount, filename in enumerate(self.filenames):
            
            # Create a dataframe for each CSV file and append to the frames list
            
            full_path = os.path.join(self.folder, filename)
            df = pd.read_csv(full_path, parse_dates = [[1,2]], dayfirst=True, index_col = 0)
            frames.append(df)
            
        # All dataframes created, now merge them and sort by time
        data = pd.concat(frames)
        data.sort_index(inplace=True)
        
        # Strip any whitespace from the column names
        data.rename(columns=lambda x: x.strip(), inplace=True)
        
        # Split data into seperate dataframes (ignoring reference field)
        column_names = list(data.columns.values)[1:]
        self.dataframes = {}
        for col in column_names:
            self.dataframes[col] = pd.DataFrame(data[col], index=data.index)

        # Apply any special data conversions
        for key, dataframe in self.dataframes.items():
            try:
                self.dataframes[key] = special_fields[key].convert(dataframe)
                get_module_logger().info("Applied special conversion to field '%s'", key)
            except KeyError:
                pass # No special field exists for this data
            except:
                raise
            
        # The fields are fixed, so save them to a member now rather than compute each time
        self._set_fieldnames(column_names)
        
        # Can also get numeric fieldnames now
        self._set_numeric_fields()
    
    def get_timestamps(self, display_name):
        """ Return timestamps (the dataframe index) for the requested series """
        field_name = self._display_to_field_dict[display_name]
        return self.dataframes[field_name].index

    def has_dataset(self, display_name):
        """ Return true if dataset with this name exists in datasets """
        return display_name in self._display_to_field_dict.keys()
    
    def get_dataset(self, display_name):
        """ Return data for the requested series """
        field_name = self._display_to_field_dict[display_name]
        return self.dataframes[field_name][field_name].values
    
    def get_dataset_average(self, display_name, average_time_seconds):
        """ Use resampling functionality to get average of dataset over requested number of seconds """
        field_name = self._display_to_field_dict[display_name]
        resampled_data = self.dataframes[field_name].resample("%dS" % average_time_seconds, how='mean')
        # Resampled data is placed at start of time periods. Re-index to middle of periods.
        new_index = resampled_data.index + timedelta(seconds = average_time_seconds/2)
        resampled_data.index = new_index
        
        return (list(resampled_data[field_name].values), list(resampled_data[field_name].index))
        
    def _set_fieldnames(self, names):
        # Get a set of display names from field names
        self._field_to_display_dict = {}
        self._display_to_field_dict = {}
        for name in names:
            try:
                display_name = special_fields[name].display_name
                self._field_to_display_dict[name] = display_name
                self._display_to_field_dict[display_name] = name
            except KeyError: # Special field does not exist for this field
                self._field_to_display_dict[name] = name
                self._display_to_field_dict[name] = name
                
    def _set_numeric_fields(self):
        """ Set field names of fields that can be considered numeric data """        
        
        # Datatype can be considered numeric if its kind is one of b,i,u,f,c
        # These are numpy kinds (see http://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html)
        # (boolean, integer, unsigned, float, complex)
        
        frames = [dataframe for (key, dataframe) in self.dataframes.items() if dataframe[key].dtype.kind in 'biufc']

        self._numeric_fields = [list(frame.columns.values)[0] for frame in frames]
        
    def get_special_dataset_options(self, dataset):
        field_name = self._display_to_field_dict[dataset]
        try:
            special_field = special_fields[field_name]
            return special_field.capabilities()
        except KeyError:
            raise#return None
        except:
            raise
            
    def get_numeric_display_names(self):
        """ Return display names of fields that can be considered numeric data """        
        return [self._field_to_display_dict[key] for key in self._numeric_fields]
        
    def get_numeric_field_names(self):
        """ Return display names of fields that can be considered numeric data """        
        return self._numeric_fields.copy()
        
    def get_field_name_from_display_name(self, display_name):
        """ For a given "nice" display name from special field return the field name (from CSV file) """ 
        return self._display_to_field_dict[display_name]
    
    def get_display_name(self, field_name):
        """ Returns the display name associated with a field name """
        return self._field_to_display_dict[field_name]
        
    @staticmethod
    def directory_has_data_files(directory):
        """ Returns True if directory has at least one .csv or .CSV file """
        return True in [".csv" in filename.lower() for filename in os.listdir(directory)]
    