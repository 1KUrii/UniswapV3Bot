import datetime

from src.Calculate.Uniswap.UniswapV3Pool import UniswapV3Pool


class BotPool:
    USDT = "USDT"
    TIMESTAMP = "timestamp"
    PAIR = "PAIR"

    def __init__(self, uniswap: UniswapV3Pool, token_a_name, token_b_name, starting_capital):
        self.token_a_name = token_a_name
        self.token_b_name = token_b_name
        self.list_token_amount = {
            self.token_a_name: 0,
            self.token_b_name: 0,
            self.USDT: starting_capital
        }
        self.log_transactions = {token: [] for token in [self.token_a_name, self.token_b_name, self.USDT]}
        self.uniswap = uniswap

    def swap_equal(self):
        self.convert_stable()
        if not self.uniswap.pool_equality(self.list_token_amount):
            token_a_price = self.get_token_price(self.token_a_name)
            token_b_price = self.get_token_price(self.token_b_name)
            difference = self.list_token_amount[self.token_a_name] * token_a_price - self.list_token_amount[
                self.token_b_name] * token_b_price
            try:
                token_a_name = self.token_a_name
                token_b_name = self.token_b_name
                if not difference > 0:
                    token_a_name, token_b_name = token_b_name, token_a_name
                    token_a_price = token_b_price
                    difference = -difference
                self.list_token_amount = self.uniswap.swap_tokens(
                    self.list_token_amount, token_a_name, difference / token_a_price, token_b_name)
            except:
                print("Swap failed.")

    def convert_stable(self):
        usdt_amount = self.list_token_amount[self.USDT]
        if usdt_amount > 0:
            split_usdt_amount = usdt_amount / 2
            self.list_token_amount = self.uniswap.swap_tokens(
                self.list_token_amount, self.USDT, split_usdt_amount, self.token_a_name)
            self.list_token_amount = self.uniswap.swap_tokens(
                self.list_token_amount, self.USDT, split_usdt_amount, self.token_b_name)

    def start_uniswap_strategy(self):
        self.swap_equal()
        price_a, price_b = self.get_token_price(self.token_a_name), self.get_token_price(self.token_b_name)
        time = datetime.datetime.now()
        self.log_transactions[self.token_a_name].append(
            (time, price_a, self.list_token_amount[self.token_a_name]))
        self.log_transactions[self.token_b_name].append(
            (time, price_b, self.list_token_amount[self.token_b_name]))
        self.log_transactions[self.USDT].append((time, 1, self.list_token_amount[self.USDT]))

    def log_transaction(self, token_name, time, price, amount):
        self.log_transactions[token_name].append((time, price, amount))

    def get_token_price(self, token_name):
        return self.uniswap.token_prices[token_name]

    def token_value(self, token_name, amount=None):
        if not amount:
            amount = self.list_token_amount[token_name]
        price = self.get_token_price(token_name)
        return amount * price

    def portfolio_value(self):
        value = 0
        for token_name, token_amount in self.list_token_amount.items():
            value += self.token_value(token_name, token_amount)
        return value

    def __str__(self):
        holdings = self.list_token_amount
        str = ""
        for token_name, token_amount in holdings.items():
            str += f"{token_name}:\n"
            str += f"\t{token_amount} {token_name} at {self.get_token_price(token_name):.2f} USD\n"
            str += f"\tCurrent value: {self.token_value(token_name, token_amount):.2f} USD\n\n"
        str += f"portfolio value: {self.portfolio_value()}\n"
        return str
