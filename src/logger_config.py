import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(module_name: str) -> logging.Logger:
    """
    Настройка логгера для модуля

    Args:
        module_name: Имя модуля (например, 'masks', 'utils')

    Returns:
        Настроенный объект логгера
    """
    # Создаем директорию для логов, если она не существует
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Создаем имя файла лога
    log_file = log_dir / f"{module_name}.log"

    # Создаем логгер
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Удаляем существующие обработчики, чтобы избежать дублирования
    logger.handlers.clear()

    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Создаем обработчик для записи в файл (режим 'w' для перезаписи)
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger