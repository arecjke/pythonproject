import os

import requests
from dotenv import load_dotenv


def converter_currency(transaction: float, currency: str) -> float:
    """Конвертер валюты в рубли через API"""

    # Проверка типа данных суммы ТОЛЬКО если это не число
    if not isinstance(transaction, (int, float)):
        print(f"Введена неверная сумма транзакции")
        return None

    # Проверяем, что transaction - число (int или float)
    try:
        amount = float(transaction)
    except (ValueError, TypeError):
        print(f"Введена неверная сумма транзакции")
        return None

    # Условие валюты
    currency_to_convert = ["USD", "EUR"]
    if currency not in currency_to_convert:
        print("Такой валюты нет в списке")
        return None

    # Загружаем переменные окружения
    load_dotenv(".env")
    API_KEY = os.getenv("API_KEY")

    # Проверяем наличие API ключа
    if not API_KEY:
        print("API_KEY не найден в .env файле")
        return None

    # Запускаем API запрос
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"

    payload = {}
    headers = {"apikey": API_KEY}

    try:
        response = requests.request("GET", url, headers=headers, data=payload, timeout=10)

        # Проверка на ошибки запроса
        if response.status_code != 200:
            print(f"Ошибка запроса: {response.status_code}")
            print(f"Ответ сервера: {response.text}")
            return None

        # Парсим результат
        result_data = response.json()
        if "result" not in result_data:
            print("Ошибка: в ответе API нет поля 'result'")
            print(f"Полный ответ: {result_data}")
            return None

        converted_amount = round(result_data["result"], 2)
        return converted_amount

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
        return None


if __name__ == "__main__":
    # Тестовые вызовы
    print("Тест 1 (USD):", converter_currency(174, "USD"))
    print("Тест 2 (EUR):", converter_currency(678, "EUR"))
