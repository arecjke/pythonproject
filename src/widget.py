def mask_account_card(data: str) -> str:
    """
    Маскирует номер карты или счета в переданной строке.

    Args:
        data: Строка с информацией о карте или счете (например: "Visa Platinum 7000792289606361")

    Returns:
        Строка с замаскированным номером карты или счета
    """
    if not data or not isinstance(data, str):
        return data if data is not None else ""

    # Сохраняем оригинальные пробелы
    stripped_data = data.strip()
    if not stripped_data:
        return data

    # Разделяем строку на части
    parts = stripped_data.split()

    if len(parts) < 2:
        return data

    # Последняя часть - это номер
    number_part = parts[-1]

    # Проверяем, является ли последняя часть номером (только цифры)
    if not number_part.isdigit():
        return data

    # Название карты/счета - все части кроме последней
    account_type = " ".join(parts[:-1])

    # Определяем тип (карта или счет)
    if account_type.lower().startswith("счет"):
        # Маскировка для счета: **последние 4 цифры
        if len(number_part) >= 4:
            masked_number = f"**{number_part[-4:]}"
        else:
            masked_number = number_part
    else:
        # Маскировка для карты: XXXX XX** **** XXXX
        if len(number_part) == 16:
            masked_number = f"{number_part[:4]} {number_part[4:6]}** **** {number_part[-4:]}"
        else:
            masked_number = number_part

    # Восстанавливаем пробелы
    leading_spaces = data[: len(data) - len(data.lstrip())]
    trailing_spaces = data[len(data.rstrip()):]

    result = f"{account_type} {masked_number}"
    return f"{leading_spaces}{result}{trailing_spaces}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO 8601 в формат ДД.ММ.ГГГГ.

    Args:
        date_string: Строка с датой в формате 2024-03-11T02:26:18.671407

    Returns:
        Строка с датой в формате ДД.ММ.ГГГГ
    """
    if not date_string or not isinstance(date_string, str):
        return date_string if date_string is not None else ""

    # Сохраняем пробелы
    stripped_date = date_string.strip()
    if not stripped_date:
        return date_string

    try:
        # Разделяем строку по 'T' и берем первую часть (дату)
        if "T" in stripped_date:
            date_part = stripped_date.split("T")[0]
        elif " " in stripped_date:
            date_part = stripped_date.split()[0]
        else:
            date_part = stripped_date

        # Разделяем дату на компоненты
        date_components = date_part.split("-")

        # Проверяем, что есть как минимум 3 компонента (год, месяц, день)
        if len(date_components) >= 3:
            year, month, day = date_components[:3]

            # Проверяем корректность формата компонентов
            if (
                len(year) == 4
                and year.isdigit()
                and len(month) == 2
                and month.isdigit()
                and len(day) == 2
                and day.isdigit()
            ):

                # Проверяем валидность диапазонов
                month_int = int(month)
                day_int = int(day)
                year_int = int(year)

                # Проверяем корректность месяца
                if not (1 <= month_int <= 12):
                    return date_string

                # Проверяем корректность дня
                days_in_month = {
                    1: 31,
                    2: 29 if (year_int % 4 == 0 and year_int % 100 != 0) or (year_int % 400 == 0) else 28,
                    3: 31,
                    4: 30,
                    5: 31,
                    6: 30,
                    7: 31,
                    8: 31,
                    9: 30,
                    10: 31,
                    11: 30,
                    12: 31,
                }

                if not (1 <= day_int <= days_in_month[month_int]):
                    return date_string

                # Все проверки пройдены, форматируем дату
                formatted_date = f"{day}.{month}.{year}"

                # Восстанавливаем пробелы
                leading_spaces = date_string[: len(date_string) - len(date_string.lstrip())]
                trailing_spaces = date_string[len(date_string.rstrip()):]

                return f"{leading_spaces}{formatted_date}{trailing_spaces}"

        return date_string

    except (IndexError, ValueError, AttributeError, KeyError):
        return date_string


print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Счет 73654108430135874305"))
print(get_date("2020-03-11T02:26:18.671407"))
