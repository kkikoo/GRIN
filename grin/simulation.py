# simulation.py
# simulation the Grin language

from collections import defaultdict
from grin.compare import compare
from grin.token import GrinTokenKind, GrinToken
from grin.variable_list import VariableList
from grin.arithmetic import Arithmetic

class ErrorMessageClass():
    """ Store all types of error-messgae
    """

    def __init__(self) -> None:
        self.INPUT_ERROR = "Errors are encountered while parsing the input!"
        self.RETURN_ERROR = "RETURN statement does not match previous GOSUB!"
        self.COMPARE_ERROR = "Errors are encountered while doing compare!"
        self.Arithmetic_ERROR = "Errors are encountered while doing arithmetic calculate!"
        self.GOTO_0_ERROR = "Can not jump to the same line!"
        self.GOTO_NOT_EXIST_LABEL = "Can not jump to a not exist Label!"
        self.GOTO_INVALID_LINE = "Can not jump to an invalid line!"

class Simulation:
    def __init__(self, grin_lines: list[list[GrinToken]]):
        self._grin_lines = grin_lines
        self._var_list = VariableList()
        self._index_of_label = defaultdict(int)
        self._stack = []
        self._max_line_number = len(grin_lines)
        self.number_of_return = 0
        self.number_of_gosub = 0

        for index, line in enumerate(grin_lines):
            if len(line) >= 2 and line[1].text == ':':
                self._index_of_label[line[0].value] = index

    def _input(self, line: list[GrinToken]):
        var_type = line[0].kind
        var_name = line[1].value
        if var_type == GrinTokenKind.INNUM:
            _ = input().strip()
            for ch in _:
                if ch not in ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                    raise ValueError
            if '.' in _:
                self._var_list.variable_list[var_name] = float(_)
            else:
                self._var_list.variable_list[var_name] = int(_)
        else:
            self._var_list.variable_list[var_name] = str(input())

    def _output(self, line: list[GrinToken]):
        if line[1].text == line[1].value:
            print(self._var_list.variable_list[line[1].value])
        else:
            print(line[1].value)

    def _let(self, line: list[GrinToken]):
        x = line[1].value  # var
        y = line[2].value  # var or value
        if line[2].text == line[2].value:
            y = self._var_list.variable_list[y]
        self._var_list.variable_list[x] = y

    def bool_of_if(self, line: list[GrinToken]):
        index_of_if = -1
        for i in range(len(line)):
            if line[i].kind == GrinTokenKind.IF:
                index_of_if = i
        if index_of_if == -1:
            return 1
        else:
            if_line = line[index_of_if:]
            comp = compare(if_line, self._var_list)
            return comp
