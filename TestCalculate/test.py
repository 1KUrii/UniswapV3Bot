import unittest
from unittest.mock import patch

from datetime import datetime
from src.Calculate.Calculate import Calculate
import App


class TestCalculate(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', 'MATIC', 'CRV', '2023-01-26', '2023-02-26', 'D', '6000', '0.05'])
    def test_calculate(self, mock_input):
        calc = App.app()
        # calc = Calculate()
        # self.assertEqual(calc.a_name, 'MATICUSDT')
        # self.assertEqual(calc.b_name, 'CRVUSDT')
        # self.assertEqual(calc.start_date, datetime(2023, 2, 1))
        # self.assertEqual(calc.end_date, datetime(2023, 3, 8))
        # self.assertEqual(calc.timeframe, 'D')
        # self.assertEqual(calc.starting_capital, 100.0)
        # log = calc.calculate()
        # print(log)


if __name__ == '__main__':
    unittest.main()
