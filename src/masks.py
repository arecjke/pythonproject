result = "565428972873"


def get_mask_card_number(card_number: str) -> str:
    """Функция, которая реализует маскировку номера карты таким образом,
     чтобы были видно первые 6 цифр
    и последние 4 цифры. номер будет разбит на 4 цифры,
    разделенные пробелами"""
    card_number = card_number.replace(" ", "")

    visible_part = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

    return visible_part


def get_mask_account(account_number: str) -> str:
    """Функция, которая реализует маскировку номера счета.
    Ввод номера карты, вывод **XXXX"""
    account_number = account_number.replace(" ", "")

    masked_account = "**" + account_number[-4:]

    return masked_account


if __name__ == "__main__":
    print(get_mask_card_number("4444555566667777"))
    print(get_mask_account("475676546754345345"))
    print(get_mask_account(result))
    print(get_mask_card_number(result))
