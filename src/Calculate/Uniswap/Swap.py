from src.Calculate.Wallet.Wallet import Wallet


# может побольше методов добавить
class Swap:
    USDT = "USDT"
    TIMESTAMP = "timestamp"
    PAIR = "PAIR"

    def __init__(self, wallet: Wallet):
        self.wallet = wallet

    def swap_tokens(self, a_name, amount_a, b_name):
        token_a_amount = self.wallet.list_token_amount[a_name]
        if token_a_amount < amount_a:
            print(f"Not enough {a_name} tokens in the wallet")
        else:
            amount_b = amount_a * self.wallet.list_price[a_name] / self.wallet.list_price[b_name]
            self.wallet.list_token_amount[a_name] -= amount_a
            self.wallet.list_token_amount[b_name] += amount_b
            print(f"{amount_a} {a_name} tokens swapped for {amount_b} {b_name} tokens")
