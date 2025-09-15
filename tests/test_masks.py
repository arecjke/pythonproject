from src.masks import get_mask_card_number, get_mask_account

def test_correct_mask_card_number():

        """Тест стандартной маскировки номера карты"""
        # Стандартный 16-значный номер
        assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"
        assert get_mask_card_number("1111222233334444") == "1111 22** **** 4444"

        # Номер с пробелами
        assert get_mask_card_number("1234 5678 1234 5678") == "1234 56** **** 5678"
        assert get_mask_card_number("1111 2222 3333 4444") == "1111 22** **** 4444"

def test_diff_card_lenght():
        """Тест различных длин номеров карт"""
        # 19-значный номер (некоторые карты)
        assert get_mask_card_number("1234567890123456789") == "1234 56** **** 6789"

        # 13-значный номер (старые Visa)
        assert get_mask_card_number("1234567890123") == "1234 56** **** 0123"

        # 15-значный номер (American Express)
        assert get_mask_card_number("123456789012345") == "1234 56** **** 2345"


def test_edge_cases_card():
        """Тест граничных случаев для карты"""
        # Минимальная длина для маскировки (10 цифр)
        assert get_mask_card_number("1234567890") == "1234 56** **** 7890"

        # Номер с множеством пробелов
        assert get_mask_card_number("1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6") == "1234 56** **** 3456"

        # Номер с разными разделителями (только пробелы удаляются)
        #assert get_mask_card_number("1234-5678-1234-5678") == "1234-56**-****-5678"


def test_short_card_numbers():
        """Тест коротких номеров карт"""
        # Слишком короткий номер (менее 10 цифр)
        assert get_mask_card_number("123456789") == "1234 56** **** 6789"  # 9 цифр
        assert get_mask_card_number("12345678") == "1234 56** **** 5678"  # 8 цифр

        # Очень короткий номер (менее 6 цифр)
        assert get_mask_card_number("12345") == "1234 5** **** 2345"  # 5 цифр
        assert get_mask_card_number("123") == "123 ** **** 123"  # 3 цифры


def test_empty_and_invalid_input_card():
        """Тест пустых и невалидных входных данных для карты"""
        # Пустая строка
        assert get_mask_card_number("") == " ** **** "

        # Только пробелы
        assert get_mask_card_number("   ") == " ** **** "

        # Остальные тесты остаются без изменений
        assert get_mask_card_number("ABCD EFGH IJKL MNOP") == "ABCD EF** **** MNOP"
        assert get_mask_card_number("1234 ABCD 5678 EFGH") == "1234 AB** **** EFGH"


def test_standard_account_masking():
        """Тест стандартной маскировки номера счета"""
        # Стандартный номер счета (20 цифр)
        assert get_mask_account("12345678901234567890") == "**7890"
        assert get_mask_account("11112222333344445555") == "**5555"

        # Номер с пробелами
        assert get_mask_account("1234 5678 9012 3456 7890") == "**7890"
        assert get_mask_account("1111 2222 3333 4444 5555") == "**5555"


def test_different_account_lengths():
        """Тест различных длин номеров счетов"""
        # Длинный номер счета
        assert get_mask_account("123456789012345678901234567890") == "**7890"

        # Короткий номер счета (но больше 4 цифр)
        assert get_mask_account("12345678") == "**5678"
        assert get_mask_account("12345") == "**2345"


def test_edge_cases_account():
        """Тест граничных случаев для номера счета"""
        # Точно 4 цифры
        assert get_mask_account("1234") == "**1234"

        # Менее 4 цифр
        assert get_mask_account("123") == "**123"
        assert get_mask_account("12") == "**12"
        assert get_mask_account("1") == "**1"

        # Номер с разными разделителями
        assert get_mask_account("1234-5678-9012-3456") == "**3456"


def test_empty_and_invalid_input_account():
        """Тест пустых и невалидных входных данных для счета"""
        # Пустая строка
        assert get_mask_account("") == "**"

        # Только пробелы
        assert get_mask_account("   ") == "**"

        # Не цифровые символы
        assert get_mask_account("ABCDEFGHIJ") == "**GHIJ"
        assert get_mask_account("ABC123DEF456") == "**F456"

        # Смесь цифр и букв
        assert get_mask_account("1234 ABCD 5678 EFGH") == "**EFGH"


def test_very_short_input_account():
        """Тест очень коротких входных данных для счета"""
        # Очень короткие строки
        assert get_mask_account("123") == "**123"
        assert get_mask_account("12") == "**12"
        assert get_mask_account("1") == "**1"
        assert get_mask_account("A") == "**A"

        # Пустая строка
        assert get_mask_account("") == "**"


def test_card_number_format():
        """Проверка, что результат имеет правильный формат"""
        result = get_mask_card_number("1234567812345678")
        parts = result.split()
        assert len(parts) == 4
        assert parts[0] == "1234"
        assert parts[1] == "56**"
        assert parts[2] == "****"
        assert parts[3] == "5678"

def test_account_format():
    """Проверка, что результат для счета начинается с **"""
    result = get_mask_account("12345678901234567890")
    assert result.startswith("**")
    assert len(result) == 6  # ** + 4 цифры
