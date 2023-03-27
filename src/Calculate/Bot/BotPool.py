from enum import Enum

from src.Calculate.Uniswap.Swap import Swap
from src.Calculate.Uniswap.Pool import Pool
from src.Calculate.Wallet.Wallet import Wallet


class Token(Enum):
    USDT = 1
    PAIR = 0


class BotPool:

    def __init__(self, wallet: Wallet, swap: Swap, a_name, b_name):
        self.pool = None
        self.a_name = a_name
        self.b_name = b_name
        self.wallet = wallet
        self.price_lower = None
        self.price_upper = None
        self.log_transactions = []
        self.swap = swap

    def add_pool(self, pool: Pool):
        self.pool = pool
        return self

    def set_range_for_pool(self, price_lower, price_upper):
        self.price_lower = price_lower
        self.price_upper = price_upper
        self.pool.add_range_pool(self.price_lower, self.price_upper)

    def change_ratio_wallet_token(self, a_name, b_name, necessary_value_a, token_a_value):
        token_b_amount_wallet = self.get_token_amount(b_name)
        amount_b_for_swap = (necessary_value_a - token_a_value) / self.get_token_price(b_name)
        if token_b_amount_wallet < amount_b_for_swap:
            raise ValueError(f"Not enough {b_name} in wallet.")
        self.swap.swap_tokens(b_name, amount_b_for_swap, a_name)

    def add_all_token_to_pool(self):
        if not self.price_lower or not self.price_upper:
            print("Adding tokens to pool failed, pool has no range, add it")
            return
        if not self.pool.in_range():
            print("Adding tokens to pool failed, current pair price not in range, change range")
            return

        ratio_a = (self.price_upper - self.get_token_price(Token.PAIR.name)) / (self.price_upper - self.price_lower)
        ratio_b = 1 - ratio_a

        token_a_value = self.token_value(self.a_name)
        token_b_value = self.token_value(self.b_name)
        value_tokens = token_a_value + token_b_value

        necessary_value_a = value_tokens * ratio_a
        necessary_value_b = value_tokens * ratio_b

        if necessary_value_a > token_a_value:
            self.change_ratio_wallet_token(self.a_name, self.b_name, necessary_value_a, token_a_value)

        elif necessary_value_b > token_b_value:
            self.change_ratio_wallet_token(self.b_name, self.a_name, necessary_value_b, token_b_value)

    def pool_strategy(self):
        # self.pool.add_liquidity(self.get_token_amount(self.a_name), self.get_token_amount(self.b_name))
        self.add_all_token_to_pool()

    def swap_equal_a_b_token(self):
        if not self.wallet.wallet_equality():
            token_a_price = self.get_token_price(self.a_name)
            token_b_price = self.get_token_price(self.b_name)
            token_a_amount = self.get_token_amount(self.a_name)
            token_b_amount = self.get_token_amount(self.b_name)
            difference = (token_a_amount * token_a_price - token_b_amount * token_b_price) / 2
            try:
                token_a_name = self.a_name
                token_b_name = self.b_name
                if not difference > 0:
                    token_a_name, token_b_name = token_b_name, token_a_name
                    token_a_price = token_b_price
                    difference = -difference
                self.swap.swap_tokens(token_a_name, difference / token_a_price, token_b_name)
            except:
                print("Swap failed.")

    def convert_stable(self):
        usdt_amount = self.get_token_amount(Token.USDT.name)
        if usdt_amount > 0:
            split_usdt_amount = usdt_amount / 2
            self.swap.swap_tokens(Token.USDT.name, split_usdt_amount, self.a_name)
            self.swap.swap_tokens(Token.USDT.name, split_usdt_amount, self.b_name)

    def start_uniswap_strategy(self):
        self.convert_stable()
        self.swap_equal_a_b_token()
        self.pool_strategy()

    def get_token_price(self, token_name):
        return self.wallet.list_price[token_name]

    def get_token_amount(self, token_name):
        return self.wallet.list_token_amount[token_name]

    def token_value(self, token_name, amount=None):
        if not amount:
            amount = self.get_token_amount(token_name)
        price = self.get_token_price(token_name)
        return amount * price

    def portfolio_value(self):
        value = 0
        for token_name, token_amount in self.wallet.list_token_amount.items():
            value += self.token_value(token_name, token_amount)
        return value
