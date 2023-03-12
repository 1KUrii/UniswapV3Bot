from src.Calculate.Wallet.Wallet import Wallet


class Swap:
    USDT = "USDT"
    TIMESTAMP = "timestamp"
    PAIR = "PAIR"

    def __init__(self, wallet: Wallet, token_a_name, token_b_name):
        self.token_a_name = token_a_name
        self.token_b_name = token_b_name
        self.token_prices = {
            token_a_name: 0,
            token_b_name: 0,
            self.USDT: 1,
            self.TIMESTAMP: 0,
            self.PAIR: 0
        }
        self.wallet = wallet.list_token_amount

    def data_update(self, time, price_pair, price_a, price_b):
        self.token_prices.update({
            self.TIMESTAMP: time,
            self.token_a_name: price_a,
            self.token_b_name: price_b,
            self.PAIR: price_pair
        })

    def swap_tokens(self, token_a_name, amount_a, token_b_name):
        token_a_amount = self.wallet[token_a_name]
        if token_a_amount < amount_a:
            print(f"Not enough {token_a_name} tokens in the wallet")
        else:
            amount_b = amount_a * self.token_prices[token_b_name] / self.token_prices[token_a_name]
            self.wallet[token_a_name] -= amount_a
            self.wallet[token_b_name] += amount_b
            print(f"{amount_a} {token_a_name} tokens swapped for {amount_b} {token_b_name} tokens")

    def pool_equality(self):
        value_a = self.wallet[self.token_a_name] * self.token_prices[self.token_a_name]
        value_b = self.wallet[self.token_b_name] * self.token_prices[self.token_b_name]
        return value_a == value_b

