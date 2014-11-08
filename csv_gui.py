"""
csv_gui.py

@author: James Fowkes

Defines a GUI for the CSV viewer application

"""

import wx

APP_TITLE = "CSV Viewer"

class Actions:
    EXIT = 0
    SHOW_SERIES = 1
    HIDE_SERIES = 2
    
class ApplicationFrame(wx.Frame):

    title = APP_TITLE
    
    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title)
        self.draw_figure()

    def create_menu(self):
        self.menubar = wx.MenuBar()
        
        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        
        menu_help = wx.Menu()
        m_about = menu_help.Append(-1, "&About\tF1", "About the demo")
        self.Bind(wx.EVT_MENU, self.on_about, m_about)
        
        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_help, "&Help")
        self.SetMenuBar(self.menubar)
        
class CSV_GUI:

    def __init__(self, wx_app, action_handler):
        self.frame = ApplicationFrame()
        
        self.plotter = CSV_Plotter(self.app)
        self.plotter.set_no_data()
        
        self.action_handler = action_handler
        
        self.exit_frame = Frame(self.root)
        self.exit_frame.pack()
        
        exit_button = Button(self.exit_frame, text="Exit", command=self.confirm_exit)
        exit_button.pack()

    def run(self):
        self.frame.show()
        self.frame.MainLoop()
        
    def confirm_exit(self):
        if messagebox.askyesno(APP_TITLE, "Exit %s?" % APP_TITLE):
            self.action_handler(Actions.EXIT)
            