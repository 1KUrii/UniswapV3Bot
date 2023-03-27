import unittest
from unittest.mock import patch

from datetime import datetime

from src.Calculate.Calculate import Calculate


class TestCalculate(unittest.TestCase):
    @patch('builtins.input', side_effect=['MATIC', 'CRV', '2023-02-01', '2023-03-08', 'D', '100'])
    def test_calculate(self, mock_input):
        calc = Calculate()
        self.assertEqual(calc.a_name, 'MATICUSDT')
        self.assertEqual(calc.b_name, 'CRVUSDT')
        self.assertEqual(calc.start_date, datetime(2023, 2, 1))
        self.assertEqual(calc.end_date, datetime(2023, 3, 8))
        self.assertEqual(calc.timeframe, 'D')
        self.assertEqual(calc.starting_capital, 100.0)
        wallet, pool = calc.calculate()
        print(wallet)
        pool.output_logs()
        wallet.output_logs()


if __name__ == '__main__':
    unittest.main()
