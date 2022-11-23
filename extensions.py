import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod                       # метод для преобразования amount и последующего его вывода в правильном виде
    def amount_transform(amount: str):  # (без "," "+" и нулевой десятичной дроби если пользователь вводит целое число)
        try:
            amount = float(amount) if ',' not in amount else float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"')
        if amount < 0:
            raise APIException(f'Отрицательное количество')
        return amount if amount % 1 != 0 else int(amount)

    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты "{base}".')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount
        return total_base
