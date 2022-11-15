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

    def test_add_variable(self):
        varlist = defaultdict(int)
        varlist['A'] = 11
        varlist['B'] = 11.5
        varlist['C'] = 11
        varlist['D'] = 11.5
        varlist['E'] = "985"
        varlist['F'] = "2022"

        lines = [
            'ADD A B',
            'ADD B C',
            'ADD C D',
            'ADD D A',
            'ADD E F',
            'ADD F "1112"'
        ]
        VL = VariableList(varlist)
        for line in parse(lines):
            Arithmetic(VL, line).calculate()
        self.assertEqual(
            list(VL.variable_list.items()),
            [('A', 22.5), ('B', 22.5), ('C', 22.5),
             ('D', 34.0), ('E', "9852022"), ('F', "20221112")]
        )
    def test_sub_value(self):
        varlist = defaultdict(int)
        varlist['A'] = 18
        varlist['B'] = 18.5
        varlist['C'] = 18
        varlist['D'] = 18.5
        lines = [
            'SUB A 7',
            'SUB B 7.0',
            'SUB C 6.5',
            'SUB D 7',
        ]
        VL = VariableList(varlist)
        for line in parse(lines):
            Arithmetic(VL, line).calculate()
        self.assertEqual(
            list(VL.variable_list.items()),
            [('A', 11), ('B', 11.5), ('C', 11.5), ('D', 11.5)]
        )

    def test_sub_variable(self):
        varlist = defaultdict(int)
        varlist['A'] = 18
        varlist['B'] = 18.5
        varlist['C'] = 18
        varlist['D'] = 18.5
        lines = [
            'SUB A B',
            'SUB B C',
            'SUB C D',
            'SUB D 0',
        ]
        VL = VariableList(varlist)
        for line in parse(lines):
            Arithmetic(VL, line).calculate()
        self.assertEqual(
            list(VL.variable_list.items()),
            [('A', -0.5), ('B', 0.5), ('C', -0.5), ('D', 18.5)]
        )

    def test_mult_value(self):
        varlist = defaultdict(int)
        varlist['A'] = 5
        varlist['B'] = 3.5
        varlist['C'] = 3
        varlist['D'] = 3.5
        varlist['E'] = "Boo"
        varlist['F'] = 3

        lines = [
            'MULT A 11',
            'MULT B 12.0',
            'MULT C 12.5',
            'MULT D 12',
            'MULT E 3',
            'MULT F "Boo"',
        ]
        VL = VariableList(varlist)
        for line in parse(lines):
            Arithmetic(VL, line).calculate()
        self.assertEqual(
            list(VL.variable_list.items()),
            [('A', 55), ('B', 42.0), ('C', 37.5), ('D', 42.0),
             ("E", "BooBooBoo"), ("F", "BooBooBoo")]
        )

    def test_mult_variable(self):
        varlist = defaultdict(int)
        varlist['A'] = 1
        varlist['B'] = 2
        varlist['C'] = 3
        varlist['D'] = 4
        varlist['E'] = "Boo"
        varlist['F'] = 3

        lines = [
            'MULT A B',
            'MULT B C',
            'MULT C D',
            'MULT D E',
            'MULT E F',
        ]
        VL = VariableList(varlist)
        for line in parse(lines):
            Arithmetic(VL, line).calculate()
        self.assertEqual(
            list(VL.variable_list.items()),
            [('A', 2), ('B', 6), ('C', 12),
             ('D', "BooBooBooBoo"), ("E", "BooBooBoo"), ("F", 3)]
        )

    def test_mult_value(self):
        varlist = defaultdict(int)
        varlist['A'] = 7
        varlist['B'] = 7.5
        varlist['C'] = 7
        varlist['D'] = 7.0

        lines = [
            'DIV A 2',
            'DIV B 3.0',
            'DIV C 2.0',
            'DIV D 2',
        ]
        VL = VariableList(varlist)
        for line in parse(lines):
            Arithmetic(VL, line).calculate()
        self.assertEqual(
            list(VL.variable_list.items()),
            [('A', 3), ('B', 2.5), ('C', 3.5), ('D', 3.5)]
        )

    def test_mult_variable(self):
        varlist = defaultdict(int)
        varlist['A'] = 1
        varlist['B'] = 2
        varlist['C'] = 4.0
        varlist['D'] = 16.0

        lines = [
            'DIV A B',
            'DIV B C',
            'DIV C D',
        ]
        VL = VariableList(varlist)
        for line in parse(lines):
            Arithmetic(VL, line).calculate()
        self.assertEqual(
            list(VL.variable_list.items()),
            [('A', 0), ('B', 0.5), ('C', 0.25), ('D', 16.0)]
        )

    def test_error_calculate(self):
        varlist = defaultdict(int)
        varlist['A'] = 1
        varlist['B'] = 2
        varlist['C'] = 'abc'
        varlist['D'] = 4
        lines = [
            'ADD A "abc"',
            'SUB B "abc"',
            'MULT C "abc"',
            'DIV D "abc"',
            'DIV D 0.0',
        ]
        VL = VariableList(varlist)
        for line in parse(lines[0:4]):
            with self.assertRaises(TypeError):
                Arithmetic(VL, line).calculate()
        for line in parse(lines[4:]):
            with self.assertRaises(ZeroDivisionError):
                Arithmetic(VL, line).calculate()


if __name__ == "__main__":
    unittest.main()
