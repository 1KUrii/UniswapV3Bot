from datetime import datetime
from enum import Enum

from src.Calculate.Bot.BotPool import BotPool
from src.Calculate.Exchange.Exchange import Exchange
from src.Calculate.Uniswap.Swap import Swap
from src.Calculate.Wallet.Wallet import Wallet
from src.Calculate.Uniswap.Pool import Pool
from src.Calculate.Data.Data import Data


class Token(Enum):
    USDT = 1
    PAIR = 0


class Calculate:
    def __init__(self):
        self.input_question()
        self.check_correct_input()
        self._data = Data()

    def input_question(self) -> None:
        self.a_name = input("Enter the name of the first token: ").strip().upper() + "USDT"
        self.b_name = input("Enter the name of the second token: ").strip().upper() + "USDT"
        self.start_date_str = input("Enter the start date (YYYY-MM-DD): ").strip()
        self.end_date_str = input("Enter the end date (YYYY-MM-DD): ").strip()
        self.timeframe = input("Enter the timeframe: ").strip()
        self.starting_capital = float(input("Enter the starting capital: "))

    def check_correct_input(self) -> None:
        # Validate inputs
        if not self.a_name.isalnum() or not self.b_name.isalnum():
            raise ValueError("Token names can only contain letters and digits.")
        self.start_date = datetime.strptime(self.start_date_str, '%Y-%m-%d')
        self.end_date = datetime.strptime(self.end_date_str, '%Y-%m-%d')
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date.")
        if self.starting_capital <= 0:
            raise ValueError("Starting capital must be positive.")

    def calculate(self) -> Wallet:
        exchange = Exchange()
        date, prices_pair, prices_a, prices_b = exchange.get_time_prices(self.a_name, self.b_name,
                                                                         self.timeframe,
                                                                         self.start_date, self.end_date)
        volume_pool = exchange.get_pool_volume(600_000, 4_000_000)

        wallet = Wallet(self._data, self.a_name, self.b_name, self.starting_capital)
        swap = Swap(wallet, self.a_name, self.b_name)
        bot = BotPool(wallet, swap, self.a_name, self.b_name)
        pool = Pool(self._data, wallet, self.a_name, self.b_name)

        for timestamp, price_pair, price_a, price_b, volume_pl in zip(date, prices_pair, prices_a, prices_b, volume_pool):
            self._data.timestamp = timestamp
            self._data.list_price = {
                self.a_name: price_a,
                self.b_name: price_b,
                Token.USDT.name: Token.USDT.value,
                Token.PAIR.name: price_pair}
            self._data.volume = volume_pl
            bot.start_uniswap_strategy()
            wallet.logging_wallet()
        return wallet


if __name__ == "__main__":
    try:
        calc = Calculate()
        wallet = calc.calculate()
        print(wallet)
        wallet.output_logs()
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
