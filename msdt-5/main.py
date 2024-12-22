import math


def calculate_statistics(numbers):
    """Вычисление среднего значения, медианы и стандартного отклонения для заданных чисел"""
    if not numbers:
        raise ValueError("Список должен быть не пустым.")

    n = len(numbers)
    mean = sum(numbers) / n

    sorted_numbers = sorted(numbers)
    if n % 2 == 0:
        median = (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
    else:
        median = sorted_numbers[n // 2]

    variance = sum((x - mean) ** 2 for x in numbers) / n
    std_dev = math.sqrt(variance)

    return {"Среднее значение": mean, "Медиана": median, "Стандартное отклонение": std_dev}


def is_palindrome(s):
    """Является ли слово палиндромом."""
    s = ''.join(filter(str.isalnum, s)).lower()
    return s == s[::-1]


def recursive_factorial(n):
    """Вычисление факториала с помощью рекурсии"""
    if n < 0:
        raise ValueError("Число должно быть неотрицательным.")
    return 1 if n in (0, 1) else n * recursive_factorial(n - 1)


def can_form_string(s, sub):
    """Можно ли получить строку используя подстроку"""
    if not s or not sub:
        return False
    if len(s) % len(sub) != 0:
        return False
    return s == sub * (len(s) // len(sub))
