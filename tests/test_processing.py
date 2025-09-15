import pytest

from src.processing import filter_by_state, sort_by_date


# Фикстуры
@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "amount": 100},
        {"id": 2, "state": "PENDING", "date": "2023-01-02", "amount": 200},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03", "amount": 300},
        {"id": 4, "state": "CANCELED", "date": "2023-01-04", "amount": 400},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-05", "amount": 500},
    ]


@pytest.fixture
def transactions_for_dates():
    return [
        {"id": 1, "date": "2023-03-01", "amount": 100},
        {"id": 2, "date": "2023-01-01", "amount": 200},
        {"id": 3, "date": "2023-02-01", "amount": 300},
        {"id": 4, "date": "2022-12-31", "amount": 400},
        {"id": 5, "date": "2023-03-15", "amount": 500},
    ]


# Тесты для filter_by_state
def test_filter_by_state_executed(sample_transactions):
    result = filter_by_state(sample_transactions, "EXECUTED")
    assert len(result) == 3
    assert all(t["state"] == "EXECUTED" for t in result)


def test_filter_by_state_default(sample_transactions):
    result = filter_by_state(sample_transactions)
    assert len(result) == 3
    assert all(t["state"] == "EXECUTED" for t in result)


def test_filter_by_state_empty_list():
    result = filter_by_state([], "EXECUTED")
    assert result == []


def test_filter_by_state_no_matches(sample_transactions):
    result = filter_by_state(sample_transactions, "COMPLETED")
    assert result == []


def test_filter_by_state_missing_key():
    transactions = [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-02"},
    ]
    result = filter_by_state(transactions, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 2


# Тесты для sort_by_date (это то, чего не хватает!)
def test_sort_by_date_descending(transactions_for_dates):
    """Тестирование сортировки по убыванию (по умолчанию)"""
    result = sort_by_date(transactions_for_dates)

    dates = [t["date"] for t in result]
    expected_dates = ["2023-03-15", "2023-03-01", "2023-02-01", "2023-01-01", "2022-12-31"]
    assert dates == expected_dates


def test_sort_by_date_ascending(transactions_for_dates):
    """Тестирование сортировки по возрастанию"""
    result = sort_by_date(transactions_for_dates, reverse=False)

    dates = [t["date"] for t in result]
    expected_dates = ["2022-12-31", "2023-01-01", "2023-02-01", "2023-03-01", "2023-03-15"]
    assert dates == expected_dates


def test_sort_by_date_empty_list():
    """Тестирование сортировки пустого списка"""
    result = sort_by_date([])
    assert result == []


def test_sort_by_date_single_element():
    """Тестирование сортировки списка с одним элементом"""
    transactions = [{"id": 1, "date": "2023-01-01"}]
    result = sort_by_date(transactions)
    assert result == transactions


def test_sort_by_date_with_duplicate_dates():
    """Тестирование сортировки с одинаковыми датами"""
    transactions = [
        {"id": 1, "date": "2023-01-01", "amount": 100},
        {"id": 2, "date": "2023-01-01", "amount": 200},
        {"id": 3, "date": "2023-01-02", "amount": 300},
    ]

    result = sort_by_date(transactions)
    # Проверяем что даты отсортированы правильно
    assert result[0]["date"] == "2023-01-02"
    assert result[1]["date"] == "2023-01-01"
    assert result[2]["date"] == "2023-01-01"


def test_sort_by_date_different_formats():
    """Тестирование с разными форматами дат"""
    transactions = [
        {"id": 1, "date": "2023-01-01T10:30:00"},
        {"id": 2, "date": "2023-01-01"},
        {"id": 3, "date": "2022-12-31"},
    ]

    result = sort_by_date(transactions)
    assert len(result) == 3
    # Должны быть отсортированы лексикографически
    assert result[0]["date"] == "2023-01-01T10:30:00" or result[0]["date"] == "2023-01-01"


# Дополнительные тесты для полного покрытия
def test_sort_by_date_reverse_true_explicit():
    """Явное указание reverse=True"""
    transactions = [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "date": "2023-01-02"},
    ]

    result = sort_by_date(transactions, reverse=True)
    assert result[0]["date"] == "2023-01-02"
    assert result[1]["date"] == "2023-01-01"


