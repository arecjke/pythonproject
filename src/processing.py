def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """

    Фильтрует список словарей по значению ключа 'state'.

    """
    return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """

    Функция, которая принимает список словарей и необязательный параметр, задающий порядок сортировки.

    """
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)
