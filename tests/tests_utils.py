import unittest
from unittest.mock import patch, mock_open
import os
import json
from src.utils import load_transactions  # предполагаемый путь



class TestLoadTransactions(unittest.TestCase):

    @patch('os.path.dirname')
    @patch('os.path.abspath')
    def test_default_path_construction(self, mock_abspath, mock_dirname):
        """Проверяет формирование пути по умолчанию."""
        mock_abspath.return_value = '/project/src/utils.py'
        mock_dirname.side_effect = [
            '/project/src',  # os.path.dirname('/project/src/utils.py')
            '/project',       # os.path.dirname('/project/src')
        ]

        with patch('builtins.open', mock_open(read_data='[]')) as mock_file:
            with patch('json.load', return_value=[]):
                result = load_transactions()


        expected_path = os.path.join('/project', 'data', 'operations.json')
        mock_file.assert_called_with(expected_path, 'r', encoding='utf-8')
        self.assertEqual(result, [])

    def test_explicit_file_path(self):
        """Проверяет передачу явного пути к файлу."""
        test_data = [{'id': 1, 'amount': 100}]
        with patch('builtins.open', mock_open(read_data=json.dumps(test_data))) as mock_file:
            with patch('json.load', return_value=test_data):
                result = load_transactions('/custom/path/ops.json')

        mock_file.assert_called_with('/custom/path/ops.json', 'r', encoding='utf-8')
        self.assertEqual(result, test_data)

    def test_valid_json_list(self):
        """Проверяет загрузку корректного JSON-списка."""
        test_data = [{'txn_id': 'A1', 'sum': 500}, {'txn_id': 'B2', 'sum': 300}]
        with patch('builtins.open', mock_open(read_data=json.dumps(test_data))):
            result = load_transactions('dummy.json')
        self.assertEqual(result, test_data)

    def test_json_not_a_list(self):
        """Проверяет случай, когда JSON — не список (например, словарь)."""
        test_data = {'total': 1000, 'count': 2}
        with patch('builtins.open', mock_open(read_data=json.dumps(test_data))):
            result = load_transactions('dummy.json')
        self.assertEqual(result, [])  # ожидаем пустой список


    def test_empty_json_file(self):
        """Проверяет пустой файл (корректный JSON, но пустой)."""
        with patch('builtins.open', mock_open(read_data='')):
            result = load_transactions('dummy.json')
        self.assertEqual(result, [])

    def test_invalid_json_syntax(self):
        """Проверяет ошибку парсинга JSON (невалидный синтаксис)."""
        with patch('builtins.open', mock_open(read_data='{invalid json}')):
            result = load_transactions('dummy.json')
        self.assertEqual(result, [])


    @patch('builtins.open', side_effect=FileNotFoundError('Not found'))
    def test_file_not_found(self, mock_open):
        """Проверяет обработку отсутствия файла."""
        result = load_transactions('nonexistent.json')
        self.assertEqual(result, [])


    @patch('builtins.open', side_effect=PermissionError('Access denied'))
    def test_permission_error(self, mock_open):
        """Проверяет обработку ошибки прав доступа."""
        result = load_transactions('restricted.json')
        self.assertEqual(result, [])

    @patch('builtins.open', side_effect=OSError('Disk error'))
    def test_os_error(self, mock_open):
        """Проверяет обработку общей OSError."""
        result = load_transactions('broken.json')
        self.assertEqual(result, [])

    def test_large_valid_json(self):
        """Проверяет загрузку большого корректного JSON-списка."""
        test_data = [{'id': i, 'amount': i * 10} for i in range(1000)]
        with patch('builtins.open', mock_open(read_data=json.dumps(test_data))):
            result = load_transactions('large.json')
        self.assertEqual(len(result), 1000)
        self.assertEqual(result[0], {'id': 0, 'amount': 0})
        self.assertEqual(result[-1], {'id': 999, 'amount': 9990})



if __name__ == '__main__':
    unittest.main()
