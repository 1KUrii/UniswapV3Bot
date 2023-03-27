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
        self.liquidity = None
        self.total_volume = 0
        self.total_liquidity = 0

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

        self.log_pool = []

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
        self.total_volume = self._data.volume_pool
        self.total_liquidity = self._data.volume_liquidity
        self.list_price = self._data.list_price

    def logging_pool(self):
        self.log_pool.append(
            [self.timestamp, {self.a_name: self.a_amount, self.b_name: self.b_amount}, self.list_price.copy()])

    def start_work(self):
        self.calculate_liquidity()

    def value_pool(self):
        return self.a_amount * self.list_price[self.a_name] + self.b_amount * self.list_price[self.b_name]

    def calculate_liquidity(self):
        price_pair = self.list_price[Token.PAIR.name]
        if price_pair <= self.price_lower:
            self.a_amount += self.b_amount / self.price_lower
            self.b_amount = 0

        elif self.price_lower < price_pair < self.price_upper:
            ratio_a = (self.price_upper - self.get_token_price(Token.PAIR.name)) / (self.price_upper - self.price_lower)
            ratio_b = 1 - ratio_a

            token_a_value = self.token_value(self.a_name, self.a_amount)
            token_b_value = self.token_value(self.b_name, self.b_amount)
            value_tokens = token_a_value + token_b_value

            necessary_value_a = value_tokens * ratio_a
            necessary_value_b = value_tokens * ratio_b

            self.a_amount = necessary_value_a / self.get_token_price(self.a_name)
            self.b_amount = necessary_value_b / self.get_token_price(self.b_name)

        elif price_pair >= self.price_upper:
            self.b_amount += self.a_amount * self.price_upper
            self.a_amount = 0

        print(
            f"{self.a_amount} {self.a_name}, {self.b_amount} {self.b_name}, Price pair: {self.get_token_price(Token.PAIR.name)}, Value pool: {self.token_value(self.a_name, self.a_amount) + self.token_value(self.b_name, self.b_amount)}")

    def add_liquidity(self, token_a_amount, token_b_amount):
        token_a_amount_wallet = self.wallet.list_token_amount[self.a_name]
        token_b_amount_wallet = self.wallet.list_token_amount[self.b_name]
        if token_a_amount_wallet < token_a_amount:
            raise ValueError(f"Not enough {self.a_name} in wallet.")
        elif token_b_amount_wallet < token_b_amount:
            raise ValueError(f"Not enough {self.b_name} in wallet.")
        else:
            self.wallet.list_token_amount[self.a_name] -= token_a_amount
            self.a_amount += token_a_amount
            self.wallet.list_token_amount[self.b_name] -= token_b_amount
            self.b_amount += token_b_amount
        if not self.liquidity:
            self.liquidity = self.value_pool()
        return self

    def get_token_amount_in_wallet(self, token_name):
        return self.wallet.list_token_amount[token_name]

    def get_token_price(self, token_name):
        return self.list_price[token_name]

    def add_range_pool(self, price_lower, price_high):
        self.price_lower = price_lower
        self.price_upper = price_high
        return self

    def in_range(self):
        return self.price_lower <= self.list_price[Token.PAIR.name] <= self.price_upper

    def remove_commission(self):
        self.wallet.list_token_amount[self.a_name] += self.commission_a_amount
        self.commission_a_amount = 0
        self.wallet.list_token_amount[self.b_name] += self.commission_b_amount
        self.commission_a_amount = 0

    def token_value(self, token_name, amount=None, price=None):
        if not amount:
            amount = self.get_token_amount_in_wallet(token_name)
        if not price:
            price = self.get_token_price(token_name)
        return amount * price

    def output_logs(self):
        for i, (timestamp, list_token_amount, list_token_prices) in enumerate(self.log_pool):
            print(f"Pool Log {i + 1}:")
            print("-------------------------------------------------")
            print(f"Timestamp: {timestamp}")
            print("Token Amounts:")
            for token_name, token_amount in list_token_amount.items():
                if token_name != Token.USDT.name:
                    value = self.token_value(token_name, token_amount, list_token_prices[token_name])
                    print(f"\t{token_name}: {token_amount} at {value:.2f} USD")
                else:
                    print(f"\t{token_name}: {token_amount}")
            print("Token Prices:")
            for token_name, token_price in list_token_prices.items():
                print(f"\t{token_name}: {token_price}")
            print()
