import datetime
from functools import wraps


def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                success_message = f"{func.__name__} ok\n"

                # Записываем или выводим лог
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(success_message)
                else:
                    print(success_message, end='')

                return result

            except Exception as e:
                # Информация о входных параметрах
                args_str = ', '.join(repr(arg) for arg in args)
                kwargs_str = ', '.join(f'{k}={repr(v)}' for k, v in kwargs.items())
                inputs_info = f"({args_str})"
                if kwargs_str:
                    inputs_info += f", {{{kwargs_str}}}"

                # Сообщение об ошибке
                error_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {inputs_info}\n"

                # Записываем или выводим лог
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(error_message)
                else:
                    print(error_message, end='')

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


# Тестируем
my_function(1, 2)  # Запишет "my_function ok" в mylog.txt