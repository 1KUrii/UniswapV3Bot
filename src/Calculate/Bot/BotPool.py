import datetime
from src.Calculate.Uniswap.UniswapV3Pool import UniswapV3Pool


class BotPool:
    def __init__(self, uniswap: UniswapV3Pool, token_a_name, token_b_name, starting_capital):
        self.token_a_name = token_a_name
        self.token_b_name = token_b_name
        self.list_token = {token_a_name: {"amount": 0}, token_b_name: {"amount": 0},
                           "USDT": {"amount": starting_capital}}
        self.log_transaction = {token_a_name: [], token_b_name: []}
        self.uniswap = uniswap

    def swap_equal(self):
        if self.list_token["USDT"]["amount"] > 0:
            diferance = self.list_token["USDT"]["amount"] / 2
            self.list_token = self.uniswap.swap_tokens(self.list_token, "USDT", diferance,
                                                       self.token_a_name)
            self.list_token = self.uniswap.swap_tokens(self.list_token, "USDT", diferance,
                                                       self.token_b_name)

        if not self.uniswap.pool_equality(self.list_token):
            price_a, price_b, price_pair = self.uniswap.get_token_prices_a_b_pair()
            difarance = self.list_token[self.token_a_name]["amount"] / price_pair - self.list_token[self.token_b_name][
                "amount"]
            if difarance > 0:
                self.list_token = self.uniswap.swap_tokens(self.list_token, self.token_a_name, difarance * price_pair,
                                                           self.token_b_name)
            else:
                self.list_token = self.uniswap.swap_tokens(self.list_token, self.token_b_name, -difarance,
                                                           self.token_a_name)

    def start_uniswap_strategy(self):
        self.swap_equal()
