import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(currency: str, currency_transfer: str, amount: str):

        if currency == currency_transfer:
            raise ConvertionException(f'Невозможно перенести одинаковые валюты в {currency_transfer}.')

        try:
            currency_ticker = keys[currency]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {currency}.')

        try:
            currency_transfer_ticker = keys[currency_transfer]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {currency_transfer}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}.')

        r = requests.get(f'https://free.currconv.com/api/v7/convert?'
                         f'q={keys[currency]}_{keys[currency_transfer]}'
                         f'&compact=ultra&apiKey=47fe5ff55bc66ea40005')
        total_base = json.loads(r.content)[f'{currency_ticker}_{currency_transfer_ticker}']

        return total_base
