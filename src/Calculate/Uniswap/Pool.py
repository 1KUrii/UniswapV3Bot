import math
from enum import Enum

from src.Calculate.Data.Data import Data
from src.Calculate.Wallet.Wallet import Wallet


class FeeTier(Enum):
    MAX = 1
    MEDIUM = 0.3
    LOW = 0.05


class Token(Enum):
    USDT = 1
    PAIR = 0


# подумать над подсчетом валью в пуле и как это суммировать с валлетом
class Pool:
    def __init__(self, _data: Data, wallet: Wallet, a_name, b_name):
        self.total_volume = 0
        self.total_liquidity = 0

        self.current_price_pair = 0
        self.current_tick = 0

        self.a_name = a_name
        self.b_name = b_name

        self.a_amount = 0
        self.b_amount = 0

        self.low_tick = 0
        self.high_tick = 0
        self.price_lower = 0
        self.price_upper = 0

        self.timestamp = 0

        self.commission_a_amount = 0
        self.commission_b_amount = 0

        self.wallet = wallet
        self.fee_tier = FeeTier.MEDIUM.value

        self.list_price = {
            self.a_name: 0,
            self.b_name: 0,
            Token.USDT.name: 1,
            Token.PAIR.name: 0
        }

        self._data = _data
        self._data.add_observer(self)

        # подумать над логами, может вообще отдельный класс под логи с наследованием и методами
        self.logs = []

    # добавить обновление комиссионных
    def update(self):
        self.timestamp = self._data.timestamp
        self.total_volume = self._data.volume
        # надо исправить тут
        self.total_liquidity = self._data.volume
        self.list_price = self._data.list_price
        # self.calculate_commission()

    # разобраться, как это работает
    def calculate_estimated_fee(self) -> float:
        """
        Calculate estimated fee based on the formula mentioned in Uniswap v3 whitepaper.
        total_liquidity: float, total liquidity of the pool.
        delta_liquidity: float, delta liquidity of the pool.
        :return: float, estimated fee of the pool.
        """
        delta_liquidity = self.calculate_delta_liquidity()
        fee = self.fee_tier * self.total_volume * (delta_liquidity / (self.total_liquidity + delta_liquidity))
        return fee

    # разобраться, как это работает
    def calculate_delta_liquidity(self) -> float:
        sqrt_p = math.sqrt(self.price_lower * self.price_upper)
        if self.current_tick < self.low_tick:
            delta_liquidity = self.a_amount * (sqrt_p * math.sqrt(self.price_lower)) / (
                    sqrt_p - math.sqrt(self.price_lower))
        elif self.current_tick > self.high_tick:
            delta_liquidity = self.b_amount / (sqrt_p - math.sqrt(self.price_upper))
        else:
            delta_liquidity = min(
                self.a_amount * (sqrt_p * math.sqrt(self.price_lower)) / (sqrt_p - math.sqrt(self.price_lower)),
                self.b_amount / (sqrt_p - math.sqrt(self.price_upper)))
        return delta_liquidity

    def add_amount_pool(self, token_a_amount, token_b_amount):
        token_a_amount_wallet = self.wallet.list_token_amount[self.a_name]
        token_b_amount_wallet = self.wallet.list_token_amount[self.b_name]
        if token_a_amount_wallet < token_a_amount:
            raise
        elif token_b_amount_wallet < token_b_amount:
            raise
        else:
            self.wallet.list_token_amount[self.a_name] -= token_a_amount
            self.a_amount += token_a_amount
            self.wallet.list_token_amount[self.b_name] -= token_b_amount
            self.b_amount += token_b_amount

    def set_range_pool(self, price_lower, price_high):
        self.price_lower = price_lower
        self.price_upper = price_high

    def in_range(self):
        return self.price_lower <= self.current_price_pair <= self.price_upper

    def remove_commission(self):
        self.wallet.list_token_amount[self.a_name] += self.commission_a_amount
        self.commission_a_amount = 0
        self.wallet.list_token_amount[self.b_name] += self.commission_b_amount
        self.commission_a_amount = 0

    # изменить работу метода или заменить на что то другое
    def calculate_commission(self):
        if not self.in_range():
            return
        commission = self.total_volume * self.fee_tier
        self.commission_a_amount += self.low_tick_range * commission * self.a_amount / self.total_volume
        self.commission_b_amount += commission * self.b_amount / self.total_volume
