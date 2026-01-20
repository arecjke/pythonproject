import logging
from typing import Optional

from logger_config import setup_logger

# Инициализируем логгер для модуля masks
logger = setup_logger("masks")


def get_mask_card_number(card_number: str) -> str:

    try:
        logger.info(f"Начало маскировки номера карты: {card_number}")

        # Удаляем пробелы из номера карты
        original_number = card_number
        card_number = card_number.replace(" ", "")

        logger.debug(f"Номер карты после удаления пробелов: {card_number}")

        # Проверяем длину номера карты
        if len(card_number) != 16:
            error_msg = f"Неверная длина номера карты: {len(card_number)} символов вместо 16"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Проверяем, что номер содержит только цифры
        if not card_number.isdigit():
            error_msg = "Номер карты должен содержать только цифры"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Форматируем номер карты с маскировкой
        visible_part = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

        logger.info(f"Успешная маскировка номера карты. Исходный: {original_number}, Замаскированный: {visible_part}")

        return visible_part

    except Exception as e:
        logger.exception(f"Ошибка при маскировке номера карты: {e}")
        raise


def get_mask_account(account_number: str) -> str:

    try:
        logger.info(f"Начало маскировки номера счета: {account_number}")

        # Удаляем пробелы из номера счета
        original_number = account_number
        account_number = account_number.replace(" ", "")

        logger.debug(f"Номер счета после удаления пробелов: {account_number}")

        # Проверяем минимальную длину номера счета
        if len(account_number) < 4:
            error_msg = f"Номер счета слишком короткий: {len(account_number)} символов"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Проверяем, что номер содержит только цифры
        if not account_number.isdigit():
            error_msg = "Номер счета должен содержать только цифры"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Форматируем номер счета с маскировкой
        masked_account = "**" + account_number[-4:]

        logger.info(
            f"Успешная маскировка номера счета. Исходный: {original_number}, Замаскированный: {masked_account}"
        )

        return masked_account

    except Exception as e:
        logger.exception(f"Ошибка при маскировке номера счета: {e}")
        raise


result = "565428972873"

if __name__ == "__main__":
    print(get_mask_card_number("4444555566667777"))
    print(get_mask_account("47567654675434534"))
    print(get_mask_account(result))
    print(get_mask_card_number(result))
