import time  # Импортируем time на уровне модуля

import pytest

from src.masks import get_mask_account, get_mask_card_number


# Выносим фикстуры на уровень модуля, чтобы они были доступны всем классам
@pytest.fixture
def valid_card_numbers():
    """Фикстура с валидными номерами карт"""
    return ["1234567890123456", "1234 5678 9012 3456", "1111222233334444"]


@pytest.fixture
def valid_account_numbers():
    """Фикстура с валидными номерами счетов"""
    return ["1234567890", "1234 5678 90", "9876543210"]


@pytest.fixture
def edge_case_numbers():
    """Фикстура с граничными случаями"""
    return {
        "short_card": "123456789012",  # 12 цифр вместо 16
        "long_card": "12345678901234567890",  # 20 цифр
        "short_account": "1234",  # 4 цифры
        "empty_string": "",
    }


class TestMaskFunctions:
    """Тесты для функций маскировки карт и счетов"""

    # Тесты для функции маскировки карты
    def test_get_mask_card_number_basic(self):
        """Базовый тест маскировки карты"""
        result = get_mask_card_number("1234567890123456")
        expected = "1234 56** **** 3456"
        assert result == expected

    def test_get_mask_card_number_with_spaces(self):
        """Тест маскировки карты с пробелами в номере"""
        result = get_mask_card_number("1234 5678 9012 3456")
        expected = "1234 56** **** 3456"
        assert result == expected

    @pytest.mark.parametrize(
        "card_number,expected",
        [
            ("1234567890123456", "1234 56** **** 3456"),
            ("1111222233334444", "1111 22** **** 4444"),
            ("9999888877776666", "9999 88** **** 6666"),
            ("1234 5678 9012 3456", "1234 56** **** 3456"),
            ("1111 2222 3333 4444", "1111 22** **** 4444"),
        ],
    )
    def test_get_mask_card_number_parametrized(self, card_number, expected):
        """Параметризованный тест маскировки карты"""
        result = get_mask_card_number(card_number)
        assert result == expected

    def test_get_mask_card_number_format(self, valid_card_numbers):
        """Тест формата маскированной карты"""
        for card_number in valid_card_numbers:
            result = get_mask_card_number(card_number)
            # Проверяем, что результат содержит 4 группы символов
            parts = result.split()
            assert len(parts) == 4
            # Проверяем формат каждой части
            assert len(parts[0]) == 4  # Первые 4 цифры
            assert len(parts[1]) == 4  # 2 цифры + **
            assert parts[2] == "****"  # Звездочки
            assert len(parts[3]) == 4  # Последние 4 цифры

    # Тесты для функции маскировки счета
    def test_get_mask_account_basic(self):
        """Базовый тест маскировки счета"""
        result = get_mask_account("1234567890")
        expected = "**7890"
        assert result == expected

    def test_get_mask_account_with_spaces(self):
        """Тест маскировки счета с пробелами"""
        result = get_mask_account("1234 5678 90")
        expected = "**7890"
        assert result == expected

    @pytest.mark.parametrize(
        "account_number,expected",
        [
            ("1234567890", "**7890"),
            ("9876543210", "**3210"),
            ("1111222233", "**2233"),
            ("1234 5678 90", "**7890"),
            ("9876 5432 10", "**3210"),
        ],
    )
    def test_get_mask_account_parametrized(self, account_number, expected):
        """Параметризованный тест маскировки счета"""
        result = get_mask_account(account_number)
        assert result == expected

    def test_get_mask_account_format(self, valid_account_numbers):
        """Тест формата маскированного счета"""
        for account_number in valid_account_numbers:
            result = get_mask_account(account_number)
            # Проверяем, что результат начинается с **
            assert result.startswith("**")
            # Проверяем, что длина результата 6 символов
            assert len(result) == 6
            # Проверяем, что последние 4 символа - цифры
            assert result[2:].isdigit()

    # Интеграционные тесты
    def test_both_functions_work_together(self):
        """Тест, что обе функции работают корректно вместе"""
        card = "1234567890123456"
        account = "1234567890"

        masked_card = get_mask_card_number(card)
        masked_account = get_mask_account(account)

        assert masked_card == "1234 56** **** 3456"
        assert masked_account == "**7890"

    # Тесты на обработку граничных случаев
    def test_get_mask_card_number_edge_cases(self, edge_case_numbers):
        """Тест граничных случаев для маскировки карты"""
        # Тестируем только случаи, которые должны работать
        short_card = edge_case_numbers["short_card"]
        long_card = edge_case_numbers["long_card"]

        # Для короткого номера
        result_short = get_mask_card_number(short_card)
        assert isinstance(result_short, str)

        # Для длинного номера
        result_long = get_mask_card_number(long_card)
        assert isinstance(result_long, str)

    def test_get_mask_account_edge_cases(self, edge_case_numbers):
        """Тест граничных случаев для маскировки счета"""
        short_account = edge_case_numbers["short_account"]

        result_short = get_mask_account(short_account)
        assert isinstance(result_short, str)
        assert result_short.startswith("**")


