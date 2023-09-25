from src.Calculate.ClassEnum.Network import Network
from src.Calculate.ClassEnum.Token import Token
from src.Calculate.ResultData.ResultData import ResultData
from src.Calculate.WorkData.WorkData import WorkData


class Wallet:

    def __init__(self, _result_data: ResultData, _work_data: WorkData, network: Network = Network.MATIC,
                 starting_capital=0):
        self.network = network
        self.list_price = {}
        self._work_data = _work_data
        self._work_data.add_observer(self)
        self.result_data = _result_data
        self.result_data.add_observer(self)
        self._list_token_amount = {
            self.network.name: {self.network.name: 10 / self.list_price[self.network.name],
                                Token.USDT.name: starting_capital - 10}}

    def update(self):
        self.list_price = self._work_data.list_price

    def logged(self):
        self.result_data.logging_wallet(self._list_token_amount[self.network.name])

    def wallet_token_eq(self, a_name, b_name):
        value_a = self._list_token_amount[self.network.name][a_name] * self.list_price[a_name]
        value_b = self._list_token_amount[self.network.name][b_name] * self.list_price[b_name]
        return value_a == value_b

    def add_token_id(self, token_name: str):
        self._list_token_amount[self.network.name][token_name] = 2

    def get_token_amount(self, token_name: str):
        return self._list_token_amount[self.network.name][token_name]

    def has_token(self, token_name: str):
        return token_name in self._list_token_amount[self.network.name]

    def add_tokens(self, token_name: str, token_amount):
        if self.has_token(token_name):
            self._list_token_amount[self.network.name][token_name] += token_amount
        else:
            raise ValueError("Don't have this token in wallet")

    def subtract_amount(self, token_name, token_amount):
        if token_amount <= self._list_token_amount[self.network.name][token_name]:
            self._list_token_amount[self.network.name][token_name] -= token_amount
        else:
            raise ValueError("Not enough tokens for swap")
