import pytest
from datetime import datetime
from src.widget import mask_account_card, get_date

# тесты для функции mask_account_card

def test_mask_card_16_digits_standard_format():
    data = "Visa Platinum 7000792289606361"
    assert mask_account_card(data) == "Visa Platinum 7000 79** **** 6361"

def test_mask_account_with_non_card_prefix():
    data = "Счет оплаты 123456789012"
    assert mask_account_card(data) == "Счет оплаты **9012"  # последние 4 цифры

def test_mask_account_with_short_number():
    data = "Счет 123"
    # недостаточно цифр для маскировки, возвращаем оригинал
    assert mask_account_card(data) == "Счет 123"

def test_mask_card_with_non_digit_last_part():
    data = "Visa Platinum 70007922896063A"
    # последняя часть не является числом -> возвращаем исходную строку
    assert mask_account_card(data) == data

def test_mask_card_with_different_number_lengths():
    # 12 цифр карты
    data = "MasterCard 123456789012"
    # для не-16-цифр маска не применяется, возвращаем оригинал
    assert mask_account_card(data) == data

def test_empty_and_none_inputs():
    assert mask_account_card("") == ""
    assert mask_account_card("   ") == "   "  # пробелы остаются как есть

def test_mask_card_with_leading_zeros():
    data = "Card 0000000000000000"
    assert mask_account_card(data) == "Card 0000 00** **** 0000"

def test_mask_preserves_spaces_only():
    data = "   "
    assert mask_account_card(data) == "   "

def test_mask_no_digits_present():
    data = "No card number here"
    assert mask_account_card(data) == "No card number here"

def test_mask_reduces_when_some_digits_present_but_insufficient():
    data = "Code 123"
    assert mask_account_card(data) == "Code 123"  # недостаточно цифр для маски

def test_mask_keeps_prefix_when_digits_at_end():
    data = "ABC-DEF-1234"
    assert mask_account_card(data) == "ABC-DEF-1234"


# Тесты для функции get_date

def test_correct_iso_date_transforms_to_dmy():
    # корректная дата в формате 2024-03-11T02:26:18.671407 -> 11.03.2024
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"

def test_correct_date_with_additional_time_fraction():
    # ещё один пример корректной даты
    assert get_date("1999-12-01T23:45:00.123456") == "01.12.1999"

def test_missing_time_part_still_ok():
    # если нет времени после T, но есть валидная дата до T
    assert get_date("2020-01-05") == "05.01.2020"

def test_incorrect_separator_returns_original():
    # неверный разделитель (используется / вместо -)
    original = "2024/03/11T02:26:18"
    assert get_date(original) == original

def test_incomplete_components_returns_original():
    # неполные компоненты даты
    original = "2024-3-11T02:26:18"
    assert get_date(original) == original

def test_extra_components_after_time_are_ignored():
    # любые символы после времени не важны, функция обрезает до T
    original = "2024-03-11T02:26:18.671407Z"
    assert get_date(original) == "11.03.2024"

def test_empty_string_returns_original():
    assert get_date("") == ""

def test_non_date_string_returns_original():
    assert get_date("not-a-date") == "not-a-date"

def test_only_time_string_returns_original():
    assert get_date("T02:26:18") == "T02:26:18"

def test_no_t_in_string_returns_original():
    # если нет символа T, split("T") даст список размера 1, и будет IndexError
    # функция должна вернуть оригинал
    original = "20240311"
    assert get_date(original) == original