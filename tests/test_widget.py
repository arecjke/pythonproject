import pytest
from datetime import datetime
from src.widget import mask_account_card, get_date

import pytest

# Фикстуры для общих данных
@pytest.fixture
def valid_card_numbers():
    return ["7000792289606361", "7158300734726758", "1596837868705199"]


@pytest.fixture
def valid_account_numbers():
    return ["64686473678894779589", "35383033474447895560", "73654108430135874305"]


@pytest.fixture
def invalid_numbers():
    return ["70007922896063A", "123456789012", "700079228960636"]


# Параметризованные тесты для mask_account_card
class TestMaskAccountCard:

    @pytest.mark.parametrize("card_type", ["Visa Platinum", "MasterCard", "Maestro"])
    def test_valid_cards(self, card_type, valid_card_numbers):
        for number in valid_card_numbers:
            input_data = f"{card_type} {number}"
            expected = f"{card_type} {number[:4]} {number[4:6]}** **** {number[-4:]}"
            assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize("account_prefix", ["Счет", "счет", "СЧЕТ"])
    def test_valid_accounts(self, account_prefix, valid_account_numbers):
        for number in valid_account_numbers:
            input_data = f"{account_prefix} {number}"
            expected = f"{account_prefix} **{number[-4:]}"
            assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize("invalid_data", [
        "Счет 123", "", "   ", "No card number here", "Code 123"
    ])
    def test_edge_cases_returns_original(self, invalid_data):
        assert mask_account_card(invalid_data) == invalid_data

    def test_invalid_cards_returns_original(self, invalid_numbers):
        for number in invalid_numbers:
            input_data = f"Visa Platinum {number}"
            assert mask_account_card(input_data) == input_data

    @pytest.mark.parametrize("input_data, expected", [
        ("  Visa Platinum  7000792289606361  ", "  Visa Platinum 7000 79** **** 6361  "),
        ("  Счет  73654108430135874305  ", "  Счет **4305  "),
    ])
    def test_preserves_whitespace(self, input_data, expected):
        assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize("case_insensitive_input, expected", [
        ("сЧет 73654108430135874305", "сЧет **4305"),
        ("СЧЕТ 73654108430135874305", "СЧЕТ **4305"),
    ])
    def test_case_insensitive(self, case_insensitive_input, expected):
        assert mask_account_card(case_insensitive_input) == expected


# Параметризованные тесты для get_date
class TestGetDate:

    @pytest.mark.parametrize("input_date, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("1999-12-01T23:45:00.123456", "01.12.1999"),
        ("2020-01-05T00:00:00.000000", "05.01.2020"),
        ("2024-02-29T12:00:00.000000", "29.02.2024"),
        ("2023-01-31T12:00:00.000000", "31.01.2023"),
        ("2024-03-11", "11.03.2024"),
    ])
    def test_valid_dates(self, input_date, expected):
        assert get_date(input_date) == expected

    @pytest.mark.parametrize("invalid_date", [
        "2024/03/11T02:26:18",
        "2024-3-11T02:26:18",
        "20240311",
        "not-a-date",
        "T02:26:18",
        "2024-13-01T12:00:00",  # несуществующий месяц
        "2024-02-30T12:00:00",  # несуществующий день
        "",
        "   ",
    ])
    def test_invalid_dates_returns_original(self, invalid_date):
        assert get_date(invalid_date) == invalid_date

    @pytest.mark.parametrize("input_date, expected", [
        ("2024-03-11T02:26:18.671407Z", "11.03.2024"),
        ("2024-03-11T02:26:18.671407+03:00", "11.03.2024"),
    ])
    def test_ignores_extra_characters(self, input_date, expected):
        assert get_date(input_date) == expected

    @pytest.mark.parametrize("input_with_whitespace, expected", [
        ("  2024-03-11T02:26:18.671407  ", "  11.03.2024  "),
        ("  1999-12-01  ", "  01.12.1999  "),
    ])
    def test_preserves_whitespace(self, input_with_whitespace, expected):
        assert get_date(input_with_whitespace) == expected

    @pytest.mark.parametrize("year, month, day, expected", [
        (2023, 2, 28, "28.02.2023"),  # невисокосный год
        (2024, 2, 29, "29.02.2024"),  # високосный год
        (2024, 4, 30, "30.04.2024"),  # 30 дней
        (2024, 4, 31, "2024-04-31T12:00:00"),  # некорректный день
    ])
    def test_month_day_validation(self, year, month, day, expected):
        """Тест валидации дней в месяцах"""
        month_str = str(month).zfill(2)
        day_str = str(day).zfill(2)
        input_date = f"{year}-{month_str}-{day_str}T12:00:00"
        assert get_date(input_date) == expected


# Интеграционные тесты
class TestIntegration:

    @pytest.mark.parametrize("input_data, expected", [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ])
    def test_real_world_examples(self, input_data, expected):
        assert mask_account_card(input_data) == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])