import pytest
from src.processing import filter_by_state, sort_by_date  # замените your_module на имя вашего модуля



# --- ФИКСТУРЫ ---

@pytest.fixture
def sample_transactions():
    """Фикстура: список транзакций для тестирования."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01T10:00:00"},
        {"id": 2, "state": "PENDING", "date": "2023-01-02T11:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03T12:00:00"},
        {"id": 4, "state": "FAILED", "date": "2023-01-04T13:00:00"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-05T14:00:00"},
    ]



@pytest.fixture
def empty_transactions():
    """Фикстура: пустой список транзакций."""
    return []



@pytest.fixture
def transactions_with_missing_keys():
    """Фикстура: транзакции с отсутствующими ключами 'state' или 'date'."""
    return [
        {"id": 1, "date": "2023-01-01T10:00:00"},  # нет 'state'
        {"id": 2, "state": "EXECUTED"},  # нет 'date'
        {"id": 3},  # нет ни 'state', ни 'date'
    ]



# --- ТЕСТЫ ДЛЯ filter_by_state ---

def test_filter_by_state_default(sample_transactions):
    """Тест: фильтрация по умолчанию (state='EXECUTED')."""
    result = filter_by_state(sample_transactions)
    assert len(result) == 3
    assert all(t["state"] == "EXECUTED" for t in result)
    assert [t["id"] for t in result] == [1, 3, 5]



def test_filter_by_state_pending(sample_transactions):
    """Тест: фильтрация по state='PENDING'."""
    result = filter_by_state(sample_transactions, "PENDING")
    assert len(result) == 1
    assert result[0]["id"] == 2



def test_filter_by_state_not_found(sample_transactions):
    """Тест: state не найден — возвращаем пустой список."""
    result = filter_by_state(sample_transactions, "CANCELLED")
    assert result == []



def test_filter_by_state_empty_list(empty_transactions):
    """Тест: пустой список транзакций."""
    result = filter_by_state(empty_transactions, "EXECUTED")
    assert result == []



def test_filter_by_state_missing_state_key(transactions_with_missing_keys):
    """Тест: транзакции без ключа 'state' — не попадают в результат."""
    result = filter_by_state(transactions_with_missing_keys, "EXECUTED")
    # Только транзакция с "state": "EXECUTED" и полным ключом
    assert len(result) == 1
    assert result[0]["id"] == 2



@pytest.mark.parametrize(
    "transactions,state,expected_count",
    [
        ([], "EXECUTED", 0),
        ([{"state": "EXECUTED"}], "EXECUTED", 1),
        ([{"state": "PENDING"}], "EXECUTED", 0),
        ([{"state": "EXECUTED"}, {"state": "FAILED"}], "FAILED", 1),
    ]
)
def test_filter_by_state_parametrized(transactions, state, expected_count):
    """Параметризованный тест: разные комбинации входных данных."""
    result = filter_by_state(transactions, state)
    assert len(result) == expected_count



# --- ТЕСТЫ ДЛЯ sort_by_date ---

def test_sort_by_date_ascending(sample_transactions):
    """Тест: сортировка по дате в прямом порядке (reverse=False)."""
    result = sort_by_date(sample_transactions, reverse=False)
    expected_order = [
        "2023-01-01T10:00:00",
        "2023-01-02T11:00:00",
        "2023-01-03T12:00:00",
        "2023-01-04T13:00:00",
        "2023-01-05T14:00:00",
    ]
    assert [t["date"] for t in result] == expected_order




def test_sort_by_date_empty_list(empty_transactions):
    """Тест: пустой список — возвращаем пустой."""
    result = sort_by_date(empty_transactions)
    assert result == []



def test_sort_by_date_single_transaction():
    """Тест: один элемент — возвращается как есть."""
    transaction = [{"id": 1, "date": "2023-01-01T10:00:00"}]
    result = sort_by_date(transaction)
    assert result == transaction



def test_sort_by_date_missing_date_key(transactions_with_missing_keys):
    """Тест: транзакции без 'date' — вызывают KeyError."""
    with pytest.raises(KeyError):
        sort_by_date(transactions_with_missing_keys)




def test_sort_by_date_all_same_dates(sample_transactions):
    """Тест: все даты одинаковые — порядок сохраняется (stable sort)."""
    transactions = [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "date": "2023-01-01"},
        {"id": 3, "date": "2023-01-01"},
    ]
    result = sort_by_date(transactions, reverse=True)
    assert [t["id"] for t in result] == [1, 2, 3]  # исходный порядок сохранён




#@pytest.mark.