# test_compare.py
# unittest for the functions compare()

from grin.parsing import parse
from collections import defaultdict
from grin.compare import compare
from grin.variable_list import VariableList

class TestCompare(unittest.TestCase):

    def test_compare_number_and_number(self):
        lines = [
            'GOTO 1 IF 1 > 2',
            'GOTO 1 IF 1 < 2',
            'GOTO 1 IF 1 >= 2',
            'GOTO 1 IF 1 <= 2',
            'GOTO 1 IF 1 = 2',
            'GOTO 1 IF 1 <> 2',
            'GOTO 1 IF A > 2',
            'GOTO 1 IF A < 2',
            'GOTO 1 IF A >= 2',
            'GOTO 1 IF A <= 2',
            'GOTO 1 IF A = 2',
            'GOTO 1 IF A <> 2',
            'GOTO 1 IF A <> B',
        ]
        ans = []
        VL = VariableList()
        for i in parse(lines):
            ans.append(
                compare(i[2:], VL)
            )
        self.assertEqual(ans,
                         [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

        def test_compare_string_and_string(self):
            lines = [
                'GOTO 1 IF "abc" > "abcdef"',
                'GOTO 1 IF "abc" < "abcdef"',
                'GOTO 1 IF "abc" >= "abcdef"',
                'GOTO 1 IF "abc" <= "abcdef"',
                'GOTO 1 IF "abc" = "abcdef"',
                'GOTO 1 IF "abc" <> "abcdef"',
                'GOTO 1 IF A > "abcdef"',
                'GOTO 1 IF A < "abcdef"',
                'GOTO 1 IF A >= "abcdef"',
                'GOTO 1 IF A <= "abcdef"',
                'GOTO 1 IF A = "abcdef"',
                'GOTO 1 IF A <> "abcdef"',

            ]
            ans = []
            d = defaultdict(int)
            d['A'] = "abc"
            VL = VariableList(d)
            for i in parse(lines):
                ans.append(
                    compare(i[2:], VL)
                )
            self.assertEqual(ans,
                             [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1])

        def test_compare_string_and_number(self):
            lines = [
                'GOTO 1 IF 1 > "abcdef"',
                'GOTO 1 IF 1 < "abcdef"',
                'GOTO 1 IF 1 >= "abcdef"',
                'GOTO 1 IF 1 <= "abcdef"',
                'GOTO 1 IF 1 = "abcdef"',
                'GOTO 1 IF 1 <> "abcdef"',
                'GOTO 1 IF A > "abcdef"',
                'GOTO 1 IF A < "abcdef"',
                'GOTO 1 IF A >= "abcdef"',
                'GOTO 1 IF A <= "abcdef"',
                'GOTO 1 IF A = "abcdef"',
                'GOTO 1 IF A <> "abcdef"',
            ]
            ans = []
            d = defaultdict(int)
            d['A'] = 0.99
            VL = VariableList(d)
            for i in parse(lines):
                ans.append(
                    compare(i[2:], VL)
                )
            self.assertEqual(ans,
                             [-1, -1, -1, -1, 0, 1, -1, -1, -1, -1, 0, 1])

    if __name__ == "__main__":
        unittest.main()
