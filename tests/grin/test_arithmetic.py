# test_arithmetic.py
# unittest for the class Arithmetic (From calculate/arithmetic.py)

from grin.arithmetic import Arithmetic
from grin.variable_list import VariableList
from grin.parsing import parse
import unittest
from collections import defaultdict

class TestArithmetic(unittest.TestCase):
    def test_add_value(self):
        varlist = defaultdict(int)
        varlist['A'] = 11
        varlist['B'] = 11.5
        varlist['C'] = 11
        varlist['D'] = 11.5
        varlist['E'] = "985"
        lines = [
            'ADD A 7',
            'ADD B 7.0',
            'ADD C 7.5',
            'ADD D 7',
            'ADD E "211"',
        ]
        VL = VariableList(varlist)
        for line in parse(lines):
            Arithmetic(VL, line).calculate()
        self.assertEqual(
            list(VL.variable_list.items()),
            [('A', 18), ('B', 18.5), ('C', 18.5), ('D', 18.5), ('E', "985211"), ]
        )