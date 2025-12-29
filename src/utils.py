import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str = None) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path (str, optional): Путь до JSON-файла. Если не указан,
                                  используется путь по умолчанию.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
    """
    # Если путь не указан, используем путь по умолчанию
    if file_path is None:
        # Получаем абсолютный путь к директории проекта
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(current_dir, "data", "operations.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        else:
            return []

    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception:
        return []


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
