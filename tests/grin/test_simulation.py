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
    def test_case_from_teacher_1(self):
        lines = [
            'LET MESSAGE "Hello Boo!"',
            'PRINT MESSAGE',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "Hello Boo!\n"
            )

    def test_case_from_teacher_2(self):
        lines = [
            ' LET        A    3',
            '   PRINT        A',
            '      GOSUB    "CHUNK"',
            '        PRINT    A',
            '  PRINT   B',
            '     GOTO         "FINAL"',
            '         CHUNK:  LET A 4',
            '  LET   B                            6',
            '              RETURN',
            '  FINAL:     PRINT    A',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "3\n4\n6\n4\n"
            )

    def test_case_from_teacher_3(self):
        lines = [
            ' LET NAME "Boo"',
            'LET AGE 13.015625',
            'PRINT NAME',
            'PRINT AGE',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "Boo\n13.015625\n"
            )

    def test_case_from_teacher_4(self):
        lines = [
            'LET A 1',
            'GOTO 2',
            'LET A 2',
            'PRINT A',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "1\n"
            )

    def test_case_from_teacher_5(self):
        lines = [
            'LET Z 5',
            'GOTO 5',
            'LET C 4',
            'PRINT C',
            'PRINT Z',
            'END',
            'PRINT C',
            'PRINT Z',
            'GOTO -6',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "0\n5\n4\n5\n"
            )

    def test_case_from_teacher_6(self):
        lines = [
            '        LET Z 5',
            '        GOTO "CZ"',
            'CCZ:    LET C 4',
            '        PRINT C',
            '        PRINT Z',
            '        END',
            'CZ:     PRINT C',
            '        PRINT Z',
            '        GOTO "CCZ" ',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "0\n5\n4\n5\n"
            )

    def test_case_from_teacher_7(self):
        lines = [
            '                LET Z 1',
            '        LET C 11',
            '        LET F 4',
            '        LET B "ZC"',
            '        GOTO F',
            'ZC:     PRINT Z',
            '        PRINT C',
            '        END',
            'CZ:     PRINT C',
            '        PRINT Z',
            '        GOTO B',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "11\n1\n1\n11\n"
            )

    def test_case_from_teacher_8(self):
        lines = [
            'LET A 4',
            'ADD A 3',
            'PRINT A',
            'LET B 5',
            'SUB B 3',
            'PRINT B',
            'LET C 6',
            'MULT C B',
            'PRINT C',
            'LET D 8',
            'DIV D 2',
            'PRINT D'
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "7\n2\n12\n4\n"
            )

    def test_case_from_teacher_9(self):
        lines = [
            'LET A 1',
            'GOSUB 4',
            'PRINT A',
            'PRINT B',
            'END',
            'LET A 2',
            'LET B 3',
            'RETURN',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "2\n3\n"
            )

    def test_case_from_teacher_10(self):
        lines = [
            '           LET A 3',
            '           GOSUB "PRINTABC"',
            '           LET B 4',
            '           GOSUB "PRINTABC"',
            '           LET C 5',
            '           GOSUB "PRINTABC"',
            '           LET A 1',
            '           GOSUB "PRINTABC"',
            '           END',
            'PRINTABC:  PRINT A',
            '           PRINT B',
            '           PRINT C',
            '           RETURN',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "3\n0\n0\n3\n4\n0\n3\n4\n5\n1\n4\n5\n"
            )

    def test_case_from_teacher_11(self):
        lines = [
            '          LET A 1',
            'GOSUB 5',
            'PRINT A',
            'END',
            'LET A 3',
            'RETURN',
            'PRINT A',
            'LET A 2',
            'GOSUB -4',
            'PRINT A',
            'RETURN',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "1\n3\n3\n"
            )
    def test_case_from_teacher_12(self):
        lines = [
            '          LET A 3',
            'LET B 5',
            'GOTO 2 IF A < 4',
            'PRINT A',
            'PRINT B',
        ]
        S = Simulation(list(parse(lines)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            S.simulation()
            self.assertEqual(
                output.getvalue(),
                "5\n"
            )

if __name__ == "__main__":
    unittest.main()

