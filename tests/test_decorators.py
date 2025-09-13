import pytest
import tempfile
import os

from src.decorators import log


class TestLogDecorator:

    def test_log_to_file_success(self):
        """Тест записи успешного выполнения в файл"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            log_file = tmp.name

        try:
            @log(filename=log_file)
            def test_func(x, y):
                return x + y

            result = test_func(2, 3)

            assert result == 5
            assert os.path.exists(log_file)

            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "test_func ok" in content
        finally:
            os.unlink(log_file)

    def test_log_to_file_error(self):
        """Тест записи ошибки в файл"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            log_file = tmp.name

        try:
            @log(filename=log_file)
            def test_func(x, y):
                return x / y

            with pytest.raises(ZeroDivisionError):
                test_func(1, 0)

            assert os.path.exists(log_file)

            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "test_func error: ZeroDivisionError" in content
                assert "Inputs: (1, 0)" in content
        finally:
            os.unlink(log_file)

    def test_log_to_console_success(self, capsys):
        """Тест вывода успешного выполнения в консоль"""

        @log()
        def test_func(x, y):
            return x * y

        result = test_func(3, 4)

        assert result == 12

        captured = capsys.readouterr()
        assert "test_func ok" in captured.out

    def test_log_to_console_error(self, capsys):
        """Тест вывода ошибки в консоль"""

        @log()
        def test_func(x, y):
            return x / y

        with pytest.raises(ZeroDivisionError):
            test_func(5, 0)

        captured = capsys.readouterr()
        assert "test_func error: ZeroDivisionError" in captured.out
        assert "Inputs: (5, 0)" in captured.out

    def test_log_with_kwargs(self, capsys):
        """Тест функции с ключевыми аргументами"""

        @log()
        def test_func(a, b=2):
            return a + b

        result = test_func(10, b=5)

        assert result == 15

        captured = capsys.readouterr()
        assert "test_func ok" in captured.out

    def test_log_with_kwargs_error(self, capsys):
        """Тест ошибки функции с ключевыми аргументами"""

        @log()
        def test_func(a, b=0):
            if b == 0:
                raise ValueError("Division by zero")
            return a / b

        with pytest.raises(ValueError):
            test_func(10, b=0)

        captured = capsys.readouterr()
        assert "test_func error: ValueError" in captured.out
        assert "Inputs: (10), {b=0}" in captured.out