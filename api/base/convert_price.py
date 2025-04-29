from base import CURRENCY_CHOICES


def convert_price(price, currency):
    return price * CURRENCY_CHOICES[currency]
