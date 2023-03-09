from matplotlib import pyplot as plt


class Gui:
    def create_chart_price(self, close_date, close_price):
        plt.style.use('seaborn')
        plt.plot(close_date, close_price)
        plt.title('Price Ratio of MATIC to CRV')
        plt.xlabel('Date')
        plt.ylabel('Price Ratio')
        plt.tight_layout()
        plt.show()
