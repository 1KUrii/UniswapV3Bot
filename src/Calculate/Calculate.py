from datetime import datetime

from src.Calculate.ClassEnum.Token import Token
from src.Calculate.Uniswap.Uniswap import Uniswap
from src.Calculate.WorkData.WorkData import WorkData
from src.Calculate.Bot.BotPool import BotPool
from src.Calculate.ClassEnum.Network import Network
from src.Calculate.Exchange.Exchange import Exchange
from src.Calculate.ResultData.ResultData import ResultData
from src.Calculate.Wallet.Wallet import Wallet


class Calculate:
    def __init__(self):
        self.input_question()
        self.check_correct_input()
        self._work_data = WorkData()
        self._result_data = ResultData()

        self.wallet = None
        self.exchange = None
        self.uniswap = None
        self.bot = None

    def input_question(self) -> None:
        message = "Choice Network:\n"
        network_name = {}
        for i, net in enumerate(Network):
            message += f"\t{i + 1}) {net.name}\n"
            network_name[i + 1] = net
        network_id = int(input(message + "Network id: ").strip())
        self.network = network_name[network_id]
        self.a_name = input("Enter the name of the first token: ").strip().upper() + "USDT"
        self.b_name = input("Enter the name of the second token: ").strip().upper() + "USDT"
        self.start_date_str = input("Enter the start date (YYYY-MM-DD): ").strip()
        self.end_date_str = input("Enter the end date (YYYY-MM-DD): ").strip()
        self.timeframe = input("Enter the timeframe: ").strip()
        self.starting_capital = float(input("Enter the starting capital: "))
        self.price_deviation = float(input("Enter the price deviation for pool:"))

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

    def data_update(self, timestamp, price_network, price_pair, price_a, price_b, volume_pl, volume_lq):
        self._work_data.a_name = self.a_name
        self._work_data.b_name = self.b_name
        self._work_data.timestamp = timestamp
        self._work_data.list_price = {
            self.network.name: price_network,
            self.a_name: price_a,
            self.b_name: price_b,
            Token.USDT.name: Token.USDT.value,
            Token.PAIR.name: price_pair}
        self._work_data.volume_pool = volume_pl
        self._work_data.volume_liquidity = volume_lq

    def save_result_data(self, timestamp, list_price):
        self._result_data.set_timestamp(timestamp)
        self._result_data.set_list_price(list_price)

    def create_environment(self):
        self.wallet = Wallet(self._result_data, self._work_data, self.network, self.starting_capital)
        self.wallet.add_token_id(self.a_name)
        self.wallet.add_token_id(self.b_name)
        self.uniswap = Uniswap(self._result_data, self._work_data)
        self.bot = BotPool(self._result_data, self._work_data, self.wallet, self.uniswap, self.network)
        self.bot.set_price_deviation(self.price_deviation)

    def calculate(self):
        self.exchange = Exchange()
        date, price_network, prices_pair, prices_a, prices_b = self.exchange.get_time_prices(self.network.name,
                                                                                             self.a_name,
                                                                                             self.b_name,
                                                                                             self.timeframe,
                                                                                             self.start_date,
                                                                                             self.end_date)

        # нужно заменить тут на что-то, а то магические числа
        volume_pool = self.exchange.get_pool_volume(100_000, 300_000)
        volume_liquidity = self.exchange.get_pool_liquidity(300_000, 600_000)

        # это можно как то обыграть черз функцию или вообще логику изменить
        for timestamp, price_network, price_pair, price_a, price_b, volume_pl, volume_lq in zip(date, price_network,
                                                                                                prices_pair, prices_a,
                                                                                                prices_b,
                                                                                                volume_pool,
                                                                                                volume_liquidity):
            self.data_update(timestamp, price_network, price_pair, price_a, price_b, volume_pl, volume_lq)
            self.save_result_data(timestamp, self._work_data.list_price)
            if self.wallet is None or self.bot is None or self.uniswap is None:
                self.create_environment()
            self.bot.uniswap_strategy()
            self._result_data.logged()

        return self

    def get_result_data(self):
        return self._result_data


if __name__ == "__main__":
    m = Calculate()
