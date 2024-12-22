import pytest
from unittest.mock import patch
from main import calculate_statistics, is_palindrome, recursive_factorial, can_form_string


@pytest.mark.parametrize("numbers, expected", [
    ([1, 2, 3, 4, 5], {"Среднее значение": 3.0, "Медиана": 3, "Стандартное отклонение": pytest.approx(1.4142, 0.0001)}),
    ([2, 2, 2, 2], {"Среднее значение": 2.0, "Медиана": 2.0, "Стандартное отклонение": 0.0}),
    ([1], {"Среднее значение": 1.0, "Медиана": 1.0, "Стандартное отклонение": 0.0}),
])
def test_calculate_statistics(numbers, expected):
    result = calculate_statistics(numbers)
    assert result["Среднее значение"] == expected["Среднее значение"]
    assert result["Медиана"] == expected["Медиана"]
    assert result["Стандартное отклонение"] == expected["Стандартное отклонение"]


def test_calculate_statistics_empty_list():
    with pytest.raises(ValueError, match="Список должен быть не пустым."):
        calculate_statistics([])


@pytest.mark.parametrize("s, expected", [
    ("A man a plan a canal Panama", True),
    ("No lemon, no melon", True),
    ("Hello", False),
    ("", True),
])
def test_is_palindrome(s, expected):
    assert is_palindrome(s) == expected


@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (5, 120),
    (10, 3628800),
])
def test_recursive_factorial(n, expected):
    assert recursive_factorial(n) == expected


@pytest.mark.parametrize("n", [20, 30, 40])
def test_recursive_factorial_large(n):
    result = recursive_factorial(n)
    assert isinstance(result, int)
    assert result > 0


def test_recursive_factorial_negative():
    with pytest.raises(ValueError, match="Число должно быть неотрицательным."):
        recursive_factorial(-5)


@pytest.mark.parametrize("s, sub, expected", [
    ("ababab", "ab", True),
    ("aaaa", "aa", True),
    ("abcabcabcabc", "abc", True),
    ("abcd", "ab", False),
    ("", "a", False),
])
def test_can_form_string(s, sub, expected):
    assert can_form_string(s, sub) == expected


@patch("main.math.sqrt")
def test_mock_calculate_statistics(mock_sqrt):
    mock_sqrt.return_value = 42  # Стаб для math.sqrt
    result = calculate_statistics([4, 4, 4, 4])  # Должно вызвать sqrt(0)
    assert result["Стандартное отклонение"] == 42
    mock_sqrt.assert_called_once_with(0)
