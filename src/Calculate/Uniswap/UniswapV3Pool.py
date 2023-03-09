class UniswapV3Pool:
    def __init__(self, token_a_name, token_b_name):
        self.token_a_name = token_a_name
        self.token_b_name = token_b_name
        self.token_pair = {token_a_name: {"price_usdt": 0}, token_b_name: {"price_usdt": 0}, "USDT": {"price_usdt": 1},
                           "timestamp": 0, "price_pair": 0}

    def data_update(self, time, price_pair, price_a, price_b):
        self.token_pair["timestamp"] = time
        self.token_pair[self.token_a_name]["price_usdt"] = price_a
        self.token_pair[self.token_b_name]["price_usdt"] = price_b
        self.token_pair["price_pair"] = price_pair

    def swap_tokens(self, list_tokens_amount, token_a_name, amount_a, token_b_name):
        if (list_tokens_amount[token_a_name]["amount"] - amount_a) < 0:
            return list_tokens_amount
        amount_b = amount_a * self.token_pair[token_a_name]["price_usdt"] / self.token_pair[token_b_name][
            "price_usdt"]
        list_tokens_amount[token_a_name]["amount"] -= amount_a
        list_tokens_amount[token_b_name]["amount"] += amount_b
        return list_tokens_amount

    def pool_equality(self, list_tokens_amount):
        if list_tokens_amount[self.token_a_name]["amount"] * self.token_pair[self.token_a_name]["price_usdt"] != \
                list_tokens_amount[self.token_b_name]["amount"] * self.token_pair[self.token_b_name]["price_usdt"]:
            return False
        return True

    def get_token_prices_a_b_pair(self):
        return self.token_pair[self.token_a_name]["price_usdt"], self.token_pair[self.token_b_name]["price_usdt"], \
            self.token_pair["price_pair"]

    # def create_pool(self, token_a_price, token_b_price, token_a_amount, token_b_amount, range_low, range_high):
    #     self.token_a_price = token_a_price
    #     self.token_b_price = token_b_price
    #     self.token_a_amount = token_a_amount
    #     self.token_b_amount = token_b_amount
    #     self.range_low = range_low
    #     self.range_high = range_high

    # def add_liquidity(self, amount_a, amount_b):
    #     self.token_a_amount += amount_a
    #     self.token_b_amount += amount_b
    #
    # def remove_liquidity(self, liquidity):
    #     token_a_share = liquidity / (self.token_a_amount / self.token_a_price)
    #     token_b_share = liquidity / (self.token_b_amount / self.token_b_price)
    #     self.token_a_amount -= token_a_share
    #     self.token_b_amount -= token_b_share

    # def get_liquidity(self):
    #     return min(self.token_a_amount / self.token_a_price, self.token_b_amount / self.token_b_price) * (
    #             self.range_high - self.range_low)
