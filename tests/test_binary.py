import unittest

from triple_scan.binary import find_divisible_binaries, is_divisible_by_three


# Проверяет проверку и поиск двоичных записей чисел, кратных трём.
class BinarySearchTests(unittest.TestCase):
    # Проверяет ноль и несколько корректных канонических записей.
    def test_valid_format(self):
        for value in ("0", "11", "110", "1001", "1100", "1111", "10010"):
            with self.subTest(value=value):
                self.assertTrue(is_divisible_by_three(value))

    # Отклоняет некорректные символы, ведущие нули и числа не кратные трём.
    def test_invalid_format(self):
        for value in (
            "", "00", "01", "1", "10", "100", "101", "111",
            "2", "102", "-11", " 11", "11 ", "11\n", "１１",
        ):
            with self.subTest(value=value):
                self.assertFalse(is_divisible_by_three(value))

    # Сверяет регулярное выражение с остатком от деления первых 256 чисел.
    def test_all_values_in_small_range(self):
        for number in range(256):
            value = format(number, "b")
            with self.subTest(number=number):
                self.assertEqual(
                    is_divisible_by_three(value), number % 3 == 0
                )

    # Проверяет порядок совпадений, повторы и границы двоичных токенов.
    def test_search_preserves_order_and_repetitions(self):
        text = "Числа: 11, 10, 110; снова 11. Код X1001Y и 011 не подходят."
        self.assertEqual(
            find_divisible_binaries(text), ["11", "110", "11"]
        )

    # Для пустого текста совпадений нет.
    def test_search_empty_text(self):
        self.assertEqual(find_divisible_binaries(""), [])


if __name__ == "__main__":
    unittest.main()
