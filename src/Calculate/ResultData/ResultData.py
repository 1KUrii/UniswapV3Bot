class ResultData:

    def __init__(self):
        self.log_commissions = {}
        self._log_reward = {}

        self.log_wallet = {}
        self.log_pool = {}
        self.current_timestamp = 0
        self._all_timestamp = []
        self._all_prices = {}

        self.list_price = {}
        self.all_data = []

        self._observers = []

    def logged(self):
        self.notify_observers()
        self.all_data.append(
            [self.current_timestamp,
             self.log_wallet[self.current_timestamp].copy(),
             self.log_pool[self.current_timestamp].copy(),
             self.list_price[self.current_timestamp].copy()])

    def set_timestamp(self, timestamp):
        self.current_timestamp = timestamp
        self._all_timestamp.append(timestamp)

    def get_log_reward(self):
        return self._log_reward

    def get_all_timestamp(self):
        return self._all_timestamp

    def set_list_price(self, list_price):
        self.list_price[self.current_timestamp] = list_price
        self._all_prices[self.current_timestamp] = list_price

    def logging_pool(self, a_name, a_amount, b_name, b_amount):
        self.log_pool[self.current_timestamp] = {a_name: a_amount, b_name: b_amount}

    def logging_wallet(self, token_amount):
        self.log_wallet[self.current_timestamp] = token_amount.copy()

    def logging_commission(self, amount_commission):
        if not self.log_commissions.get(self.current_timestamp):
            self.log_commissions[self.current_timestamp] = amount_commission
        else:
            self.log_commissions[self.current_timestamp] += amount_commission

    def logging_reward(self, reward):
        if not self._log_reward.get(self.current_timestamp):
            self._log_reward[self.current_timestamp] = reward
        else:
            self._log_reward[self.current_timestamp] += reward

    def token_value(self, token_name, amount=None, price=None):
        if amount is None:
            amount = self.list_price[token_name]
        if price is None:
            price = self.list_price[token_name]
        return amount * price

    def portfolio_value(self, list_token_amount):
        value = 0
        for token_name, token_amount in list_token_amount.items():
            value += self.token_value(token_name, token_amount)
        return value

    def get_wallet_logs(self):
        date_and_value = {}
        for timestamp, tokens_amount in self.log_wallet.items():
            date_and_value[timestamp] = []
            for token_name, token_amount in tokens_amount.items():
                date_and_value[timestamp].append(token_amount)

        return date_and_value

    def get_pool_logs(self):
        token_name_list = []
        token_one = []
        token_two = []
        for timestamp, log_pool in self.log_pool.items():
            for i, (token_name, token_amount) in enumerate(log_pool.items()):
                if token_name not in token_name_list:
                    token_name_list.append(token_name)
                if i == 0:
                    token_one.append(token_amount)
                else:
                    token_two.append(token_amount)

        return token_name_list, token_one, token_two

    def get_all_logs(self):
        all_log = self.all_data
        date_and_value = {}

        for timestamp, log_wallet, log_pool, list_token_prices in all_log:
            date_and_value[timestamp] = 0
            for token_name, token_amount in log_wallet.items():
                date_and_value[timestamp] += self.token_value(token_name, token_amount,
                                                              list_token_prices[token_name])

            for token_name, token_amount in log_pool.items():
                date_and_value[timestamp] += self.token_value(token_name, token_amount,
                                                              list_token_prices[token_name])

        return date_and_value

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.logged()
