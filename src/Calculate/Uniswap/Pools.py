from src.Calculate.Uniswap.Pool import Pool
from src.Calculate.Wallet.Wallet import Wallet


class Pools:
    def __init__(self, wallet: Wallet):
        self.wallet = wallet

    def create_pool(self):
        pool = Pool(self.wallet)
        pool.set_name_pool()
        pool.add_amount_pool()
        pool.set_range_pool()
