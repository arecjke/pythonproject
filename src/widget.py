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

    # Разделяем строку на части
    parts = data.split()

    if len(parts) < 2:
        return data

    # Последняя часть - это номер
    number_part = parts[-1]

    # Проверяем, является ли последняя часть номером (только цифры)
    if not number_part.isdigit():
        return data

    # Название карты/счета - все части кроме последней
    account_type = ' '.join(parts[:-1])

    # Определяем тип (карта или счет)
    if account_type.lower().startswith('счет'):
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

    return f"{account_type} {masked_number}"


def get_date(date_string: str) -> str:
    """Функция, которая принимает на вход строку с датой в формате
    2024-03-11T02:26:18.671407 и возвращает строку с датой в формате
    ДД.ММ.ГГГГ"""
    try:
        date_part = date_string.split("T")[0]
        year, month, day = date_part.split("-")

        # Проверяем, что все компоненты даты существуют
        if len(year) == 4 and len(month) == 2 and len(day) == 2:
            return f"{day}.{month}.{year}"
        else:
            return date_string
    except (IndexError, ValueError):
        # Возвращаем исходную строку в случае ошибки
        return date_string


print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Счет 73654108430135874305"))
print(get_date("2020-03-11T02:26:18.671407"))
