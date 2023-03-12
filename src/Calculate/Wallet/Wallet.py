class Wallet:
    USDT = "USDT"
    TIMESTAMP = "timestamp"
    PAIR = "PAIR"

    def __init__(self, token_a_name, token_b_name, starting_capital):
        self.token_a_name = token_a_name
        self.token_b_name = token_b_name
        self.list_token_amount = {
            self.token_a_name: 0,
            self.token_b_name: 0,
            self.USDT: starting_capital
        }