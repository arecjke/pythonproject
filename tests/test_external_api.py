import os
import unittest
from unittest.mock import MagicMock, patch

import requests

from src.external_api import converter_currency


class TestConverterCurrency(unittest.TestCase):

    def setUp(self):
        """Очищаем переменные окружения перед каждым тестом."""
        if "API_KEY" in os.environ:
            del os.environ["API_KEY"]

    @patch("os.getenv", return_value="test_api_key")
    @patch("requests.request")
    def test_valid_conversion_usd_to_rub(self, mock_request, mock_getenv):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 95.4321}
        mock_request.return_value = mock_response

        result = converter_currency(100, "USD")

        self.assertEqual(result, 95.43)

    @patch("os.getenv", return_value="test_api_key")
    @patch("requests.request")
    def test_valid_conversion_eur_to_rub(self, mock_request, mock_getenv):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 102.999}
        mock_request.return_value = mock_response

        result = converter_currency(50, "EUR")
        self.assertEqual(result, 103.00)

    def test_invalid_transaction_type_string(self):
        result = converter_currency("not_a_number", "USD")
        self.assertIsNone(result)

    def test_invalid_transaction_type_none(self):
        result = converter_currency(None, "USD")
        self.assertIsNone(result)

    def test_transaction_cannot_convert_to_float(self):
        result = converter_currency([], "USD")
        self.assertIsNone(result)

    def test_unsupported_currency(self):
        result = converter_currency(100, "GBP")
        self.assertIsNone(result)

    def test_empty_currency_string(self):
        result = converter_currency(100, "")
        self.assertIsNone(result)

    @patch("os.getenv", return_value=None)
    def test_api_key_not_found(self, mock_getenv):
        result = converter_currency(100, "USD")
        self.assertIsNone(result)
        mock_getenv.assert_called_with("API_KEY")

    @patch("os.getenv", return_value="test_api_key")
    @patch("requests.request")
    @patch("builtins.print")
    def test_http_404_error(self, mock_print, mock_request, mock_getenv):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_request.return_value = mock_response

        result = converter_currency(100, "USD")

        self.assertIsNone(result)
        mock_print.assert_any_call("Ошибка запроса: 404")
        mock_print.assert_any_call("Ответ сервера: Not Found")

    @patch("os.getenv", return_value="test_api_key")
    @patch("requests.request")
    def test_http_500_error(self, mock_request, mock_getenv):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_request.return_value = mock_response

        result = converter_currency(100, "USD")
        self.assertIsNone(result)

    @patch("os.getenv", return_value="test_api_key")
    @patch("requests.request")
    def test_missing_result_in_response(self, mock_request, mock_getenv):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"error": "no result"}
        mock_request.return_value = mock_response

        result = converter_currency(100, "USD")
        self.assertIsNone(result)

    @patch("os.getenv", return_value="test_api_key")
    @patch("requests.request", side_effect=requests.exceptions.Timeout("Timeout"))
    def test_request_timeout(self, mock_request, mock_getenv):
        result = converter_currency(100, "USD")
        self.assertIsNone(result)

    @patch("os.getenv", return_value="test_api_key")
    @patch("requests.request", side_effect=requests.exceptions.ConnectionError("No connection"))
    def test_connection_error(self, mock_request, mock_getenv):
        result = converter_currency(100, "USD")
        self.assertIsNone(result)

    @patch("os.getenv", return_value="test_api_key")
    @patch("requests.request")
    def test_result_rounded_to_2_decimals(self, mock_request, mock_getenv):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 99.999}
        mock_request.return_value = mock_response

        result = converter_currency(10, "USD")
        self.assertEqual(result, 100.00)

    @patch("os.getenv", return_value="test_api_key")
    @patch("requests.request")
    def test_large_amount_conversion(self, mock_request, mock_getenv):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 12345678.901}
        mock_request.return_value = mock_response

        result = converter_currency(100000, "USD")
        self.assertEqual(result, 12345678.90)

        @patch("os.getenv", return_value="test_api_key")
        @patch("requests.request")
        def test_api_returns_float_with_many_decimals(self, mock_request, mock_getenv):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"result": 0.123456789}
            mock_request.return_value = mock_response

            result = converter_currency(1, "USD")
            self.assertEqual(result, 0.12)

        @patch("os.getenv", return_value="test_api_key")
        @patch("requests.request")
        def test_api_response_contains_extra_fields(self, mock_request, mock_getenv):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"result": 50.50, "timestamp": "2025-01-01", "rate": 75.0}
            mock_request.return_value = mock_response

            result = converter_currency(1, "USD")
            self.assertEqual(result, 50.50)

        @patch("os.getenv", return_value="test_api_key")
        @patch("requests.request")
        def test_api_returns_zero_result(self, mock_request, mock_getenv):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"result": 0}
            mock_request.return_value = mock_response

            result = converter_currency(100, "USD")
            self.assertEqual(result, 0.00)

        @patch("os.getenv", return_value="test_api_key")
        @patch("requests.request")
        def test_url_construction(self, mock_request, mock_getenv):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"result": 100}
            mock_request.return_value = mock_response

            converter_currency(50, "EUR")

            called_url = mock_request.call_args[0][1]
            self.assertIn("to=RUB", called_url)
            self.assertIn("from=EUR", called_url)
            self.assertIn("amount=50", called_url)

        def test_currency_case_insensitive(self):
            with patch("os.getenv", return_value="test_api_key"):
                with patch("requests.request") as mock_request:
                    mock_response = MagicMock()
                    mock_response.status_code = 200
                    mock_response.json.return_value = {"result": 75.25}
                    mock_request.return_value = mock_response

                    result = converter_currency(1, "usd")  # нижний регистр

            self.assertEqual(result, 75.25)
            called_url = mock_request.call_args[0][1]
            self.assertIn("from=USD", called_url)

        @patch("os.getenv", return_value="test_api_key")
        @patch("requests.request")
        def test_invalid_json_response(self, mock_request, mock_getenv):
            mock_response = MagicMock()
            mock_response.status_code = 200
            # Имитируем ошибку декодирования JSON
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_request.return_value = mock_response

            result = converter_currency(100, "USD")
            self.assertIsNone(result)

        @patch("os.getenv", return_value="test_api_key")
        @patch("requests.request")
        def test_empty_json_response(self, mock_request, mock_getenv):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_request.return_value = mock_response

            result = converter_currency(100, "USD")
            self.assertIsNone(result)

        @patch("os.getenv", return_value="test_api_key")
        @patch("requests.request")
        def test_non_numeric_result_in_response(self, mock_request, mock_getenv):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"result": "not_a_number"}
            mock_request.return_value = mock_response

            result = converter_currency(100, "USD")
            self.assertIsNone(result)

    if __name__ == "__main__":
        unittest.main()
