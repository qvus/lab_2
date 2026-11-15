from email.message import Message
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from triple_scan.binary import find_divisible_binaries
from triple_scan.text_sources import read_text_file, read_url_text


# Проверяет чтение файлов и получение текста с веб-страниц.
class TextSourceTests(unittest.TestCase):
    # Проверяет чтение файла в UTF-8 с меткой порядка байтов.
    def test_utf8_file_with_bom(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "числа.txt"
            path.write_text("Двоичная запись числа 3: 11", encoding="utf-8-sig")
            self.assertEqual(read_text_file(path), "Двоичная запись числа 3: 11")

    # Проверяет извлечение записей из соседних абзацев HTML-файла.
    def test_html_file(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "числа.html"
            path.write_text("<p>11</p><p>110</p>", encoding="utf-8")
            self.assertEqual(
                find_divisible_binaries(read_text_file(path)), ["11", "110"]
            )

    # Проверяет декодирование страницы и поиск двоичных записей в её тексте.
    @patch("triple_scan.text_sources.urlopen")
    def test_html_page(self, urlopen):
        html = (
            '<head><title>111</title></head>'
            '<p data-id="100">Три: <b>1</b>1</p>'
            '<p>&#49;10</p><script>110</script><style>1001</style>'
        )
        response = BytesIO(html.encode("windows-1251"))
        response.headers = Message()
        response.headers["Content-Type"] = "text/html; charset=windows-1251"
        urlopen.return_value = response
        text = read_url_text("https://example.com")
        self.assertIn("Три", text)
        self.assertEqual(find_divisible_binaries(text), ["11", "110"])
        urlopen.assert_called_once_with("https://example.com", timeout=10)

    # Проверяет, что неподдерживаемый URL отклоняется до сетевого запроса.
    @patch("triple_scan.text_sources.urlopen")
    def test_invalid_url_is_rejected_before_request(self, urlopen):
        with self.assertRaises(ValueError):
            read_url_text("file:///tmp/address.txt")
        urlopen.assert_not_called()
