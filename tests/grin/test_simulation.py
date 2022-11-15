# test_simulation.py
# unittest for the class Simulation

from grin.simulation import Simulation, ErrorMessageClass
from grin.parsing import parse
import unittest
import io
import contextlib

class TestSimulation(unittest.TestCase):
    def test_many_labels(self):
        lines = [
            'LABEL1: LET A 1',
            'LABEL2: PRINT A',
            'LABEL3: LET B C',
            'LABEL4: PRINT B',
            'LABEL5: PRINT C',
            'END',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "1\n0\n0\n"
            )

    def test_many_ifs(self):
        lines = [
            'LABEL1: LET A 1',
            'LABEL2: GOTO 1 IF 1 > 2',
            'LABEL3: LET B C',
            'LABEL4: PRINT B',
            'LABEL5: PRINT C',
            'END',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "0\n0\n"
            )

    def test_goto_0_v1(self):
        lines = [
            'LET A 0',
            'GOTO A',
            'END',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                ErrorMessageClass().GOTO_0_ERROR+'\n'
            )

    def test_goto_0_v2(self):
        lines = [
            'GOTO 0',
            'END',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                ErrorMessageClass().GOTO_0_ERROR+'\n'
            )

    def test_goto_0_v3(self):
        lines = [
            'GOTO ABCDEF',
            'END',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                ErrorMessageClass().GOTO_0_ERROR+'\n'
            )

    def test_goto_NOT_EXIST_LABEL(self):
        lines = [
            'GOTO "ABCDEF"',
            'END',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                ErrorMessageClass().GOTO_NOT_EXIST_LABEL+'\n'
            )

    def test_goto_invalid_line(self):
        lines = [
            'GOTO 3',
            'PRINT A',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                ErrorMessageClass().GOTO_INVALID_LINE+'\n'
            )

    def test_return(self):
        lines = [
            'GOTO 1',
            'RETURN',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                ErrorMessageClass().RETURN_ERROR+'\n'
            )
