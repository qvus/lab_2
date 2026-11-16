# Чтение текста из локального файла или с веб-страницы.

from html.parser import HTMLParser
from pathlib import Path
import ssl
from urllib.parse import urlsplit
from urllib.request import urlopen

import certifi

_BLOCK_TAGS = {
    "address", "article", "aside", "blockquote", "br", "dd", "div", "dl",
    "dt", "footer", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr",
    "li", "main", "nav", "ol", "p", "pre", "section", "table", "tbody",
    "td", "tfoot", "th", "thead", "tr", "ul",
}
_HIDDEN_TAGS = {"head", "script", "style", "template"}


# Извлекает текст страницы, пропуская содержимое служебных тегов.
class _PageTextParser(HTMLParser):
    # Создаёт списки для фрагментов текста и открытых служебных тегов.
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.hidden_tags: list[str] = []

    # Запоминает начало служебного тега или добавляет пробел перед текстовым блоком.
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _HIDDEN_TAGS:
            self.hidden_tags.append(tag)
        elif not self.hidden_tags and tag in _BLOCK_TAGS:
            self.parts.append(" ")

    # Завершает пропуск служебного тега или добавляет пробел после текстового блока.
    def handle_endtag(self, tag: str) -> None:
        if self.hidden_tags:
            if tag == self.hidden_tags[-1]:
                self.hidden_tags.pop()
        elif tag in _BLOCK_TAGS:
            self.parts.append(" ")

    # Сохраняет текст вне служебных тегов.
    def handle_data(self, data: str) -> None:
        if not self.hidden_tags:
            self.parts.append(data)


# Разбирает HTML и объединяет извлечённые фрагменты текста.
def _html_to_text(html: str) -> str:
    parser = _PageTextParser()
    parser.feed(html)
    parser.close()
    return "".join(parser.parts)


# Читает файл в UTF-8 и извлекает текст, если файл содержит HTML.
def read_text_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() in {".html", ".htm"}:
        return _html_to_text(text)
    return text


# Загружает страницу по HTTP или HTTPS и возвращает её текст.
def read_url_text(url: str) -> str:
    address = urlsplit(url)
    if address.scheme not in {"http", "https"} or not address.hostname:
        raise ValueError("Введите полный URL с http:// или https://.")

    tls_context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(url, timeout=10, context=tls_context) as response:
        content_type = response.headers.get_content_type()
        is_html = content_type in {"text/html", "application/xhtml+xml"}
        if not is_html and not content_type.startswith("text/"):
            raise ValueError(f"Неподдерживаемый тип содержимого: {content_type}.")
        encoding = response.headers.get_content_charset() or "utf-8-sig"
        text = response.read().decode(encoding)

    return _html_to_text(text) if is_html else text
