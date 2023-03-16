from enum import Enum

from src.Calculate.Data.Data import Data


class Token(Enum):
    USDT = 1
    PAIR = 0

#  где хранить пул в валлете или лучше данные об пуле записывать в валлет, чтобы можно было подсчитать валью
class Wallet:
    USDT = "USDT"
    PAIR = "PAIR"

    def __init__(self, _data: Data, a_name, b_name, starting_capital):
        self.a_name = a_name
        self.b_name = b_name
        self.list_token_amount = {
            self.a_name: 0,
            self.b_name: 0,
            self.USDT: starting_capital
        }
        self.list_price = {
            self.a_name: 0,
            self.b_name: 0,
            Token.USDT.name: 1,
            Token.PAIR.name: 0
        }
        self.timestamp = 0
        self.log_wallet = []
        self._data = _data
        self._data.add_observer(self)

    def update(self):
        self.timestamp = self._data.timestamp
        self.list_price = self._data.list_price

    def wallet_equality(self):
        value_a = self.list_token_amount[self.a_name] * self.list_price[self.a_name]
        value_b = self.list_token_amount[self.b_name] * self.list_price[self.b_name]
        return value_a == value_b

    def logging_wallet(self):
        self.log_wallet.append([self.timestamp, self.list_token_amount.copy(), self.list_price.copy()])

    def token_value(self, token_name, amount=None, price=None):
        if not amount:
            amount = self.list_price[token_name]
        if not price:
            price = self.list_price[token_name]
        return amount * price

    def portfolio_value(self):
        value = 0
        for token_name, token_amount in self.list_token_amount.items():
            value += self.token_value(token_name, token_amount)
        return value

    def output_logs(self):
        for i, (timestamp, list_token_amount, list_token_prices) in enumerate(self.log_wallet):
            print(f"Wallet Log {i + 1}:")
            print("-------------------------------------------------")
            print(f"Timestamp: {timestamp}")
            print("Token Amounts:")
            for token_name, token_amount in list_token_amount.items():
                if token_name != self.USDT:
                    value = self.token_value(token_name, token_amount, list_token_prices[token_name])
                    print(f"\t{token_name}: {token_amount} at {value:.2f} USD")
                else:
                    print(f"\t{token_name}: {token_amount}")
            print("Token Prices:")
            for token_name, token_price in list_token_prices.items():
                print(f"\t{token_name}: {token_price}")
            print()

    def __str__(self):
        str = ""
        for token_name, token_amount in self.list_token_amount.items():
            str += f"{token_name}:\n"
            str += f"\t{token_amount} {token_name} at {self.list_price[token_name]:.2f} USD\n"
            str += f"\tCurrent value: {self.token_value(token_name, token_amount):.2f} USD\n\n"
        str += f"portfolio value: {self.portfolio_value()}\n\n"
        return str
