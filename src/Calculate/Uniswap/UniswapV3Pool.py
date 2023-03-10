
class UniswapV3Pool:
    USDT = "USDT"
    TIMESTAMP = "timestamp"
    PAIR = "PAIR"

    def __init__(self, token_a_name, token_b_name):
        self.token_a_name = token_a_name
        self.token_b_name = token_b_name
        self.token_prices = {
            token_a_name: 0,
            token_b_name: 0,
            self.USDT: 1,
            self.TIMESTAMP: 0,
            self.PAIR: 0
        }

    def data_update(self, time, price_pair, price_a, price_b):
        self.token_prices.update({
            self.TIMESTAMP: time,
            self.token_a_name: price_a,
            self.token_b_name: price_b,
            self.PAIR: price_pair
        })

    def swap_tokens(self, list_tokens_amount, token_a_name, amount_a,
                    token_b_name):
        token_a_amount = list_tokens_amount[token_a_name]
        if token_a_amount < amount_a:
            print(f"Not enough {token_a_name} tokens in the pool")
            return list_tokens_amount

        amount_b = amount_a * self.token_prices[token_b_name] / self.token_prices[token_a_name]
        list_tokens_amount[token_a_name] -= amount_a
        list_tokens_amount[token_b_name] += amount_b
        print(f"{amount_a} {token_a_name} tokens swapped for {amount_b} {token_b_name} tokens")
        return list_tokens_amount

    def pool_equality(self, list_tokens_amount):
        value_a = list_tokens_amount[self.token_a_name] * self.token_prices[self.token_a_name]
        value_b = list_tokens_amount[self.token_b_name] * self.token_prices[self.token_b_name]
        return value_a == value_b

    def get_token_prices_a_b_pair(self):
        return (
            self.token_prices[self.token_b_name],
            self.token_prices[self.token_a_name],
            self.token_prices[self.PAIR],
        )

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
