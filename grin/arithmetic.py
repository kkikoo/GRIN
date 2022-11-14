# arithmetic.py
# Do the arithmetic operations in Grin, and process the Exception

# *example1: ADD A 5, means that A += 5
# *example2: DIV A 3, means that A /= 3
# *example3: DIV A 0, means that A /= 0, this is a RuntimeError, will be processed.
# *example4: SUB A B, means that A -= B, Notice that here B is a Variable

from grin.token import GrinToken, GrinTokenKind
from grin.variable_list import VariableList


class Arithmetic:
    def __init__(self, _var_list: VariableList, grinline: list[GrinToken]) -> None:

        self.var_list = _var_list    # global variable list
        self.op = grinline[0].kind   # operations type
        self.var = grinline[1].text  # variable name

        # text=value='ABC'            ABC is variable
        # text='"ABC"', value='ABC'   ABC is string
        self.value = grinline[2].value  # may be value or variable
        if grinline[2].value == grinline[2].text: # it is a variable
            self.value = self.var_list.variable_list[grinline[2].value]

    def calculate(self):
        """
        * update the value of variable
        * and catch the exception
        """
        if self.op == GrinTokenKind.ADD:
            self.add()
        elif self.op == GrinTokenKind.SUB:
            self.sub()
        elif self.op == GrinTokenKind.MULT:
            self.multi()
        elif self.op == GrinTokenKind.DIV:
            self.div()
    def add(self):
        """do the + operation"""
        try:
            self.var_list.variable_list[self.var] += self.value
        except:
            raise TypeError(
                "unsupported operand type(s) for +: '{}' and '{}'".format(
                    type(self.var).__name__, type(self.value).__name__)
            )

    def sub(self):
        """do the - operation"""
        try:
            self.var_list.variable_list[self.var] -= self.value
        except:
            raise TypeError(
                "unsupported operand type(s) for -: '{}' and '{}'".format(
                    type(self.var).__name__, type(self.value).__name__)
            )

    def multi(self):
        """do the * operation"""
        try:
            self.var_list.variable_list[self.var] *= self.value
        except:
            raise TypeError(
                "unsupported operand type(s) for *: '{}' and '{}'".format(
                    type(self.var).__name__, type(self.value).__name__)
            )

    def div(self):
        """do the / operation"""
        if self.value == 0:
            raise ZeroDivisionError("division by zero")
        try:
            if type(self.var_list.variable_list[self.var]) == type(self.value) and \
                    type(self.value) == int:
                self.var_list.variable_list[self.var] //= self.value
            else:
                self.var_list.variable_list[self.var] /= self.value
        except:
            raise TypeError(
                "unsupported operand type(s) for /: '{}' and '{}'".format(
                    type(self.var).__name__, type(self.value).__name__)
            )
