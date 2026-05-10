import pandas as pd
from typing import List, Dict, Any


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:

    try:
        df = pd.read_csv(file_path, delimiter=';')
        transactions = df.to_dict('records')
        print(f"Загружено {len(transactions)} транзакций из {file_path}")
        return transactions
    except Exception as e:
        print(f"Ошибка при чтении CSV-файла: {e}")
        return []


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:

    try:
        df = pd.read_excel(file_path)
        df = df.where(pd.notnull(df), None)
        transactions = df.to_dict('records')
        print(f"Загружено {len(transactions)} транзакций из {file_path}")
        return transactions
    except Exception as e:
        print(f"Ошибка при чтении Excel-файла: {e}")
        return []


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    if file_path.endswith('.csv'):
        return load_transactions_from_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return load_transactions_from_excel(file_path)
    else:
        print(f"Неподдерживаемый формат файла: {file_path}")
        return []


# Пример использования
if __name__ == "__main__":
    # Загрузка из CSV
    csv_transactions = load_transactions("transactions.csv")
    print("\nТранзакции из CSV:")
    for i, transaction in enumerate(csv_transactions[:3], 1):
        print(f"{i}. {transaction}")

    print("\n" + "=" * 80 + "\n")

    # Загрузка из Excel
    excel_transactions = load_transactions("transactions_excel.xlsx")
    print("Транзакции из Excel:")
    for i, transaction in enumerate(excel_transactions[:3], 1):
        print(f"{i}. {transaction}")