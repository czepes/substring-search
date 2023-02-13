"""Модуль функции логирования времени"""

import functools
import time

from typing import Any, Callable


def calc_time(func: Callable) -> Callable:
    """
    Функция-декоратор для измерения времени выполнения
    :param func: Декорируемая функция
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Функция-обёртка
        :param args: Аргументы декорируемой функции
        :return: Результат выполнения декорируемой функции
        """
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Время выполнения: {end - start:.5f} сек.")
        return result
    return wrapper
