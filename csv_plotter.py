"""
csv_plotter.py

@author: James Fowkes

Defines a data plotter for the CSV viewer application using 

"""

from numpy import arange, sin, pi

from windrose import WindroseAxes
    
class DataSet:

    def __init__(self, ylabel, data, times):
        self.ylabel = ylabel
        self.data = data
        self.times = times
        
class CSV_WindPlotter:

    def __init__(self):
        pass
    
    def set_data(self, speed, direction):
        self.ws = speed
        self.wd = direction
    
    def draw(self, f):
        self.ax = WindroseAxes(f, rect=[0.1, 0.1, 0.8, 0.8])
        f.add_axes(self.ax)
        self.ax.bar(self.wd, self.ws, normed=True)
        self.ax.set_title("Windrose (by % in 6 bins)")
        l = self.ax.legend(borderaxespad=-0.10, fontsize=8, bbox_to_anchor=(-0.2, 0))
        l.set_title("Wind Speed m/s", prop={"size":8})
        
class CSV_Plotter:

    def __init__(self, config):
        self.config = config
        self.suspend = False        
        self.clear_data()
    
    def suspend_draw(self, suspend):
        self.suspend = suspend
        
    def clear_data(self):
        self.subplot_visible = [False, False, False]
        self.subplot_data = [None, None, None]
    
    def apply_units_to_axis_label(self, label):
        # Get unit strings from config
        units = self.config['UNITS']
     
        try:
            #Try adding a unit to the field name
            label = label + " " + units[label].strip()
        except KeyError:
            pass #If no unit exists, just use the field name
        
        return label
        
    def set_dataset(self, times, dataset, axis_label, field_index):
        if field_index < 3:
            axis_label = self.apply_units_to_axis_label(axis_label)
            self.subplot_data[field_index] = DataSet(axis_label, dataset, times)
    
    def set_visibility(self, plot, show):
        self.subplot_visible[plot] = show
        
    def close(self):
        plt.close()
           
    def draw(self, f):
        
        if self.suspend:
            return # Drawing has been suspended
            
        f.clf()
        
        first_axis = None
        plot_count = 0
        for idx in range(3):
            if self.subplot_visible[idx]: #Only show visible plots
                a = f.add_subplot(self.visible_count, 1, plot_count+1, sharex=first_axis) #sharex parameter means axes will zoom as one w.r.t x-axis
                a.tick_params(axis='both', which='major', labelsize=10)
                a.plot(self.subplot_data[idx].times, self.subplot_data[idx].data)   
                a.set_ylabel(self.subplot_data[idx].ylabel, fontsize=10)
                
                #Save the first subplot so that other plots can share its x axis
                first_axis = a if idx == 0 else first_axis
                
                #Keep track of number of visible plots
                plot_count += 1
                
        f.autofmt_xdate() # Nice formatting for dates (diagonal, only on bottom axis)
        
    @property
    def visible_count(self):
        return self.subplot_visible.count(True)