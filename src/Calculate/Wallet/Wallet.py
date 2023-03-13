class Wallet:
    USDT = "USDT"
    PAIR = "PAIR"

    def __init__(self, token_a_name, token_b_name, starting_capital):
        self.token_a_name = token_a_name
        self.token_b_name = token_b_name
        self.list_token_amount = {
            self.token_a_name: 0,
            self.token_b_name: 0,
            self.USDT: starting_capital
        }
        self.list_token_prices = {
            self.token_a_name: 0,
            self.token_b_name: 0,
            self.USDT: 1,
            self.PAIR: 0
        }
        self.list_pools = []
        self.timestamp = 0
        self.log_wallet = []

    def data_update(self, timestamp, price_pair, price_a, price_b):
        self.timestamp = timestamp
        self.list_token_prices.update({
            self.token_a_name: price_a,
            self.token_b_name: price_b,
            self.PAIR: price_pair
        })

    def wallet_equality(self):
        value_a = self.list_token_amount[self.token_a_name] * self.list_token_prices[self.token_a_name]
        value_b = self.list_token_amount[self.token_b_name] * self.list_token_prices[self.token_b_name]
        return value_a == value_b

    def logging_wallet(self):
        self.log_wallet.append([self.timestamp, self.list_token_amount.copy(), self.list_token_prices.copy()])

    def token_value(self, token_name, amount=None, price=None):
        if not amount:
            amount = self.list_token_prices[token_name]
        if not price:
            price = self.list_token_prices[token_name]
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
            str += f"\t{token_amount} {token_name} at {self.list_token_prices[token_name]:.2f} USD\n"
            str += f"\tCurrent value: {self.token_value(token_name, token_amount):.2f} USD\n\n"
        str += f"portfolio value: {self.portfolio_value()}\n\n"
        return str
