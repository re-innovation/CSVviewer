"""
csv_error.py

@author: James Fowkes

Defines an error class for the application
"""

class CSVError(Exception):
    def __init__(self, msg, expr = None):
        self.msg = msg
        self.expr = expr
    def __str__(self):
        if self.expr is not None:
            return self.msg + "(" + expr + ")"
        else:
            return self.msg
