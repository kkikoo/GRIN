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
    op = if_line[2].kind
    value1 = if_line[1]
    value2 = if_line[3]
    # value1, may be a var
    if value1.value == value1.text:
        value1 = VL.variable_list[value1.value]
    else:
        value1 = if_line[1].value

    # value2, may be a var
    if value2.value == value2.text:
        value2 = VL.variable_list[value2.value]
    else:
        value2 = if_line[3].value
    # print(value1,value2)
    Tag = True
    try:
        if op == GrinTokenKind.EQUAL:
            Tag = (value1 == value2)
        if op == GrinTokenKind.NOT_EQUAL:
            Tag = (value1 != value2)
        if op == GrinTokenKind.LESS_THAN:
            Tag = value1 < value2
        if op == GrinTokenKind.LESS_THAN_OR_EQUAL:
            Tag = value1 <= value2
        if op == GrinTokenKind.GREATER_THAN:
            Tag = value1 > value2
        if op == GrinTokenKind.GREATER_THAN_OR_EQUAL:
            Tag = value1 >= value2
    except:
        Tag = -1
    return Tag


