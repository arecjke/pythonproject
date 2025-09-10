import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

class TestFilterByCurrency:

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с примерными транзакциями для тестирования."""
        return [
            {
                "id": 1,
                "operationAmount": {
                    "amount": "100.00",
                    "currency": {"name": "USD", "code": "USD"}
                }
            },
            {
                "id": 2,
                "operationAmount": {
                    "amount": "200.00",
                    "currency": {"name": "EUR", "code": "EUR"}
                }
            },
            {
                "id": 3,
                "operationAmount": {
                    "amount": "300.00",
                    "currency": {"name": "USD", "code": "USD"}
                }
            },
            {
                "id": 4,
                "operationAmount": {
                    "amount": "400.00",
                    "currency": {"name": "RUB", "code": "RUB"}
                }
            }
        ]

    def test_filter_usd_transactions(self, sample_transactions):
        """Тест фильтрации USD транзакций."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))

        assert len(usd_transactions) == 2
        assert usd_transactions[0]["id"] == 1
        assert usd_transactions[1]["id"] == 3
        assert all(tx["operationAmount"]["currency"]["code"] == "USD"
                   for tx in usd_transactions)

    def test_filter_eur_transactions(self, sample_transactions):
        """Тест фильтрации EUR транзакций."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))

        assert len(eur_transactions) == 1
        assert eur_transactions[0]["id"] == 2
        assert eur_transactions[0]["operationAmount"]["currency"]["code"] == "EUR"

    def test_filter_rub_transactions(self, sample_transactions):
        """Тест фильтрации RUB транзакций."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))

        assert len(rub_transactions) == 1
        assert rub_transactions[0]["id"] == 4
        assert rub_transactions[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_basic_descriptions_extraction():
    """Основной тест извлечения описаний."""
    transactions = [
        {"id": 1, "description": "Перевод организации", "amount": "100"},
        {"id": 2, "description": "Оплата услуг", "amount": "200"},
        {"id": 3, "description": "Пополнение счета", "amount": "300"}
    ]

    result = list(transaction_descriptions(transactions))
    expected = ["Перевод организации", "Оплата услуг", "Пополнение счета"]

    assert result == expected


def test_empty_transactions_list():
    """Тест пустого списка транзакций."""
    result = list(transaction_descriptions([]))
    assert result == []


def test_generator_behavior():
    """Тест поведения генератора."""
    transactions = [
        {"description": "Первая операция"},
        {"description": "Вторая операция"},
        {"description": "Третья операция"}
    ]

    gen = transaction_descriptions(transactions)

    assert next(gen) == "Первая операция"
    assert next(gen) == "Вторая операция"
    assert next(gen) == "Третья операция"


class TestCardNumberGenerator:

    def test_basic_range_generation(self):
        """Тест генерации базового диапазона номеров карт."""
        result = list(card_number_generator(1, 5))

        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005"
        ]

        assert result == expected
        assert len(result) == 5

    def test_correct_formatting(self):
        """Тест корректности форматирования номеров карт."""
        result = list(card_number_generator(1234567890123456, 1234567890123456))

        assert result == ["1234 5678 9012 3456"]
        assert len(result[0]) == 19  # 16 цифр + 3 пробела

    def test_edge_cases(self):
        """Тест крайних значений диапазона."""
        # Минимальное значение
        min_result = list(card_number_generator(1, 1))
        assert min_result == ["0000 0000 0000 0001"]

        # Максимальное значение
        max_result = list(card_number_generator(9999999999999999, 9999999999999999))
        assert max_result == ["9999 9999 9999 9999"]
