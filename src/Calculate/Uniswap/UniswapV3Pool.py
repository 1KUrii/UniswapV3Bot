from src.Calculate.Wallet.Wallet import Wallet

class UniswapV3Pool:
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
        self.pool = Pools()

    def data_update(self, time, price_pair, price_a, price_b):
        self.token_prices.update({
            self.TIMESTAMP: time,
            self.token_a_name: price_a,
            self.token_b_name: price_b,
            self.PAIR: price_pair
        })

        self.pool.time = time
        self.pool.current_price_pair = price_pair

    def swap_tokens(self, token_a_name, amount_a, token_b_name):
        token_a_amount = self.wallet[token_a_name]
        if token_a_amount < amount_a:
            print(f"Not enough {token_a_name} tokens in the pool")
        else:
            amount_b = amount_a * self.token_prices[token_b_name] / self.token_prices[token_a_name]
            self.wallet[token_a_name] -= amount_a
            self.wallet[token_b_name] += amount_b
            print(f"{amount_a} {token_a_name} tokens swapped for {amount_b} {token_b_name} tokens")

    def pool_equality(self):
        value_a = self.wallet[self.token_a_name] * self.token_prices[self.token_a_name]
        value_b = self.wallet[self.token_b_name] * self.token_prices[self.token_b_name]
        return value_a == value_b


class Pools:
    TOKEN_NAMES = "token_names"
    TOKEN_AMOUNT = "token_amount"
    RANGE = "range"
    COMISSION = "comission"

    def __init__(self):
        self.pools = {}
        self.time = 0
        self.current_price_pair = 0

    def create_pool(self, token_a_name, token_b_name, token_a_amount, token_b_amount, low_tick_range, high_tick_range):
        pool = {
            self.TOKEN_NAMES: [token_a_name, token_b_name],
            self.TOKEN_AMOUNT: [token_a_amount, token_b_amount],
            self.RANGE: [low_tick_range, high_tick_range],
            self.COMISSION: 0}
        self.pools[f"{token_a_name}/{token_b_name}"] = pool

    def add_liquidity(self, list_token_amount, name_pool, token_name, token_amount):
        pass

    def in_diapazon(self, name_pool):
        low_tick_range = self.pools[name_pool][self.RANGE][0]
        high_tick_range = self.pools[name_pool][self.RANGE][1]
        return low_tick_range <= self.current_price_pair <= high_tick_range

    def delete_pool(self, name_pool):
        del self.pools[name_pool]
