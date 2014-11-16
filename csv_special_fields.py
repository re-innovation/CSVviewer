"""
csv_special_fields.py

@author: James Fowkes

Classes to perform special modifications to data
"""

import pandas as pd
import numpy as np

class CSV_SpecialField:
    
    """
    Base class ("interface") for a special field
    """
    
    def __init__(self, field_name, display_name):
        self.field_name = field_name
        self.display_name = display_name
        
    def convert(self, data, times):
        pass
    
    def capabilities(self):
        return None
        
class CSV_Humidity(CSV_SpecialField):
    
    def __init__(self, field_name):
        CSV_SpecialField.__init__(self, field_name, "Humidity")
        
    def convert(self, dataframe):
        
        # Humidity comes in as decimal from 0 to 1.0. Convert to 0 to 100%
        new_dataframe = dataframe * 100
        
        return new_dataframe
        
class CSV_Windspeed(CSV_SpecialField):
    
    def __init__(self, field_name, calibration_factor):
        self.factor = calibration_factor
        CSV_SpecialField.__init__(self, field_name, "Wind Speed")
        
    def convert(self, dataframe):

        # Convert timestamps to time deltas
        diffs = np.diff(dataframe.index)
        deltas_seconds = diffs/np.timedelta64(1, 's')
            
        # Use deltas to calculate windspeed
        windspeed = list(dataframe[self.field_name].values)
        
        # Apply the constant calibration factor
        windspeed = [pulses * self.factor for pulses in windspeed[1:]] 
        
        # Divide by the delta to get m/s
        speeds = [speed/delta for speed, delta in zip(windspeed, list(deltas_seconds))]
            
        # Need to re-index these data to time points in middle of timestamps
        old_timestamps = list(dataframe.index.values)[:-1]
        new_timestamps = old_timestamps + (diffs / 2) 
        return pd.DataFrame({self.field_name:speeds}, index=new_timestamps) 

    def capabilities(self):
        return ["Windrose", "Histogram"]
        
class CSV_WindDirection(CSV_SpecialField):
    
    def __init__(self, field_name):
        CSV_SpecialField.__init__(self, field_name, "Direction")

    def convert(self, dataframe):
        # Map cardinal points to degrees (generated random data for 'D' entry)
        map = {'N':0, 'NE':45, 'E':90, 'SE':135, 'S':180, 'SW':225, 'W':270, 'NW':315, 'D':lambda x: np.randint(0, 359)}
        dataframe = dataframe.replace({'Direction':map})
        
        # Drop first point (since this data will be plotted against windspeed which drops first point also)
        dataframe = dataframe.ix[1:]
        
        return dataframe