import json
import logging
import os
from typing import Any, Dict, List

from logger_config import setup_logger

# Инициализируем логгер для модуля utils
logger = setup_logger("utils")


def load_transactions(file_path: str = None) -> List[Dict[str, Any]]:

    try:
        # Логируем начало загрузки транзакций
        logger.info(f"Начало загрузки транзакций. Переданный путь: {file_path}")

        # Если путь не указан, используем путь по умолчанию
        if file_path is None:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(current_dir, "data", "operations.json")
            logger.debug(f"Используется путь по умолчанию: {file_path}")

        # Проверяем существование файла
        if not os.path.exists(file_path):
            error_msg = f"Файл не найден: {file_path}"
            logger.error(error_msg)
            return []

        # Проверяем, что это файл
        if not os.path.isfile(file_path):
            error_msg = f"Указанный путь не является файлом: {file_path}"
            logger.error(error_msg)
            return []

        # Проверяем расширение файла
        if not file_path.lower().endswith(".json"):
            logger.warning(f"Файл имеет нестандартное расширение: {file_path}")

        # Получаем размер файла для информации
        file_size = os.path.getsize(file_path)
        logger.debug(f"Размер файла: {file_size} байт")

        # Читаем и парсим JSON файл
        logger.info(f"Чтение файла: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем тип данных
        if isinstance(data, list):
            transaction_count = len(data)
            logger.info(f"Успешно загружено {transaction_count} транзакций из файла {file_path}")

            # Логируем информацию о первой транзакции для примера
            if data:
                logger.debug(
                    f"Первая транзакция: {data[0].get('id', 'Неизвестно')} - {data[0].get('description', 'Без описания')}"
                )

            return data
        else:
            logger.warning(f"Загруженные данные не являются списком. Тип данных: {type(data)}")
            return []

    except FileNotFoundError as e:
        error_msg = f"Файл не найден: {str(e)}"
        logger.error(error_msg)
        return []

    except json.JSONDecodeError as e:
        error_msg = f"Ошибка декодирования JSON: {str(e)}"
        logger.error(error_msg)
        return []

    except PermissionError as e:
        error_msg = f"Отсутствуют права на чтение файла: {str(e)}"
        logger.error(error_msg)
        return []

    except Exception as e:
        error_msg = f"Неизвестная ошибка при загрузке транзакций: {str(e)}"
        logger.exception(error_msg)
        return []


def get_transaction_amount(transaction: Dict[str, Any]) -> float:

    try:
        amount = float(transaction.get("operationAmount", {}).get("amount", 0))
        logger.debug(f"Получена сумма транзакции {transaction.get('id')}: {amount}")
        return amount
    except (ValueError, TypeError) as e:
        logger.warning(f"Ошибка при получении суммы транзакции {transaction.get('id')}: {e}")
        return 0.0


def is_transaction_completed(transaction: Dict[str, Any]) -> bool:

    try:
        status = transaction.get("state", "").lower() == "executed"
        logger.debug(f"Статус транзакции {transaction.get('id')}: {'EXECUTED' if status else 'другой'}")
        return status
    except Exception as e:
        logger.warning(f"Ошибка при проверке статуса транзакции {transaction.get('id')}: {e}")
        return False


def get_transaction_date(transaction: Dict[str, Any]) -> str:

    try:
        date = transaction.get("date", "")
        logger.debug(f"Дата транзакции {transaction.get('id')}: {date}")
        return date
    except Exception as e:
        logger.warning(f"Ошибка при получении даты транзакции {transaction.get('id')}: {e}")
        return ""


if __name__ == "__main__":
    # Тестирование при прямом запуске
    print("Тестирование load_transactions...")
    transactions = load_transactions()

    if transactions:
        print(f"Успешно загружено {len(transactions)} транзакций")
        print("\nПервые 3 транзакции:")

        # Простой вывод без отдельной функции
        for i, transaction in enumerate(transactions[:3], 1):
            print(f"\n--- Транзакция #{i} ---")
            print(f"ID: {transaction.get('id', 'N/A')}")
            print(f"Статус: {transaction.get('state', 'N/A')}")
            print(f"Дата: {transaction.get('date', 'N/A')}")
            print(f"Описание: {transaction.get('description', 'N/A')}")

            operation_amount = transaction.get("operationAmount", {})
            amount = operation_amount.get("amount", "N/A")
            currency = operation_amount.get("currency", {})
            currency_name = currency.get("name", "N/A")
            print(f"Сумма: {amount} {currency_name}")

            if "from" in transaction:
                print(f"Откуда: {transaction['from']}")
            if "to" in transaction:
                print(f"Куда: {transaction['to']}")

            print("-" * 40)
    else:
        print("Транзакции не загружены или файл пуст")
