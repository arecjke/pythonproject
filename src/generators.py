def filter_by_currency(transactions, currency_code):
    """
    Функция, которая фильтрует транзакции по коду валюты и возвращает итератор.

        transactions: список словарей с транзакциями
        currency_code: код валюты для фильтрации (например, "USD")

    """
    for transaction in transactions:
        # Проверяем, что транзакция имеет структуру operationAmount -> currency -> code
        if (transaction.get('operationAmount') and
                transaction['operationAmount'].get('currency') and
                transaction['operationAmount']['currency'].get('code') == currency_code):
            yield transaction


# Примеры
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {
                "name": "рубли",
                "code": "RUB"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160"
    }
]


#usd_transactions = filter_by_currency(transactions, "USD")
#for _ in range(2):
#    print(next(usd_transactions))


def transaction_descriptions(transactions):
    """
    Генератор, который возвращает описание каждой транзакции по очереди.
    """
    for transaction in transactions:
        yield transaction.get('description', '')

# Использование генератора
#descriptions = transaction_descriptions(transactions)
#for _ in range(5):
#   print(next(descriptions))


def card_number_generator(start, end):
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

        start: начальный номер карты (целое число от 1)
        end: конечный номер карты (целое число до 9999999999999999)

    """
    for number in range(start, end + 1):
        # Преобразуем число в строку и дополняем нулями до 16 цифр
        card_str = str(number).zfill(16)

        # Форматируем строку: XXXX XXXX XXXX XXXX
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"

        yield formatted_card

#for card_number in card_number_generator(1, 5):
#    print(card_number)
