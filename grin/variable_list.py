# variable_list.py
# define a dictionary to store the value of variable

# *example: VariableList.variable_list =
#           {"A": 1,
#            "B": 0.985,
#            "C": "USA"}
# It means that there is 3 variables, and A = 1, B = 0.985, C = "USA"

from collections import defaultdict


class VariableList:
    def __init__(self, _varlist_ = None):
        self.variable_list = defaultdict(int)
        if _varlist_ is not None:
            self.variable_list = _varlist_
