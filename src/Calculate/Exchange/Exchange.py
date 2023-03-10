import hashlib
import hmac
import json
import time
from datetime import datetime

import requests

from src.Calculate.Exchange.data import API_KEY, SECRET_KEY


class Exchange:
    URL = "https://api.bybit.com"
    RECV_WINDOW = "5000"
    CONTENT_TYPE = "application/json"
    SIGN_TYPE = "2"

    def __init__(self):
        self.api_key = API_KEY
        self.secret_key = SECRET_KEY
        self.httpClient = requests.Session()

    def http_request(self, end_point, method, payload):
        time_stamp = str(int(time.time() * 10 ** 3))
        signature = self.gen_signature(payload, time_stamp)
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': self.SIGN_TYPE,
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': self.RECV_WINDOW,
            'Content-Type': self.CONTENT_TYPE
        }
        if method == "POST":
            return self.httpClient.request(method, self.URL + end_point, headers=headers, data=payload)
        else:
            return self.httpClient.request(method, self.URL + end_point + "?" + payload, headers=headers).json()

    def gen_signature(self, payload, time_stamp):
        param_str = str(time_stamp) + self.api_key + self.RECV_WINDOW + payload
        hash = hmac.new(bytes(self.secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        return signature

    def timestamp(self, dt):
        epoch = datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds() * 1000.0

    def write_price_file(self, price_volume):
        with open("../price_volume", 'w') as f:
            json.dump(price_volume, f)

    def read_price_file(self):
        with open("../price_volume", 'r') as f:
            return json.load(f)

    def get_kline(self, category, symbol, interval, start, end):
        if not all(isinstance(d, datetime) for d in [start, end]):
            start = datetime(*start)
            end = datetime(*end)
        start_timestamp = int(self.timestamp(start))
        end_timestamp = int(self.timestamp(end))
        endpoint = "/v5/market/kline"
        method = "GET"
        params = f"category={category}&symbol={symbol}&interval={interval}&start={start_timestamp}&end={end_timestamp}"
        response = self.http_request(endpoint, method, params)
        if response.get('retCode') == '0':
            raise Exception(f"API error: {response.get('message')}")
        return response.get('result', {}).get('list', [])

    def get_time_prices(self, symbol_a, symbol_b, interval, start, end):
        try:
            price_volume_a = self.get_kline('spot', symbol_a, interval, start, end)
            price_volume_b = self.get_kline('spot', symbol_b, interval, start, end)
        except Exception as e:
            raise ValueError(
                f"Error getting prices for symbols {symbol_a} and {symbol_b} with interval {interval}: {str(e)}")

        close_date = [datetime.utcfromtimestamp(int(close_a[0]) / 1000).date() for close_a in price_volume_a]
        close_prices_a = [float(close_a[4]) for close_a in price_volume_a]
        close_prices_b = [float(close_b[4]) for close_b in price_volume_b]
        close_prices_pair = [pa / pb for pa, pb in zip(close_prices_a, close_prices_b)]

        return close_date[::-1], close_prices_pair[::-1], close_prices_a[::-1], close_prices_b[::-1]


    def main(self):
        price_volume_crv = self.get_kline('spot', 'CRVUSDT', 'D', (2022, 7, 31), (2023, 2, 16))
        price_volume_matic = self.get_kline('spot', 'MATICUSDT', 'D', (2022, 7, 31), (2023, 2, 16))
        close_date = []
        close_price = []
        for close_crv, close_matic in zip(price_volume_crv, price_volume_matic):
            close_date.append(datetime.utcfromtimestamp(int(close_crv[0]) / 1000).date())
            close_price.append(float(close_matic[4]) / float(close_crv[4]))

        print(close_price)


if __name__ == '__main__':
    m = Exchange()
    m.main()