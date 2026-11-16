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
4. Найти числа на странице с примерами
0. Выйти
"""

EXAMPLE_PAGE_URL = (
    "https://ursinus-cs373-f2021.github.io/CoursePage/"
    "ClassExercises/Week2_Formal/"
)


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
                    print(f"Загружаю страницу: {EXAMPLE_PAGE_URL}")
                    print_matches(read_url_text(EXAMPLE_PAGE_URL))
                else:
                    print("Выберите пункт от 0 до 4.")
            except (OSError, ValueError, LookupError, RuntimeError, HTTPException) as error:
                print(f"Ошибка: {error}", file=sys.stderr)
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == "__main__":
    main()
