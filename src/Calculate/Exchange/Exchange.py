import requests
import time
import hashlib
import hmac
import json
from datetime import datetime
from src.Calculate.Exchange.data import API_KEY, SECRET_KEY


class Exchange:
    def __init__(self):
        self.api_key = API_KEY
        self.secret_key = SECRET_KEY
        self.httpClient = requests.Session()
        self.recv_window = str(5000)
        self.url = "https://api.bybit.com"

    def http_request(self, end_point, method, payload, info):
        global time_stamp
        time_stamp = str(int(time.time() * 10 ** 3))
        signature = self.gen_signature(payload)
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': self.recv_window,
            'Content-Type': 'application/json'
        }
        if method == "POST":
            return self.httpClient.request(method, self.url + end_point, headers=headers, data=payload)
        else:
            return self.httpClient.request(method, self.url + end_point + "?" + payload, headers=headers).json()

    def gen_signature(self, payload):
        param_str = str(time_stamp) + self.api_key + self.recv_window + payload
        hash = hmac.new(bytes(self.secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        return signature

    def timestamp(self, dt):
        epoch = datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds() * 1000.0

    def write_price_file(self, price_volume):
        with open("../price_volume", 'w') as f:
            price_volume = json.dumps(price_volume)
            f.write(price_volume)

    def read_price_file(self):
        with open("../price_volume", 'r') as f:
            price_volume = json.loads(f.read())
            return price_volume

    def get_kline(self, category, symbol, interval, start, end):
        if not (isinstance(start, datetime) and isinstance(end, datetime)):
            start = datetime(start[0], start[1], start[2])
            end = datetime(end[0], end[1], end[2])
        start_timestamp = int(self.timestamp(start))
        end_timestamp = int(self.timestamp(end))
        endpoint = "/v5/market/kline"
        method = "GET"
        params = f"category={category}&symbol={symbol}&interval={interval}&start={start_timestamp}&end={end_timestamp}"
        response = self.http_request(endpoint, method, params, "Get Kline")
        if response.get('retCode') == '0':
            raise Exception(f"API error: {response.get('message')}")
        return response.get('result', {}).get('list', [])

    def get_time_prices(self, symbol_a, symbol_b, interval, start, end):
        price_volume_a = self.get_kline('spot', symbol_a, interval, start, end)
        price_volume_b = self.get_kline('spot', symbol_b, interval, start, end)
        close_date = []
        close_prices_pair = []
        close_prices_a = []
        close_prices_b = []
        for close_a, close_b in zip(price_volume_a, price_volume_b):
            close_date.append(datetime.utcfromtimestamp(int(close_a[0]) / 1000).date())
            close_prices_a.append(float(close_a[4]))
            close_prices_b.append(float(close_b[4]))
            close_prices_pair.append(float(close_a[4]) / float(close_b[4]))
        return close_date, close_prices_pair, close_prices_a, close_prices_b

    def main(self):
        price_volume_crv = self.get_kline('spot', 'CRVUSDT', 'D', (2022, 7, 31), (2023, 2, 16))
        price_volume_matic = self.get_kline('spot', 'MATICUSDT', 'D', (2022, 7, 31), (2023, 2, 16))
        # write_price_file(price_volume)
        # price_volume = read_price_file()
        close_date = []
        close_price = []
        for close_crv, close_matic in zip(price_volume_crv, price_volume_matic):
            close_date.append(datetime.utcfromtimestamp(int(close_crv[0]) / 1000).date())
            close_price.append(float(close_matic[4]) / float(close_crv[4]))

        print(close_price)


if __name__ == '__main__':
    m = Exchange()
    m.main()

