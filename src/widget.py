from masks import get_mask_account, get_mask_card_number


def mask_account_card(number_info: str) -> str:
    """Функция, которая реализует маскировку номера карты или счета"""
    number_list = number_info.split()
    if not isinstance(number_info, str):
        return "неккоректные данные"

    if "Счет" in number_info:
        return f"{number_list[0]} {get_mask_account(number_list[-1])}"
    else:
        return f"{' '.join(number_list[:-1])} {get_mask_card_number(number_list[-1])}"


def get_date(date_string: str) -> str:
    """Функция, которая принимает на вход строку с датой в формате
    2024-03-11T02:26:18.671407 и возвращает строку с датой в формате
    ДД.ММ.ГГГГ"""
    date_part = date_string.split("T")[0]
    year, month, day = date_part.split("-")

    return f"{day}.{month}.{year}"


print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Счет 73654108430135874305"))
