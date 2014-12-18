"""
csv_gui.py

@author: James Fowkes

Defines a GUI for the CSV viewer application

"""
import os
import sys
import logging

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

from matplotlib.figure import Figure

import tkinter as Tk
from tkinter import messagebox, filedialog, ttk

import app_info

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
        
class TkEntryHelper(Tk.Entry):
    def __init__(self, master, **kwargs):
        self.var = Tk.StringVar(master)
        Tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        
class CSV_GUI:

    def __init__(self, application):
        
        self.application = application
        self.title = app_info.TITLE
        self.root = Tk.Tk()
        
        # Note: keeping PhotoImage in self.icon stops it being garbage collected.
        # Therefore, don't simplify these lines by getting rid of self.icon!
        self.icon = Tk.PhotoImage(file=os.path.join(app_info.app_dir(), "logo.png"))
        self.root.iconphoto(True, self.icon)
        
        self.root.wm_title(self.title)
        self.root.protocol("WM_DELETE_WINDOW", self._exit)
        
        get_module_logger().setLevel(logging.INFO)
        
        self.windows = {}
        self.frames = {}
        self.figures = {}
        self.canvases = {}
        self.toolbars = {}
        
        self.display_fields = [None, None, None]
        
        self.plot_picker_titles = ["Upper Plot Data", "Middle Plot Data", "Lower Plot Data"]
        self.subplot_actions = [
            self.application.action_subplot1_change,
            self.application.action_subplot2_change,
            self.application.action_subplot3_change
        ]
        
        self.ui_exists = False
        
        self.add_new_window('Main', (8,5))
        self.add_interface()
        
    def reset_data_loading_bar(self, folder):
        self.add_new_window("Progress Bar", (5, 0.5), False, False) 
 
        self.progress_bar_label = Tk.Label(self.windows["Progress Bar"], text= "Loading from folder '%s'" % folder)
        self.progress_bar_var = Tk.IntVar()
        self.progress_bar = ttk.Progressbar(
            self.windows["Progress Bar"],
            orient="horizontal", length="5i", mode="determinate",
            variable = self.progress_bar_var)
        
        self.progress_bar_label.pack()
        self.progress_bar.pack()
        
    def set_data_load_percent(self, pc):
        self.progress_bar_var.set(pc)
    
    def hide_progress_bar(self):
        self.kill_window("Progress Bar")
        
    def kill_window(self, window):
        try:  
            self.windows["Progress Bar"].destroy()
        except KeyError:
            pass

    def add_new_window(self, key, size, add_figure = True, add_nav_toolbar = True):
        """ Adds a new Tk window, overwriting if the key already exists """
        window = self.root if key == "Main" else Tk.Toplevel(self.root)
        self.windows[key] = window
        self.frames[key] = Tk.Frame(window)
        if add_figure:
            self.figures[key] = Figure(figsize=size, dpi=100)
            
            self.canvases[key] = FigureCanvasTkAgg(self.figures[key], master=window)           
            self.canvases[key].get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
            if add_nav_toolbar:
                self.toolbars[key] = NavigationToolbar2TkAgg( self.canvases[key], window )
                self.toolbars[key].update()
                
    def get_figure(self, key):
        """ Returns a handle to the requested figure (None if key does not exist) """
        try:
            return self.figures[key]
        except KeyError:
            return None
            
    def set_displayed_field(self, display_name, index):
        get_module_logger().info("Setting subplot %d to %s", index, display_name)
        self.display_fields[index] = display_name   
        
    def ask_directory(self, title):
        """ Brings up Tk askdirectory window and if there are valid files, redraws plot """
        return filedialog.askdirectory(title = title)
        
    def add_interface(self):
        self.app_frame = Tk.Frame(self.root, bd=1, relief=Tk.SUNKEN)
        self.control_frame = Tk.Frame(self.root, bd=1, relief=Tk.SUNKEN)
        
        self.plot_select_frame = Tk.Frame(self.control_frame)
        self.data_control_frame = Tk.Frame(self.control_frame)
        
        self.new_data_button = Tk.Button(self.app_frame, text='Open CSV Folder', command=self.application.action_new_data)
        self.new_data_button.pack(padx=10, pady=10)
        
        self.about_button = Tk.Button(self.app_frame, text='About CSV Viewer', command=self.application.action_about_dialog)
        self.about_button.pack(padx=10, pady=10)
        
        self.exit_button = Tk.Button(self.app_frame, text='Exit', command=self._exit)
        self.exit_button.pack(padx=10, pady=10)
        
        self.control_frame.pack(side=Tk.LEFT, padx=10, pady=10)
        self.app_frame.pack(side=Tk.RIGHT, padx=10, pady=10)
        self.plot_select_frame.pack()
        self.data_control_frame.pack()

    def refresh_subplot_lists(self, datasets):
        """ When a plot changes, this function produces new lists for each plot's dropdown menu 
        The dropdown menus have a selection of all datasets EXCEPT that currently shown for that plot,
        plus there's a "None" entry to hide the plot """
        
        datasets.append("None")
        self.subplot_lists = [[dataset for dataset in datasets if dataset != self.display_fields[i]] for i in range(3)]
    
    def get_selected_dataset_displayname(self):
        return self.dataset_picker.var.get()
    
    def get_averaging_time_period(self):
        return float(self.dataset_average_text_entry.var.get())      
    
    def get_averaging_time_units(self):
        return self.dataset_average_period_picker.var.get()

    def get_special_action(self):
        return self.dataset_special_option_picker.var.get()
        
    def set_dataset_choices(self, datasets):
        """ Sets the list of possible datasets that can be selected for each plot """

        get_module_logger().info("Setting dataset choices %s", ','.join(datasets))
        
        if not self.ui_exists:
            self._draw_ui()

        self.refresh_subplot_lists(datasets)
        self.dataset_picker.set_options(self.display_fields)
        
        for (i, picker) in enumerate(self.subplot_pickers):
            picker.set_options(self.subplot_lists[i])

    def change_dataset_selection(self, selection):
        special_options_list = self.application.get_special_dataset_options(selection)
        if special_options_list is not None:
            self.dataset_special_option_picker.set_options(special_options_list)
            self.dataset_special_option_picker.pack(side=Tk.LEFT, padx=2, pady=2)
            self.dataset_special_option_button.pack(side=Tk.LEFT, padx=2, pady=2)
        else:
            self.dataset_special_option_picker.pack_forget()
            self.dataset_special_option_button.pack_forget()
            
    def _draw_ui(self):
        # This is the first time drawing the full UI
        self.ui_exists = True
        
        self.control_frames = [Tk.Frame(self.data_control_frame), Tk.Frame(self.data_control_frame), Tk.Frame(self.data_control_frame)]
        
        self.dataset_picker = TkOptionMenuHelper(self.control_frames[1], "Select dataset", ["Select dataset"], command=self.change_dataset_selection)  
        self.dataset_average_period_label = Tk.Label(self.control_frames[1], text="Average every:")
        self.dataset_average_text_entry = TkEntryHelper(self.control_frames[1], width=10)
        self.dataset_average_period_picker = TkOptionMenuHelper(self.control_frames[1], "Seconds", ["Seconds", "Minutes", "Hours", "Days", "Weeks"], command=None, width=10)
        self.dataset_average_button = Tk.Button(self.control_frames[1], text='Apply', command=self.application.action_average_data)
        self.dataset_average_reset_button = Tk.Button(self.control_frames[1], text='Reset', command=self.application.reset_average_data)
        
        self.dataset_special_option_picker = TkOptionMenuHelper(self.control_frames[2], "Special Options", ["Special Options"], command = None)
        self.dataset_special_option_button = Tk.Button(self.control_frames[2], text='Show', command=self.application.action_special_option)
        
        self.dataset_picker.pack(side=Tk.LEFT, padx=2, pady=2)
        self.dataset_average_period_label.pack(side=Tk.LEFT, padx=2, pady=2)
        self.dataset_average_text_entry.pack(side=Tk.LEFT, padx=2, pady=2)
        self.dataset_average_period_picker.pack(side=Tk.LEFT, padx=2, pady=2)
        self.dataset_average_button.pack(side=Tk.LEFT, padx=2, pady=2)
        self.dataset_average_reset_button.pack(side=Tk.LEFT, padx=2, pady=2)
        
        for frame in self.control_frames:
            frame.pack(side=Tk.TOP, padx=3, pady=3)
        
        # Subplot dataset pickers and label
        self.subplot_picker_label = Tk.Label(self.plot_select_frame, text="Select plots:")
        self.subplot_pickers = [TkOptionMenuHelper(self.plot_select_frame, self.plot_picker_titles[i], [self.plot_picker_titles[i]], command=self.subplot_actions[i]) for i in range(3)]
        
        self.subplot_picker_label.pack(side=Tk.LEFT)
        for picker in self.subplot_pickers:
            picker.pack(side=Tk.LEFT)
            
    def get_index_of_displayed_plot(self, display_name):
        """ Returns the subplot index (0 to 2) of the plot with the requested display name (None if name is not displayed) """
        try:
            return self.display_fields.index(display_name)
        except:
            return None
            
    def draw(self, plotter, figure_key='Main'):
        """ Draw the supplied plot on the figure with the supplied key """
        plotter.draw(self.figures[figure_key])
        self.canvases[figure_key].draw()

    def show_info_dialog(self, text):
        messagebox.showinfo(self.title, text)
        
    def _exit(self):
        if messagebox.askyesno(self.title, "Exit %s?" % self.title):
            self.root.quit()
            if os.name=="nt":
                self.root.destroy()  # this is necessary on Windows to prevent "Fatal Python Error: PyEval_RestoreThread: NULL tstate"
            
    def run(self):
        Tk.mainloop()