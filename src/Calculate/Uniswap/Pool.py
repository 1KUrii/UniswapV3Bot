import math
from enum import Enum

from src.Calculate.Wallet.Wallet import Wallet


class FeeTier(Enum):
    MAX = 1
    MEDIUM = 0.3
    LOW = 0.05


class Pool:
    def __init__(self, wallet: Wallet, token_a_name, token_b_name):
        self.total_value_pool = 0
        self.current_price_pair = 0

        self.token_a_name = token_a_name
        self.token_b_name = token_b_name

        self.a_amount = 0
        self.b_amount = 0

        self.low_tick_range = 0
        self.high_tick_range = 0

        self.timestamp = 0

        self.commission_a_amount = 0
        self.commission_b_amount = 0

        self.wallet = wallet
        self.fee_tier = FeeTier.MEDIUM

    def data_update(self, timestamp, volume_pl, price_pair):
        self.timestamp = timestamp
        self.total_value_pool = volume_pl
        self.current_price_pair = price_pair
        self.calculate_commission()


    def calculate_estimated_fee(self, volume_24h: float, total_liquidity: float, delta_liquidity: float) -> float:
        """
        Calculate estimated fee based on the formula mentioned in Uniswap v3 whitepaper.
        :param volume_24h: float, 24-hour volume of the pool.
        :param total_liquidity: float, total liquidity of the pool.
        :param delta_liquidity: float, delta liquidity of the pool.
        :return: float, estimated fee of the pool.
        """
        L = total_liquidity
        deltaL = delta_liquidity
        fee_tier = self.fee_tier

        fee = fee_tier * volume_24h * (deltaL / (L + deltaL))
        return fee

    def calculate_delta_liquidity(self, amount0: float, amount1: float, current_tick_id: int, lower_tick_id: int,
                                  upper_tick_id: int, price_lower: float, price_upper: float) -> float:
        sqrt_p = math.sqrt(price_lower * price_upper)
        if current_tick_id < lower_tick_id:
            delta_liquidity = amount0 * (sqrt_p * math.sqrt(price_lower)) / (sqrt_p - math.sqrt(price_lower))
        elif current_tick_id > upper_tick_id:
            delta_liquidity = amount1 / (sqrt_p - math.sqrt(price_upper))
        else:
            delta_liquidity = min(amount0 * (sqrt_p * math.sqrt(price_lower)) / (sqrt_p - math.sqrt(price_lower)),
                                  amount1 / (sqrt_p - math.sqrt(price_upper)))
        return delta_liquidity

    def add_amount_pool(self, token_a_amount, token_b_amount):
        token_a_amount_wallet = self.wallet.list_token_amount[self.token_a_name]
        token_b_amount_wallet = self.wallet.list_token_amount[self.token_b_name]
        if token_a_amount_wallet < token_a_amount:
            raise
        elif token_b_amount_wallet < token_b_amount:
            raise
        else:
            self.wallet.list_token_amount[self.token_a_name] -= token_a_amount
            self.a_amount += token_a_amount
            self.wallet.list_token_amount[self.token_b_name] -= token_b_amount
            self.b_amount += token_b_amount

    def set_range_pool(self, low_tick_range, high_tick_range):
        self.low_tick_range = low_tick_range
        self.high_tick_range = high_tick_range

    def in_range(self):
        return self.low_tick_range <= self.current_price_pair <= self.high_tick_range

    def remove_commission(self):
        self.wallet.list_token_amount[self.token_a_name] += self.commission_a_amount
        self.commission_a_amount = 0
        self.wallet.list_token_amount[self.token_b_name] += self.commission_b_amount
        self.commission_a_amount = 0

    def calculate_commission(self):
        if not self.in_range():
            return
        commission = self.total_value_pool * self.fee_tier
        self.commission_a_amount += self.low_tick_range * commission * self.a_amount / self.total_value_pool
        self.commission_b_amount += commission * self.b_amount / self.total_value_pool
