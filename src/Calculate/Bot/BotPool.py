from src.Calculate.ClassEnum.Network import Network
from src.Calculate.ResultData.ResultData import ResultData
from src.Calculate.Uniswap.Uniswap import Uniswap
from src.Calculate.Wallet.Wallet import Wallet
from src.Calculate.ClassEnum.Token import Token
from src.Calculate.WorkData.WorkData import WorkData


class BotPool:

    def __init__(self, _result_data: ResultData, _work_data: WorkData, wallet: Wallet, uniswap: Uniswap,
                 network: Network):
        self.wallet = wallet
        self.uniswap = uniswap
        self._price_deviation = None
        self.a_name = None
        self.b_name = None
        self._price_lower = None
        self._price_upper = None
        self.list_price = None
        self._network = network

        self._work_data = _work_data
        self._work_data.add_observer(self)
        self.result_data = _result_data

    def update(self):
        self.a_name = self._work_data.a_name
        self.b_name = self._work_data.b_name
        self.list_price = self._work_data.list_price

    def uniswap_strategy(self):
        self.convert_stable()
        self.swap_equal_a_b_token()
        self.pool_strategy()

    def convert_stable(self):
        usdt_amount = self.wallet.get_token_amount(Token.USDT.name)
        if usdt_amount > 0:
            usdt_for_network_coms = 10
            split_usdt_amount = (usdt_amount - usdt_for_network_coms) / 2
            self.uniswap.swap(self.wallet, Token.USDT.name, split_usdt_amount, self.a_name)
            self.uniswap.swap(self.wallet, Token.USDT.name, split_usdt_amount, self.b_name)
            self.uniswap.swap(self.wallet, Token.USDT.name, usdt_for_network_coms, self._network.name)

    def swap_equal_a_b_token(self):
        if not self.wallet.wallet_token_eq(self.a_name, self.b_name):
            token_a_price = self.get_token_price(self.a_name)
            token_b_price = self.get_token_price(self.b_name)
            token_a_amount = self.wallet.get_token_amount(self.a_name)
            token_b_amount = self.wallet.get_token_amount(self.b_name)
            difference = (token_a_amount * token_a_price - token_b_amount * token_b_price) / 2
            try:
                token_a_name = self.a_name
                token_b_name = self.b_name
                if not difference > 0:
                    token_a_name, token_b_name = token_b_name, token_a_name
                    token_a_price = token_b_price
                    difference = -difference
                Uniswap.swap(self.wallet, token_a_name, difference / token_a_price, token_b_name)
            except:
                print("Swap failed.")

    def pool_strategy(self):
        if not self.uniswap.has_pools():
            self.uniswap.create_pool(self.a_name, self.b_name)
            self.change_range_pool()
            self.add_liquidity_to_pool()
        elif self.uniswap.pool_in_range(self.a_name, self.b_name):
            self.add_liquidity_to_pool()
        else:
            self.uniswap.remove_pool(self.wallet, self.a_name, self.b_name)
            self.uniswap.create_pool(self.a_name, self.b_name)
            self.change_range_pool()
            self.add_liquidity_to_pool()

    @property
    def price_deviation(self):
        return self._price_deviation

    def set_price_deviation(self, price_deviation):
        self._price_deviation = price_deviation

    def set_range_for_pool(self):
        self.uniswap.set_range_pool(self.a_name, self.b_name, self._price_lower, self._price_upper)

    def set_network(self, network: Network):
        self._network = network

    def swap_token_necessary_value(self, a_name, b_name, necessary_value_a, token_a_value):
        token_b_amount_wallet = self.wallet.get_token_amount(b_name)
        amount_b_for_swap = (necessary_value_a - token_a_value) / self.get_token_price(b_name)
        if token_b_amount_wallet < amount_b_for_swap:
            raise ValueError(f"Not enough {b_name} in wallet.")
        self.uniswap.swap(self.wallet, b_name, amount_b_for_swap, a_name)

    def change_ratio_wallet_token(self):
        ratio_a = (self._price_upper - self.get_token_price(Token.PAIR.name)) / (
                self._price_upper - self._price_lower)
        ratio_b = 1 - ratio_a

        token_a_value = self.token_value(self.a_name)
        token_b_value = self.token_value(self.b_name)
        value_tokens = token_a_value + token_b_value

        necessary_value_a = value_tokens * ratio_a
        necessary_value_b = value_tokens * ratio_b
        try:

            if necessary_value_a > token_a_value:
                self.swap_token_necessary_value(self.a_name, self.b_name, necessary_value_a, token_a_value)

            elif necessary_value_b > token_b_value:
                self.swap_token_necessary_value(self.b_name, self.a_name, necessary_value_b, token_b_value)
        except ValueError as er:
            print(er)

    def add_liquidity_to_pool(self, overage=1):
        self.change_ratio_wallet_token()
        self.swap_for_coms()
        self.uniswap.add_liquidity(self.wallet, self.a_name, self.b_name,
                                   self.wallet.get_token_amount(self.a_name),
                                   self.wallet.get_token_amount(self.b_name))

    def swap_for_coms(self):
        network_amount = self.wallet.get_token_amount(self._network.name)
        lower_coms, upper_coms = self._network.value
        if network_amount <= upper_coms * 3 * self.list_price[self._network.name]:
            need_coms_amount = upper_coms * 2.5 * self.list_price[self._network.name]
            self.uniswap.swap(self.wallet, self.a_name, need_coms_amount / self.list_price[self.a_name],
                              self._network.name)
            self.uniswap.swap(self.wallet, self.b_name, need_coms_amount / self.list_price[self.b_name],
                              self._network.name)

    def get_token_price(self, token_name):
        return self.list_price[token_name]

    def token_value(self, token_name, amount=None, price=None):
        if not amount:
            amount = self._work_data.list_price[token_name]
        if not price:
            price = self._work_data.list_price[token_name]
        return amount * price

    def change_range_pool(self):
        pair_price = self.get_token_price(Token.PAIR.name)
        deviation = self._price_deviation * self.get_token_price(Token.PAIR.name)
        self._price_lower = pair_price - deviation
        self._price_upper = pair_price + deviation
        self.set_range_for_pool()
