"""
csv_special_fields.py

@author: James Fowkes

Classes to perform special modifications to data
"""
import datetime

class CSV_SpecialField:
    
    """
    Base class ("interface") for a special field
    """
    
    def __init__(self, field_name, display_name):
        self.field_name = field_name
        self.display_name = display_name
        
    def convert(self, data, times):
        pass

class CSV_Humidity(CSV_SpecialField):
    
    def __init__(self, field_name):
        CSV_SpecialField.__init__(self, field_name, "Humidity")
        
    def convert(self, data, times):
        
        # Humidity comes in as decimal from 0 to 1.0. Convert to 0 to 100%
        new_data = [datum * 100 for datum in data ]
            
        return (new_data, times)
        
class CSV_Windspeed(CSV_SpecialField):
    
    def __init__(self, field_name, calibration_factor):
        self.factor = calibration_factor
        CSV_SpecialField.__init__(self, field_name, "Wind Speed")
        
    def convert(self, data, times):
        
        new_data = []
        new_timestamps = []
        previous_time = times[0]
        
        #Skip the first data point - we have no reference to how long it was counting for
        data = data[1:]
        times = times[1:]
        
        for (datum, time) in zip(data, times):
            period = (time - previous_time).seconds
            previous_time = time
            new_data.append(self.factor * datum / period)
            new_timestamps.append(previous_time + datetime.timedelta(seconds = period/2))
            
        return (new_data, new_timestamps)