def test_sort_by_date_reverse_false():
    """Явное указание reverse=False"""
    transactions = [
        {"id": 1, "date": "2023-01-02"},
        {"id": 2, "date": "2023-01-01"},
    ]

    result = sort_by_date(transactions, reverse=False)
    assert result[0]["date"] == "2023-01-01"
    assert result[1]["date"] == "2023-01-02"


# Интеграционные тесты
def test_filter_then_sort():
    """Интеграционный тест: фильтрация + сортировка"""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2023-03-01"},
        {"id": 2, "state": "PENDING", "date": "2023-01-01"},
        {"id": 3, "state": "EXECUTED", "date": "2023-02-01"},
    ]

    filtered = filter_by_state(transactions, "EXECUTED")
    sorted_result = sort_by_date(filtered)

    assert len(sorted_result) == 2
    assert sorted_result[0]["id"] == 1  # Самая поздняя дата
    assert sorted_result[1]["id"] == 3  # Более ранняя дата


def test_complex_workflow():
    """Комплексный тест всего workflow"""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-10", "amount": 1000},
        {"id": 2, "state": "PENDING", "date": "2023-01-05", "amount": 500},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-15", "amount": 1500},
        {"id": 4, "state": "EXECUTED", "date": "2023-01-01", "amount": 200},
    ]

    # Фильтруем
    executed = filter_by_state(transactions, "EXECUTED")
    assert len(executed) == 3

    # Сортируем
    sorted_executed = sort_by_date(executed)

    # Проверяем
    assert sorted_executed[0]["date"] == "2023-01-15"
    assert sorted_executed[1]["date"] == "2023-01-10"
    assert sorted_executed[2]["date"] == "2023-01-01"
    assert all(t["state"] == "EXECUTED" for t in sorted_executed)


def sort_by_date(transactions, reverse=True):
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)


# Тестовые данные
transactions = [
    {"id": 1, "date": "2023-01-15", "amount": 100},
    {"id": 2, "date": "2023-03-10", "amount": 200},
    {"id": 3, "date": "2023-02-05", "amount": 150},
    {"id": 4, "date": "2023-01-01", "amount": 50},
]

duplicate_dates = [
    {"id": 1, "date": "2023-01-15", "amount": 100},
    {"id": 2, "date": "2023-01-15", "amount": 200},
    {"id": 3, "date": "2023-02-05", "amount": 150},
]


def test_sort_descending():
    """Сортировка по убыванию дат"""
    result = sort_by_date(transactions, reverse=True)
    dates = [t["date"] for t in result]
    assert dates == ["2023-03-10", "2023-02-05", "2023-01-15", "2023-01-01"]

def test_sort_ascending():
    """Сортировка по возрастанию дат"""
    result = sort_by_date(transactions, reverse=False)
    dates = [t["date"] for t in result]
    assert dates == ["2023-01-01", "2023-01-15", "2023-02-05", "2023-03-10"]

def test_default_reverse():
    """Проверка значения по умолчанию reverse=True"""
    result_default = sort_by_date(transactions)
    result_explicit = sort_by_date(transactions, reverse=True)
    assert result_default == result_explicit


def test_duplicate_dates_stability():
    """Стабильность сортировки при одинаковых датах"""
    result = sort_by_date(duplicate_dates, reverse=True)

    # Находим транзакции с одинаковой датой
    jan_15 = [t for t in result if t["date"] == "2023-01-15"]

    # Проверяем сохранение исходного порядка
    assert [t["id"] for t in jan_15] == [1, 2]

def test_empty_list():
    """Обработка пустого списка"""
    result = sort_by_date([])
    assert result == []

def test_single_element():
    """Обработка списка с одним элементом"""
    single = [{"id": 1, "date": "2023-01-01", "amount": 100}]
    result = sort_by_date(single)
    assert result == single


def test_missing_date_key():
    """Ошибка при отсутствии ключа 'date'"""
    invalid = [{"id": 1, "amount": 100}]  # Нет ключа date

    with pytest.raises(KeyError):
        sort_by_date(invalid)
