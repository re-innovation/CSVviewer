"""
csv_gui.py

@author: James Fowkes

Defines a GUI for the CSV viewer application

"""
import os
import logging

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

from matplotlib.figure import Figure

import tkinter as Tk
from tkinter import messagebox, filedialog

APP_TITLE = "CSV Viewer"

def get_module_logger():

    """ Returns logger for this module """
    return logging.getLogger(__name__)
    
class TkOptionMenuHelper(Tk.OptionMenu):
    def __init__(self, master, title, options, command, width=15):
        self.master = master
        self.title = title
        self.application_callback = command
        self.width = width
        
        self.var = Tk.StringVar(master)
        self.var.set(title)
        
        Tk.OptionMenu.__init__(self, master, self.var, *options, command=self.on_var_change)
        self.config(width=width)
        
    def on_var_change(self, new_var):
        if new_var != self.title:
            self.var.set(new_var)
            if self.application_callback is not None:
                self.application_callback(new_var)
            
    def set_options(self, new_options):
        """ Sets new menu options. """
        
        self['menu'].delete(0, "end")
        for opt in new_options:
            self['menu'].add_command(label=opt, command=lambda val=opt: self.on_var_change(val))
        self.var.set(self.title)
        
        #Tk.OptionMenu.__init__(self, self.master, self.var, *new_options, command=self.application_callback)
        #self.config(width=self.width)
        
class TkEntryHelper(Tk.Entry):
    def __init__(self, master):
        self.var = Tk.StringVar(master)
        Tk.Entry.__init__(self, master, textvariable=self.var)
        
class CSV_GUI:

    def __init__(self, application):
        self.root = Tk.Tk()
        self.root.wm_title(APP_TITLE)
        self.root.protocol("WM_DELETE_WINDOW", self._exit)
        
        get_module_logger().setLevel(logging.INFO)
        
        self.application = application
        self.display_fields = [None, None, None]
        
        self.plot_picker_titles = ["Upper Plot Data", "Middle Plot Data", "Lower Plot Data"]
        self.subplot_actions = [
            self.application.action_subplot1_change,
            self.application.action_subplot2_change,
            self.application.action_subplot3_change
        ]
        
        self.ui_exists = False
        
        self.add_figure()
        self.add_interface()
    
    def set_displayed_field(self, display_name, index):
        get_module_logger().info("Setting subplot %d to %s", index, display_name)
        self.display_fields[index] = display_name
        
    def ask_directory(self, title):
        """ Brings up Tk askdirectory window and if there are valid files, redraws plot """
        return filedialog.askdirectory(title = title)
        
    def add_figure(self):
        self.f = Figure(figsize=(8,5), dpi=100)

        self.canvas = FigureCanvasTkAgg(self.f, master=self.root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        
        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.root )
        self.toolbar.update()
        
        self.canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    def add_interface(self):
        self.app_frame = Tk.Frame(self.root)
        self.control_frame = Tk.Frame(self.root)
        
        self.plot_select_frame = Tk.Frame(self.control_frame)
        self.data_control_frame = Tk.Frame(self.control_frame)
        
        self.new_data_button = Tk.Button(self.app_frame, text='Open CSV Folder', command=self.application.action_new_data)
        self.new_data_button.pack(padx=10, pady=10)
        
        self.exit_button = Tk.Button(self.app_frame, text='Exit', command=self._exit)
        self.exit_button.pack(padx=10, pady=10)
        
        self.control_frame.pack(side=Tk.LEFT, padx=10, pady=10)
        self.app_frame.pack(side=Tk.RIGHT, padx=10, pady=10)
        self.plot_select_frame.pack()
        self.data_control_frame.pack()

    def refresh_subplot_lists(self, datasets):
        datasets.append("None") #Each list also needs a "None" selection to hide the plot
        self.subplot_lists = [[dataset for dataset in datasets if dataset != self.display_fields[i]] for i in range(3)]
    
    def get_averaging_displayname(self):
        return self.dataset_average_picker.var.get()
        
    def get_averaging_time_period(self):
        return float(self.dataset_average_text_entry.var.get())      
    
    def get_averaging_time_units(self):
        return self.dataset_average_period_picker.var.get()
        
    def set_dataset_choices(self, datasets):
        """ Sets the list of possible datasets that can be selected for each plot """
        
        get_module_logger().info("Setting dataset choices %s", ','.join(datasets))
        
        if not self.ui_exists:
            self.ui_exists = True
            
            self.control_frames = [Tk.Frame(self.data_control_frame), Tk.Frame(self.data_control_frame)]
            
            self.control_frame_label = Tk.Label(self.control_frames[0], text="Dataset Averaging")                    
            
            self.dataset_average_picker = TkOptionMenuHelper(self.control_frames[1], "Select dataset", datasets, command=None)  
            self.dataset_average_period_label = Tk.Label(self.control_frames[1], text="Average every:")
            self.dataset_average_text_entry = TkEntryHelper(self.control_frames[1])
            self.dataset_average_period_picker = TkOptionMenuHelper(self.control_frames[1], "Seconds", ["Seconds", "Minutes", "Hours", "Days", "Weeks"], command=None, width=10)
            self.dataset_average_button = Tk.Button(self.control_frames[1], text='Apply', command=self.application.action_average_data)

            self.dataset_average_picker.pack(side=Tk.LEFT, padx=2, pady=2)
            self.dataset_average_period_label.pack(side=Tk.LEFT, padx=2, pady=2)
            self.dataset_average_text_entry.pack(side=Tk.LEFT, padx=2, pady=2)
            self.dataset_average_period_picker.pack(side=Tk.LEFT, padx=2, pady=2)
            self.dataset_average_button.pack(side=Tk.LEFT, padx=2, pady=2)
            
            self.control_frame_label.pack(side=Tk.LEFT, padx=3, pady=3)
            
            for frame in self.control_frames:
                frame.pack(side=Tk.TOP, padx=3, pady=3)
            
            self.refresh_subplot_lists(datasets)
                
            self.subplot_pickers = [TkOptionMenuHelper(self.plot_select_frame, self.plot_picker_titles[i], self.subplot_lists[i], command=self.subplot_actions[i]) for i in range(3)]
            
            for picker in self.subplot_pickers:
                picker.pack(side=Tk.LEFT)

        else:
            self.refresh_subplot_lists(datasets)
            self.dataset_average_picker.set_options(datasets)
            
            for (i, picker) in enumerate(self.subplot_pickers):
                picker.set_options(self.subplot_lists[i])
                
    def draw(self, plotter):
        plotter.draw(self.f)
        self.canvas.draw()
        
    def _exit(self):
        if messagebox.askyesno(APP_TITLE, "Exit %s?" % APP_TITLE):
            self.root.quit()
            if os.name=="nt":
                self.root.destroy()  # this is necessary on Windows to prevent "Fatal Python Error: PyEval_RestoreThread: NULL tstate"
            
    def run(self):
        Tk.mainloop()