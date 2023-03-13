from matplotlib import pyplot as plt

from src.Calculate.Calculate import Calculate


class Gui:
    def __init__(self):
        calculate = Calculate()
        # self.create_chart_price(*calculate)
    def create_chart_price(self, close_date, close_price):
        plt.style.use('seaborn')
        plt.plot(close_date, close_price)
        plt.title('Price Ratio of MATIC to CRV')
        plt.xlabel('Date')
        plt.ylabel('Price Ratio')
        plt.tight_layout()
        plt.show()
