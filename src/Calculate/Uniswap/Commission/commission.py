from src.Calculate.Wallet.Wallet import Wallet


def commission(func):
    def _wrapper(self, wallet: Wallet, *args, **kwargs):
        import random
        coms = random.uniform(*wallet.network.value) / self.list_price[wallet.network.name]
        if wallet.get_token_amount(wallet.network.name) < coms:
            raise ValueError(f"Not enough {wallet.network.name} tokens in the wallet for commission")
        wallet.subtract_amount(wallet.network.name, coms)
        wallet.result_data.logging_commission(coms)
        result = func(self, wallet, *args, **kwargs)
        return result

    return _wrapper
