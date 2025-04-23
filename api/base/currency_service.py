import requests
from datetime import datetime

CBU_API_URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"


def get_currency_rate(code):
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        response = requests.get(f"{CBU_API_URL}{code}/{today}/")
        response.raise_for_status()
        data = response.json()
        if data and 'Rate' in data[0]:
            return float(data[0]['Rate'].replace(',', '.'))
    except Exception as e:
        print(f"Currency API error: {e}")
        return None


