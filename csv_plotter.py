"""
plotter.py

@author: James Fowkes

Defines a data plotter for the CSV viewer application using 

"""

import matplotlib.pyplot as plt
#import wx

from matplotlib.figure import Figure
#from matplotlib.backends.backend_wxagg import figureCanvasWxAgg as FigCanvas, NavigationToolbar2WxAgg as NavigationToolbar
 
#matplotlib.use('WXAgg')

APP_TITLE = "CSV Viewer"
        
class DataSet:

    def __init__(self, ylabel, data, times):
        self.ylabel = ylabel
        self.data = data
        self.times = times
        
class CSV_Plotter:

    def __init__(self):
        self.first = True
        
        self.subfigure_count = 0
        self.subfigure_data = []
        
        plt.ion()
        
        #self.frame = ApplicationFrame()

    def add_dataset(self, times, dataset, axis_label):
        if self.subfigure_count < 3:
            
            self.subfigure_count += 1            
            self.subfigure_data.append(DataSet(axis_label, dataset, times))
            
    def close(self):
        plt.close()
        
    def show(self):
    
        plt.close('all')
        f, axarr = plt.subplots(self.subfigure_count)
        
        if self.subfigure_count == 1:
            axarr = [axarr]
                
        for idx in range(self.subfigure_count):
            axarr[idx].plot(self.subfigure_data[idx].times, self.subfigure_data[idx].data)
            axarr[idx].set_ylabel(self.subfigure_data[idx].ylabel)
        
        if self.first:
            self.first = False
            plt.show()
        else:
            plt.draw()
    