from src.Calculate.Wallet.Wallet import Wallet


class Pool:
    def __init__(self, wallet: Wallet):
        self.time = 0
        self.current_price_pair = 0
        self.token_a_name = ""
        self.token_b_name = ""
        self.timestamp = 0
        self.low_tick_range = 0
        self.high_tick_range = 0
        self.pool_a_amount = 0
        self.pool_b_amount = 0
        self.commission_a_amount = 0
        self.commission_b_amount = 0
        self.wallet = wallet.list_token_amount

    def set_name_pool(self, token_a_name, token_b_name):
        self.token_a_name = token_a_name
        self.token_b_name = token_b_name

    def add_amount_pool(self, token_a_amount, token_b_amount):
        token_a_amount_wallet = self.wallet[self.token_a_name]
        token_b_amount_wallet = self.wallet[self.token_b_name]
        if token_a_amount_wallet < token_a_amount:
            print(f"Not enough {self.token_a_name} tokens in the pool")
        elif token_b_amount_wallet < token_b_amount:
            print(f"Not enough {self.token_b_name} tokens in the pool")
        else:
            self.wallet[self.token_a_name] -= token_a_amount
            self.pool_a_amount += token_a_amount
            self.wallet[self.token_b_name] -= token_b_amount
            self.pool_b_amount += token_b_amount

    def set_range_pool(self, low_tick_range, high_tick_range):
        self.low_tick_range = low_tick_range
        self.high_tick_range = high_tick_range

    def in_diapazon(self):
        return self.low_tick_range <= self.current_price_pair <= self.high_tick_range

    def remove_commission(self):
        self.wallet[self.token_a_name] += self.commission_a_amount
        self.commission_a_amount = 0
        self.wallet[self.token_b_name] += self.commission_b_amount
        self.commission_a_amount = 0

    def calculate_commission(self):
        if not self.in_range():
            return
        total_value = self.pool_a_amount * self.current_price_pair + self.pool_b_amount
        commission = total_value * self.commission_rate
        self.commission_a_amount += commission * self.pool_a_amount / total_value
        self.commission_b_amount += commission * self.pool_b_amount / total_value

    def withdraw_liquidity(self, token_name: str, token_amount: int):
        if token_name not in [self.token_a_name, self.token_b_name]:
            print(f"Invalid token name: {token_name}")
            return
        if token_amount <= 0:
            print("Token amount must be positive")
            return
        if not self.in_range():
            print("Cannot withdraw liquidity outside of the range")
            return
        if token_name == self.token_a_name:
            pool_token_amount = self.pool_a_amount
        else:
            pool_token_amount = self.pool_b_amount
        if pool_token_amount == 0:
            print(f"No {token_name} tokens in the pool")
            return
        token_amount_pool = int(token_amount * pool_token_amount /
                                (self.pool_a_amount + self.pool_b_amount))
        if token_name == self.token_a_name:
            self.pool_a_amount -= token_amount_pool
        else:
            self.pool_b_amount -= token_amount_pool
        token_amount_wallet = self.wallet.list_token_amount[token_name]
        self.wallet.list_token_amount[token_name] = min(token_amount_wallet + token_amount,
                                                        self.wallet.initial_token_amount[token_name])
