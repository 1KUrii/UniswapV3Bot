from src.Gui.Gui import Gui


def app():
    gui = Gui()
    gui.create_chart_price()
    gui.create_chart_wallet()
    gui.create_chart_pool()
    gui.create_chart_reward()
    gui.show()

if __name__ == '__main__':
    app()
