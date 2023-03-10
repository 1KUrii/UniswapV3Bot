from src.Calculate.Uniswap.UniswapV3Pool import UniswapV3Pool
from src.Calculate.Wallet.Wallet import Wallet


class BotPool:
    USDT = "USDT"
    TIMESTAMP = "timestamp"
    PAIR = "PAIR"

    def __init__(self, wallet: Wallet, uniswap: UniswapV3Pool, token_a_name, token_b_name):
        self.token_a_name = token_a_name
        self.token_b_name = token_b_name
        self.wallet = wallet.list_token_amount
        self.log_transactions = []
        self.uniswap = uniswap
        self.time = 0

    def data_update(self, time):
        self.time = time

    def swap_equal(self):
        self.convert_stable()
        if not self.uniswap.pool_equality():
            token_a_price = self.get_token_price(self.token_a_name)
            token_b_price = self.get_token_price(self.token_b_name)
            difference = self.wallet[self.token_a_name] * token_a_price - self.wallet[self.token_b_name] * token_b_price
            try:
                token_a_name = self.token_a_name
                token_b_name = self.token_b_name
                if not difference > 0:
                    token_a_name, token_b_name = token_b_name, token_a_name
                    token_a_price = token_b_price
                    difference = -difference
                self.uniswap.swap_tokens(token_a_name, difference / token_a_price, token_b_name)
            except:
                print("Swap failed.")

    def convert_stable(self):
        usdt_amount = self.wallet[self.USDT]
        if usdt_amount > 0:
            split_usdt_amount = usdt_amount / 2
            self.uniswap.swap_tokens(self.USDT, split_usdt_amount, self.token_a_name)
            self.uniswap.swap_tokens(self.USDT, split_usdt_amount, self.token_b_name)

    def start_uniswap_strategy(self):
        self.swap_equal()

    def get_token_price(self, token_name):
        return self.uniswap.token_prices[token_name]

    def token_value(self, token_name, amount=None):
        if not amount:
            amount = self.wallet[token_name]
        price = self.get_token_price(token_name)
        return amount * price

    def portfolio_value(self):
        value = 0
        for token_name, token_amount in self.wallet.items():
            value += self.token_value(token_name, token_amount)
        return value

    def __str__(self):
        holdings = self.wallet
        str = ""
        for token_name, token_amount in holdings.items():
            str += f"{token_name}:\n"
            str += f"\t{token_amount} {token_name} at {self.get_token_price(token_name):.2f} USD\n"
            str += f"\tCurrent value: {self.token_value(token_name, token_amount):.2f} USD\n\n"
        str += f"portfolio value: {self.portfolio_value()}\n\n"
        return str
