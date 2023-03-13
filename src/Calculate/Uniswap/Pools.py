from src.Calculate.Uniswap.Pool import Pool
from src.Calculate.Wallet.Wallet import Wallet


class Pools:
    def __init__(self, wallet: Wallet):
        self.wallet = wallet

    def create_pool(self, token_a_name, token_b_name, pool_a_amount, pool_b_amount, low_tick_range, high_tick_range):
        try:
            pool = Pool(self.wallet)
            pool.set_name_pool(token_a_name, token_b_name)
            pool.add_amount_pool(pool_a_amount, pool_b_amount)
            pool.set_range_pool(low_tick_range, high_tick_range)
            self.wallet.list_pools.append(pool)
        except Exception as er:
            print("Error creating pool: " + er)

    def update_data(self, volume):
        # self.wallet.list_pools
        pass

