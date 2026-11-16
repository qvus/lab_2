# Консольная утилита для проверки двоичных записей чисел, кратных трём.

import sys
from http.client import HTTPException
from pathlib import Path

from triple_scan.binary import find_divisible_binaries, is_divisible_by_three
from triple_scan.text_sources import read_text_file, read_url_text


MENU = """
1. Проверить двоичную запись числа
2. Найти числа во введённом тексте
3. Найти числа в файле
4. Найти числа на веб-странице
0. Выйти
"""


# Выводит найденные записи по одной на строку или сообщает об их отсутствии.
def print_matches(text: str) -> None:
    matches = find_divisible_binaries(text)
    if matches:
        print(*matches, sep="\n")
    else:
        print("Двоичные записи чисел, кратных трём, не найдены.")


# Показывает меню и выполняет выбранные действия до выхода из программы.
def main() -> None:
    try:
        while True:
            print(MENU, end="")
            choice = input("Выберите действие: ").strip()

            try:
                if choice == "0":
                    return
                if choice == "1":
                    value = input("Введите двоичную запись числа: ")
                    if is_divisible_by_three(value):
                        print("Запись корректна: число кратно трём.")
                    else:
                        print("Запись некорректна или число не кратно трём.")
                elif choice == "2":
                    print_matches(input("Введите текст: "))
                elif choice == "3":
                    path = input("Введите путь к файлу: ").strip()
                    print_matches(read_text_file(Path(path).expanduser()))
                elif choice == "4":
                    url = input("Введите URL страницы: ").strip()
                    print_matches(read_url_text(url))
                else:
                    print("Выберите пункт от 0 до 4.")
            except (OSError, ValueError, LookupError, RuntimeError, HTTPException) as error:
                print(f"Ошибка: {error}", file=sys.stderr)
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == "__main__":
    main()
