"""
csv_error.py

@author: James Fowkes

Defines an error class for the application
"""

class CSVError(Exception):
    def __init__(self, msg, expr):
        self.msg = msg
        self.expr = expr
    def __str__(self):
        return self.msg + "(" + expr + ")"
