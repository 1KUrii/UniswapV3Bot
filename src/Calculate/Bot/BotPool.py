import datetime


class BotPool:
    def __init__(self, token_a_name, token_b_name, starting_capital):
        self.list_token = {token_a_name: {"amount": 0}, token_b_name: {"amount": 0}}
        self.log_transaction = {token_a_name: [], token_b_name: []}
        self.capital = starting_capital

    def start_uniswap_strategy(self):
        pass











































    # def add_token(self, token_name, token_amount, token_price, token_date_buy):
    #     if token_name in self.list_token.keys():
    #         self.list_token[token_name].append({"amount": token_amount, "price": token_price, "date": token_date_buy})
    #     else:
    #         self.list_token[token_name] = [{"amount": token_amount, "price": token_price, "date": token_date_buy}]
    #
    # def remove_token(self, token_name, token_amount, token_price, token_date_sell):
    #     if token_name in self.list_token.keys():
    #         remaining_amount = token_amount
    #         for token in self.list_token[token_name]:
    #             if token["amount"] <= remaining_amount:
    #                 remaining_amount -= token["amount"]
    #                 self.list_token[token_name].remove(token)
    #             else:
    #                 token["amount"] -= remaining_amount
    #                 token["price"] = token_price
    #                 token["date"] = token_date_sell
    #                 break
    #
    # def get_holdings(self, token_prices):
    #     holdings = {}
    #     for token_name, token_data in self.list_token.items():
    #         token_value = sum([token["amount"] * token_prices[token_name] for token in token_data])
    #         holdings[token_name] = {"tokens": token_data, "value": token_value}
    #     return holdings
    #
    # def out_wallet(self, token_prices):
    #     holdings = self.get_holdings(token_prices)
    #     for token_name, token_data in holdings.items():
    #         print(f"{token_name}:")
    #         for token in token_data["tokens"]:
    #             print(f"\t{token['amount']} {token_name} at {token['price']} {token['date']}")
    #         print(f"\tCurrent value: {token_data['value']:.2f} USD")


# def main():
#     Bob = BotPool("BTC", 13, 23300, datetime.date(2023, 3, 5))
#     Bob.add_token("ETH", 7, 1700, datetime.date(2023, 3, 4))
#     Bob.add_token("ETH", 7, 1600, datetime.date(2023, 3, 4))
#     Bob.out_wallet({"BTC": 24000, "ETH": 1800})
#     Bob.add_token("ETH", 11, 1900, datetime.date(2023, 4, 5))
#     Bob.remove_token("BTC", 7, 18300, datetime.date(2023, 4, 5))
#     Bob.out_wallet({"BTC": 17000, "ETH": 1100})


if __name__ == "__main__":
    main()
