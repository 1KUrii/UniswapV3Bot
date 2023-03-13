from src.Calculate.Uniswap.Swap import Swap
from src.Calculate.Wallet.Wallet import Wallet


class BotPool:
    USDT = "USDT"
    TIMESTAMP = "timestamp"
    PAIR = "PAIR"

    def __init__(self, wallet: Wallet, swap: Swap, token_a_name, token_b_name):
        self.token_a_name = token_a_name
        self.token_b_name = token_b_name
        self.wallet = wallet
        self.log_transactions = []
        self.uniswap = swap

    def swap_equal_a_b_token(self):
        if not self.wallet.wallet_equality():
            token_a_price = self.get_token_price(self.token_a_name)
            token_b_price = self.get_token_price(self.token_b_name)
            token_a_amount = self.wallet.list_token_amount[self.token_a_name]
            token_b_amount = self.wallet.list_token_amount[self.token_b_name]
            difference = (token_a_amount * token_a_price - token_b_amount * token_b_price) / 2
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
        usdt_amount = self.wallet.list_token_amount[self.USDT]
        if usdt_amount > 0:
            split_usdt_amount = usdt_amount / 2
            self.uniswap.swap_tokens(self.USDT, split_usdt_amount, self.token_a_name)
            self.uniswap.swap_tokens(self.USDT, split_usdt_amount, self.token_b_name)

    def start_uniswap_strategy(self):
        self.convert_stable()
        self.swap_equal_a_b_token()

    def get_token_price(self, token_name):
        return self.wallet.list_token_prices[token_name]

    def token_value(self, token_name, amount=None):
        if not amount:
            amount = self.wallet.list_token_amount[token_name]
        price = self.get_token_price(token_name)
        return amount * price

    def portfolio_value(self):
        value = 0
        for token_name, token_amount in self.wallet.list_token_amount.items():
            value += self.token_value(token_name, token_amount)
        return value
