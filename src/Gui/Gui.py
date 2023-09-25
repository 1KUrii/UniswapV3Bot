from matplotlib import pyplot as plt
from src.Calculate.Calculate import Calculate
from src.Calculate.ResultData.ResultData import ResultData


class Gui:
    def __init__(self):
        self.calc = Calculate().calculate()
        self.data: ResultData = self.calc.get_result_data()
        self.all_timestamp = self.data.get_all_timestamp()
        self.f, self.ax = plt.subplots(2, 2)
        plt.style.use('seaborn')

    def create_chart_price(self):
        data = self.data.get_all_logs()
        self.ax[0, 0].semilogy(data.keys(), data.values())
        self.ax[0, 0].set_title(f'Price Ratio of {self.calc.a_name}/{self.calc.b_name}')
        # self.ax[0, 0].set_xlabel('Date')
        # self.ax[0, 0].set_ylabel('Price Ratio')

    def create_chart_wallet(self):
        wallet_data = self.data.get_wallet_logs()
        network = [i[0] for i in list(wallet_data.values())]
        self.ax[0, 1].plot(self.all_timestamp, network)
        self.ax[0, 1].set_title(f'Network tokens in Wallet over Time')
        # self.ax[0, 1].set_xlabel('Date')
        # self.ax[0, 1].set_ylabel(f'Number of {self.calc.network.name}')

    def create_chart_pool(self):
        pool_data = self.data.get_pool_logs()
        first_name, second_name = pool_data[0]
        self.ax[1, 0].plot(self.all_timestamp, pool_data[1], self.all_timestamp, pool_data[2])
        self.ax[1, 0].set_title(f'Tokens in Pools over Time')
        # self.ax[1, 0].set_xlabel('Date')
        # self.ax[1, 0].set_ylabel(f'Number of value {first_name} and {second_name} tokens')

    def create_chart_reward(self):
        reward_data = self.data.get_log_reward()
        self.ax[1, 1].semilogy(reward_data.keys(), reward_data.values(), '--o')
        self.ax[1, 1].set_title(f'Reward in Pools over Time')
        # self.ax[1, 1].set_xlabel('Date')
        # self.ax[1, 1].set_ylabel(f'reward tokens')

    def show(self):
        plt.show()
