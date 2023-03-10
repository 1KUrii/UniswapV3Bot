import unittest
from unittest.mock import patch

from io import StringIO
from datetime import datetime

from src.Calculate.Calculate import Calculate


class TestCalculate(unittest.TestCase):
    @patch('builtins.input', side_effect=['MATIC', 'CRV', '2023-02-01', '2023-03-08', 'D', '100'])
    def test_calculate(self, mock_input):
        calc = Calculate()
        self.assertEqual(calc.token_a_name, 'MATICUSDT')
        self.assertEqual(calc.token_b_name, 'CRVUSDT')
        self.assertEqual(calc.start_date, datetime(2023, 2, 1))
        self.assertEqual(calc.end_date, datetime(2023, 3, 8))
        self.assertEqual(calc.timeframe, 'D')
        self.assertEqual(calc.starting_capital, 100.0)
        calc.output()


if __name__ == '__main__':
    unittest.main()
