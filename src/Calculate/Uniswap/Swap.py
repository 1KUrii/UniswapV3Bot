from src.Calculate.Wallet.Wallet import Wallet


class Swap:
    USDT = "USDT"
    TIMESTAMP = "timestamp"
    PAIR = "PAIR"

    def __init__(self, wallet: Wallet, token_a_name, token_b_name):
        self.token_a_name = token_a_name
        self.token_b_name = token_b_name
        self.wallet = wallet

    def swap_tokens(self, token_a_name, amount_a, token_b_name):
        token_a_amount = self.wallet.list_token_amount[token_a_name]
        if token_a_amount < amount_a:
            print(f"Not enough {token_a_name} tokens in the wallet")
        else:
            amount_b = amount_a * self.wallet.list_token_prices[token_a_name] / self.wallet.list_token_prices[
                token_b_name]
            self.wallet.list_token_amount[token_a_name] -= amount_a
            self.wallet.list_token_amount[token_b_name] += amount_b
            print(f"{amount_a} {token_a_name} tokens swapped for {amount_b} {token_b_name} tokens")
