"""
menu.py

@author: James Fowkes

Handles command line menu processing for CSV viewer
"""

class MenuOption:

    def __init__(self, text, selector, action):
        self.text = text
        self.selector = selector
        self.action = action
        
    def print(self):
        print("%s: %s" % (self.selector, self.text))
    
    def action_on_match(self, selector):
        if selector == self.selector:
            self.action(selector)
            
class Menu:

    def __init__(self):
        self.level = ['0']
        self.titles = {}
        self.menu_items = {}
        
    def add_title(self, level_list, title):
        level_list = ''.join(level_list)
        self.titles[level_list] = title
        self.menu_items[level_list] = []
        
    def add_options(self, level_list, options):
        level_list = ''.join(level_list)
        for index, option in enumerate(options):
            if option.selector is None:
                option.selector = "%d" % index
                
            self.menu_items[level_list].append(option)
        
    def print_title(self):
        print("")
        print("--- " + self.titles[self._level_index] + " ---")
        
    def print_menu(self):
        for item in self.menu_items[self._level_index]:
            item.print()
            
    def process_input(self, input):
        try:
            for menu_item in self.menu_items[self._level_index]:
                menu_item.action_on_match(input)
        except KeyError:
            print("Option '%s' not recognised!" % input)
    
    def drop_to_level(self, level):
        self.level.append(level)
        self.print_title()
        self.print_menu()
        
    @property    
    def _level_index(self):
        return ''.join(self.level)