# compare.py
# Do the compare operations in Grin, and process the Exception

# *example1: 1 > 2, is False
# *example2: 2 == 4, is False
# *example3: 1 > "USA", this is a RuntimeError, will be processed.

from grin.token import *
from grin.variable_list import *


def compare(if_line: list[GrinToken], VL: VariableList):
    """return
        * a bool value of value1 op value2
        * or -1 if there is a RuntimeError
    Args:
        if_line (list[GrinToken]): ths GrinToken list of "IF value1 op value2"
    Returns:
        int: a bool value of value1 op value2 or -1 if there is a RuntimeError
    """
