# simulation.py
# simulation the Grin language

from collections import defaultdict
from grin.compare import compare
from grin.token import GrinTokenKind, GrinToken
from grin.variable_list import VariableList
from grin.arithmetic import Arithmetic


class ErrorMessageClass:
    """ Store all types of error-message
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

    def _process_line_with_label(self, line: list[GrinToken]):
        tag = -1
        for i in range(len(line)):
            if line[i].kind == GrinTokenKind.COLON:
                tag = i
                break
        if tag == -1:
            return line
        else:
            return line[tag+1:]

    def simulation(self):
        self._stack.append(0)
        while len(self._stack) != 0:
            now_do_line_number = self._stack.pop()
            if now_do_line_number >= len(self._grin_lines):
                break

            now_do_line = self._process_line_with_label(
                self._grin_lines[now_do_line_number]
            )
            op_type = now_do_line[0].kind

            # input
            if op_type in [GrinTokenKind.INNUM, GrinTokenKind.INSTR]:
                try:
                    self._input(now_do_line)
                    self._stack.append(now_do_line_number + 1)
                except:
                    print(ErrorMessageClass().INPUT_ERROR)
                    break
            # output
            elif op_type == GrinTokenKind.PRINT:
                self._output(now_do_line)
                self._stack.append(now_do_line_number + 1)
            # let
            if op_type == GrinTokenKind.LET:
                self._let(now_do_line)
                self._stack.append(now_do_line_number + 1)
            # end
            elif op_type in [GrinTokenKind.END]:
                break
            # return
            elif op_type == GrinTokenKind.RETURN:
                self.number_of_return += 1
                if self.number_of_return > self.number_of_gosub:
                    print(ErrorMessageClass().RETURN_ERROR)
                    break
                continue

            # arithmetic: +,-,*,/
            elif op_type in [GrinTokenKind.ADD, GrinTokenKind.SUB, GrinTokenKind.MULT, GrinTokenKind.DIV]:
                try:
                    A = Arithmetic(self._var_list, now_do_line)
                    A.calculate()
                    self._stack.append(now_do_line_number + 1)
                except:
                    print(ErrorMessageClass().Arithmetic_ERROR)
                    break
            # goto / gosub
            elif op_type in [GrinTokenKind.GOTO, GrinTokenKind.GOSUB]:
                bool_of_if = self.bool_of_if(now_do_line)
                if bool_of_if == -1:
                    print(ErrorMessageClass().COMPARE_ERROR)
                    break
                if bool_of_if == 0:
                    self._stack.append(now_do_line_number + 1)
                    continue

                if op_type == GrinTokenKind.GOSUB:
                    self.number_of_gosub += 1
                    self._stack.append(now_do_line_number + 1)

                goto_index = now_do_line[1].value

                # value of goto(gosub), like goto 5
                if type(goto_index) == int:
                    if goto_index == 0:
                        print(ErrorMessageClass().GOTO_0_ERROR)
                        break
                    else:
                        next_line_number = now_do_line_number + goto_index
                else:
                    if now_do_line[1].text == now_do_line[1].value:  # var
                        value_of_this_var = self._var_list.variable_list[now_do_line[1].value]
                        if type(value_of_this_var) == int:
                            next_line_number = now_do_line_number + value_of_this_var
                        else:
                            if value_of_this_var not in self._index_of_label.keys():
                                print(ErrorMessageClass().GOTO_NOT_EXIST_LABEL)
                                break
                            else:
                                next_line_number = self._index_of_label[value_of_this_var]
                        if now_do_line_number == next_line_number:
                            print(ErrorMessageClass().GOTO_0_ERROR)
                            break
                    else:  # label
                        if now_do_line[1].value not in self._index_of_label.keys():
                            print(ErrorMessageClass().GOTO_NOT_EXIST_LABEL)
                            break
                        else:
                            next_line_number = self._index_of_label[now_do_line[1].value]
                # print(next_line_number,now_do_line_number)
                if 0 <= next_line_number <= self._max_line_number and next_line_number != now_do_line_number:
                    self._stack.append(next_line_number)
                else:
                    print(ErrorMessageClass().GOTO_INVALID_LINE)