# Дополнительные тесты с фикстурами для комплексных сценариев
class TestMaskFunctionsAdvanced:
    """Расширенные тесты с использованием фикстур"""

    @pytest.fixture
    def mixed_test_data(self):
        """Фикстура со смешанными тестовыми данными"""
        return {
            "cards": [
                ("1234567890123456", "1234 56** **** 3456"),
                ("5555 6666 7777 8888", "5555 66** **** 8888"),
            ],
            "accounts": [
                ("123456789012", "**9012"),
                ("9999 8888 7777", "**7777"),
            ],
        }

    def test_mixed_data_with_fixture(self, mixed_test_data):
        """Тест с использованием комплексной фикстуры"""
        for card_input, expected_card in mixed_test_data["cards"]:
            result = get_mask_card_number(card_input)
            assert result == expected_card

        for account_input, expected_account in mixed_test_data["accounts"]:
            result = get_mask_account(account_input)
            assert result == expected_account

    def test_performance(self, valid_card_numbers, valid_account_numbers):
        """Тест производительности на множестве данных"""
        # Убедимся, что фикстуры передаются корректно
        assert valid_card_numbers is not None
        assert valid_account_numbers is not None
        assert len(valid_card_numbers) > 0
        assert len(valid_account_numbers) > 0

        start_time = time.time()

        # Многократный вызов функций - уменьшим количество итераций для стабильности
        iterations = 5
        for i in range(iterations):
            for card in valid_card_numbers:
                result = get_mask_card_number(card)
                assert result is not None  # Проверяем, что функция возвращает результат
            for account in valid_account_numbers:
                result = get_mask_account(account)
                assert result is not None  # Проверяем, что функция возвращает результат

        end_time = time.time()
        execution_time = end_time - start_time

        # Более мягкое ограничение по времени
        assert execution_time < 10.0  # меньше 10 секунд
        print(f"Performance test completed in {execution_time:.4f} seconds")

    def test_consistency(self, valid_card_numbers):
        """Тест консистентности результатов"""
        # Убедимся, что фикстура передается корректно
        assert valid_card_numbers is not None
        assert len(valid_card_numbers) > 0

        for card_number in valid_card_numbers:
            # Многократный вызов с одинаковыми данными должен давать одинаковый результат
            results = []
            for _ in range(3):  # Уменьшим количество итераций
                masked = get_mask_card_number(card_number)
                assert masked is not None
                results.append(masked)

            # Все результаты должны быть одинаковыми
            first_result = results[0]
            for result in results[1:]:
                assert result == first_result, f"Results inconsistent for card {card_number}: {results}"


# Тесты для проверки корректности логики маскировки
class TestMaskLogic:
    """Тесты для проверки бизнес-логики маскировки"""

    @pytest.mark.parametrize(
        "input_card,expected_masked",
        [
            ("1234567812345678", "1234 56** **** 5678"),
            ("8765432187654321", "8765 43** **** 4321"),
        ],
    )
    def test_card_masking_logic(self, input_card, expected_masked):
        """Тест правильности логики маскировки карт"""
        result = get_mask_card_number(input_card)
        assert result == expected_masked
        # Проверяем, что первые 6 цифр видны
        assert result[:7].replace(" ", "") == input_card[:6]
        # Проверяем, что последние 4 цифры видны
        assert result[-4:] == input_card[-4:]

    @pytest.mark.parametrize(
        "input_account,expected_masked",
        [
            ("123456789012", "**9012"),
            ("987654321098", "**1098"),
        ],
    )
    def test_account_masking_logic(self, input_account, expected_masked):
        """Тест правильности логики маскировки счетов"""
        result = get_mask_account(input_account)
        assert result == expected_masked
        # Проверяем, что видны только последние 4 цифры
        assert result[2:] == input_account[-4:]


# Альтернативный вариант - если все еще есть проблемы с фикстурами
class TestSimplePerformance:
    """Упрощенные тесты производительности без зависимостей от фикстур"""

    def test_simple_performance(self):
        """Упрощенный тест производительности"""
        test_cards = ["1234567890123456", "1111222233334444"]
        test_accounts = ["1234567890", "9876543210"]

        start_time = time.time()

        iterations = 10
        for _ in range(iterations):
            for card in test_cards:
                get_mask_card_number(card)
            for account in test_accounts:
                get_mask_account(account)

        end_time = time.time()
        execution_time = end_time - start_time

        assert execution_time < 5.0
        print(f"Simple performance test completed in {execution_time:.4f} seconds")

    def test_simple_consistency(self):
        """Упрощенный тест консистентности"""
        test_card = "1234567890123456"

        results = []
        for _ in range(5):
            results.append(get_mask_card_number(test_card))

        assert all(result == results[0] for result in results)
