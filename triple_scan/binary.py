# Проверка двоичных чисел на делимость на три.

import re

# Ноль или двоичные записи без ведущих нулей, значение которых делится на 3.
MULTIPLE_PATTERN = re.compile(
    r"(?<!\w)(?:0|1(?:01*0)*1(?:0|1(?:01*0)*1)*)(?!\w)"
)


# Проверяет, что вся строка является двоичной записью числа, кратного трём.
def is_divisible_by_three(value: str) -> bool:
    return MULTIPLE_PATTERN.fullmatch(value) is not None


# Возвращает найденные записи в порядке появления, включая повторы.
def find_divisible_binaries(text: str) -> list[str]:
    return MULTIPLE_PATTERN.findall(text)
