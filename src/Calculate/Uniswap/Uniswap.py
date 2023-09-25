from .Commission.commission import commission
from .Pool import Pool
from ..ClassEnum.Token import Token
from ..ResultData.ResultData import ResultData
from ..Wallet.Wallet import Wallet
from ..WorkData.WorkData import WorkData


class Uniswap:

    def __init__(self, _result_data: ResultData, _work_data: WorkData):
        self.list_price = self.list_price = {
            Token.USDT.name: 1,
            Token.PAIR.name: 0
        }
        self._pools = {}
        self._work_data = _work_data
        self._work_data.add_observer(self)
        self.result_data = _result_data

    def update(self):
        self.list_price = self._work_data.list_price

    def has_pools(self):
        return len(self._pools) > 0

    def create_pool(self, a_name, b_name):
        pool = Pool(self.result_data, self._work_data, a_name, b_name)
        self._pools[a_name + b_name] = pool

    def set_range_pool(self, a_name, b_name, price_lower, price_upper):
        pool: Pool = self.get_pool(a_name, b_name)
        pool.set_range_pool(price_lower, price_upper)

    def pool_in_range(self, a_name, b_name):
        pool = self.get_pool(a_name, b_name)
        return pool.in_range()

    def get_pool(self, a_name, b_name):
        return self._pools[a_name + b_name]

    def remove_pool(self, wallet: Wallet, a_name, b_name):
        pool = self.get_pool(a_name, b_name)
        pool.remove_commission(wallet)
        pool.remove_liquidity(wallet)
        self._pools.pop(a_name + b_name)

    def add_liquidity(self, wallet: Wallet, a_name, b_name, token_a_amount, token_b_amount):
        pool: Pool = self._pools[a_name + b_name]
        try:
            pool.add_liquidity(wallet, token_a_amount, token_b_amount)
        except ValueError as er:
            print("Add liquid failed: ", er)

    @commission
    def swap(self, wallet: Wallet, a_name, amount_a, b_name):
        amount_b = amount_a * self.list_price[a_name] / self.list_price[b_name]
        try:
            wallet.subtract_amount(a_name, amount_a)
            wallet.add_tokens(b_name, amount_b)
        except ValueError as er:
            print("Problem with swap: ", er)
