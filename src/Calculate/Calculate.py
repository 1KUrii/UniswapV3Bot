from datetime import datetime

from src.Calculate.Bot.BotPool import BotPool
from src.Calculate.Exchange.Exchange import Exchange
from src.Calculate.Uniswap.UniswapV3Pool import UniswapV3Pool


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
        date, prices = exchange.get_time_prices(self.token_a_name, self.token_b_name, self.timeframe, self.start_date,
                                                self.end_date)

        bot = BotPool(self.token_a_name, self.token_b_name, self.starting_capital)
        # uniswap = UniswapV3Pool(date[0], prices[0])
        # for time, price in zip(date, prices):
        #     pass
            # uniswap.data_update(time, price)
            # bot.start_uniswap_strategy()

        return date, prices

    def output(self):
        date, prices = self.calculate()
        # print(date[0], prices[0])
        for time, price in zip(date, prices):
            print(f"{time}\t{price:.4f}")


if __name__ == "__main__":
    try:
        calc = Calculate()
        date, prices = calc.calculate()
        print("Date\t\tPrice")
        for time, price in zip(date, prices):
            print(f"{time}\t{price:.4f}")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
