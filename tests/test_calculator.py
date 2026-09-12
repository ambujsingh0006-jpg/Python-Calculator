import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest
from calculator import SafeCalculator


class TestSafeCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = SafeCalculator()

    def test_addition(self):
        self.assertEqual(self.calc.calculate("10 + 5"), 15)

    def test_multiplication(self):
        self.assertEqual(self.calc.calculate("6 * 7"), 42)

    def test_parentheses(self):
        self.assertEqual(self.calc.calculate("(10 + 5) * 2"), 30)

    def test_power(self):
        self.assertEqual(self.calc.calculate("2 ** 5"), 32)

    def test_square_root(self):
        self.assertEqual(self.calc.calculate("sqrt(144)"), 12)

    def test_pi(self):
        self.assertAlmostEqual(self.calc.calculate("pi"), 3.141592653589793)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.calculate("10 / 0")


if __name__ == "__main__":
    unittest.main()
