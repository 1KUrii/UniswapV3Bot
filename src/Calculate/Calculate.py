from datetime import datetime

from src.Calculate.Bot.BotPool import BotPool
from src.Calculate.Exchange.Exchange import Exchange
from src.Calculate.Uniswap.UniswapV3Pool import UniswapV3Pool
from src.Calculate.Wallet.Wallet import Wallet


class Calculate:
    def __init__(self):
        self.token_a_name = input("Enter the name of the first token: ").strip().upper() + "USDT"
        self.token_b_name = input("Enter the name of the second token: ").strip().upper() + "USDT"
        self.start_date_str = input("Enter the start date (YYYY-MM-DD): ").strip()
        self.end_date_str = input("Enter the end date (YYYY-MM-DD): ").strip()
        self.timeframe = input("Enter the timeframe: ").strip()
        self.starting_capital = float(input("Enter the starting capital: "))

        # Validate inputs
        if not self.token_a_name.isalnum() or not self.token_b_name.isalnum():
            raise ValueError("Token names can only contain letters and digits.")
        self.start_date = datetime.strptime(self.start_date_str, '%Y-%m-%d')
        self.end_date = datetime.strptime(self.end_date_str, '%Y-%m-%d')
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date.")
        if self.starting_capital <= 0:
            raise ValueError("Starting capital must be positive.")

    def calculate(self):
        exchange = Exchange()
        date, prices_pair, prices_a, prices_b = exchange.get_time_prices(self.token_a_name, self.token_b_name,
                                                                         self.timeframe, self.start_date,
                                                                         self.end_date)
        wallet = Wallet(self.token_a_name, self.token_b_name, self.starting_capital)
        uniswap = UniswapV3Pool(wallet, self.token_a_name, self.token_b_name)
        bot = BotPool(wallet, uniswap, self.token_a_name, self.token_b_name)
        for time, price_pair, price_a, price_b in zip(date, prices_pair, prices_a, prices_b):
            uniswap.data_update(time, price_pair, price_a, price_b)
            bot.data_update(time)
            bot.start_uniswap_strategy()
        return bot


if __name__ == "__main__":
    try:
        calc = Calculate()
        bot = calc.calculate()
        print(bot)
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
