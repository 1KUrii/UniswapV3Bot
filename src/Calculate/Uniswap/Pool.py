import math

from src.Calculate.ClassEnum.FeeTier import FeeTier
from src.Calculate.ClassEnum.Token import Token
from src.Calculate.ResultData.ResultData import ResultData
from src.Calculate.WorkData.WorkData import WorkData
from src.Calculate.Wallet.Wallet import Wallet
from src.Calculate.Uniswap.Commission.commission import commission


class Pool:
    def __init__(self, _result_data: ResultData, _data: WorkData, a_name, b_name):
        self.liquidity = None
        self.volume24H = 0
        self.total_liquidity = 0

        self.a_name = a_name
        self.b_name = b_name

        self._a_amount = 0
        self._b_amount = 0

        self._price_lower = 0
        self._price_upper = 0

        self.timestamp = 0

        self._commission_a_amount = 0
        self._commission_b_amount = 0

        self.fee_tier = FeeTier.MEDIUM.value

        self.list_price = {
            self.a_name: 0,
            self.b_name: 0,
            Token.USDT.name: 1,
            Token.PAIR.name: 0
        }

        self._data = _data
        self._data.add_observer(self)

        self.result_data = _result_data
        self.result_data.add_observer(self)

    def update(self):
        self.timestamp = self._data.timestamp
        self.volume24H = self._data.volume_pool
        self.total_liquidity = self._data.volume_liquidity
        self.list_price = self._data.list_price
        try:
            self.update_token_ratio()
            self.update_commission_amount()
        except ValueError as er:
            print("Error with update pool: ", er)

    def logged(self):
        self.result_data.logging_pool(self.a_name, self._a_amount, self.b_name, self._b_amount)
        self.result_data.logging_reward(self._commission_a_amount)
        self.result_data.logging_reward(self._commission_b_amount)

    def remove_liquidity(self, wallet: Wallet):
        try:
            wallet.add_tokens(self.a_name, self._a_amount)
            wallet.add_tokens(self.b_name, self._b_amount)
        except ValueError as er:
            print("Faild remove liquidity: ", er)

    def update_token_ratio(self):
        if not self.liquidity:
            raise ValueError("Don't update token ratio, not have liquidity")

        price_pair = self.list_price[Token.PAIR.name]
        if price_pair <= self._price_lower:
            self._a_amount += self._b_amount / self._price_lower
            self._b_amount = 0

        elif self._price_lower < price_pair < self._price_upper:
            ratio_a = (self._price_upper - self.get_token_price(Token.PAIR.name)) / (
                    self._price_upper - self._price_lower)
            ratio_b = 1 - ratio_a

            token_a_value = self.token_value(self.a_name, self._a_amount)
            token_b_value = self.token_value(self.b_name, self._b_amount)
            value_tokens = token_a_value + token_b_value

            necessary_value_a = value_tokens * ratio_a
            necessary_value_b = value_tokens * ratio_b

            self._a_amount = necessary_value_a / self.get_token_price(self.a_name)
            self._b_amount = necessary_value_b / self.get_token_price(self.b_name)

        elif price_pair >= self._price_upper:
            self._b_amount += self._a_amount * self._price_upper
            self._a_amount = 0

    def update_commission_amount(self):
        if self.in_range():
            ratio_a = (self._price_upper - self.get_token_price(Token.PAIR.name)) / (
                    self._price_upper - self._price_lower)
            ratio_b = 1 - ratio_a
            try:
                value_fee = self.calculate_estimated_fee()
                self._commission_a_amount += value_fee * ratio_a / self.get_token_price(self.a_name)
                self._commission_b_amount += value_fee * ratio_b / self.get_token_price(self.b_name)

            except ValueError as er:
                print(er)

    @commission
    def add_liquidity(self, wallet: Wallet, token_a_amount, token_b_amount):
        if not self._price_lower or not self._price_upper:
            raise ValueError("Adding tokens to pool failed, pool has no range, add it")

        if not self.in_range():
            raise ValueError("Adding tokens to pool failed, current pair price not in range, change range")

        token_a_amount_wallet = wallet.get_token_amount(self.a_name)
        token_b_amount_wallet = wallet.get_token_amount(self.b_name)
        if token_a_amount_wallet < token_a_amount:
            raise ValueError(f"Not enough {self.a_name} in wallet.")
        elif token_b_amount_wallet < token_b_amount:
            raise ValueError(f"Not enough {self.b_name} in wallet.")
        else:
            wallet.subtract_amount(self.a_name, token_a_amount)
            self._a_amount += token_a_amount
            wallet.subtract_amount(self.b_name, token_b_amount)
            self._b_amount += token_b_amount
        if self.liquidity is None:
            self.liquidity = self.value_pool()

    def value_pool(self):
        return self._a_amount * self.list_price[self.a_name] + self._b_amount * self.list_price[self.b_name]

    def get_token_price(self, token_name):
        return self.list_price[token_name]

    def set_range_pool(self, price_lower, price_high):
        self._price_lower = price_lower
        self._price_upper = price_high
        return self

    def in_range(self):
        return self._price_lower <= self.list_price[Token.PAIR.name] <= self._price_upper

    def calculate_estimated_fee(self):
        if not self.liquidity:
            raise ValueError("Don't calculate estimated fee, not have liquidity")
        delta_l = None
        liquidity_amount0 = self._a_amount * self.list_price[self.a_name] * (
                math.sqrt(self._price_upper) * math.sqrt(self._price_lower)) / (
                                    math.sqrt(self._price_upper) - math.sqrt(self._price_lower))
        liquidity_amount1 = self._b_amount * self.list_price[self.b_name] / (
                math.sqrt(self._price_upper) - math.sqrt(self._price_lower))
        price_pair = self.list_price[Token.PAIR.name]
        if price_pair <= self._price_lower:
            delta_l = liquidity_amount0
        if price_pair > self._price_upper:
            delta_l = liquidity_amount1
        if self._price_lower <= price_pair <= self._price_upper:
            delta_l = min(liquidity_amount0, liquidity_amount1)
        fee = self.fee_tier * self.volume24H * (delta_l / (self.total_liquidity + delta_l))
        return fee

    @commission
    def remove_commission(self, wallet: Wallet):
        wallet.add_tokens(self.a_name, self._commission_a_amount)
        self._commission_a_amount = 0
        wallet.add_tokens(self.b_name, self._commission_b_amount)
        self._commission_a_amount = 0

    def token_value(self, token_name, amount=None, price=None):
        if not amount:
            amount = self.list_price[token_name]
        if not price:
            price = self.list_price[token_name]
        return amount * price
