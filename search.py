"""Модуль поиска подстроки в строке"""

from typing import Union, Optional, List, Tuple, Dict

from time_calculator import calc_time


@calc_time
def search(string: str,
           sub_string: Union[str, List[str]],
           case_sensitivity: bool = False,
           method: str = 'first',
           count: Optional[int] = None) -> Optional[Union[Tuple[int, ...], Dict[str, Tuple[int, ...]]]]:
    """
    Общая функция поиска подстроки в строке по алгоритму Кнута-Морриса-Пратта
    :param string: Строка в которой ведётся поиск
    :param sub_string: Подстрока или список подстрок для поиска
    :param case_sensitivity: Вкл/Выкл чуствительность к регистру
    :param method: Метод поиска: last - в обратном порядке с конца, в остальных случаях в прямом порядке с начала
    :param count: Число искомых вхождений (если равняется None идёт поиск всех вхождений)
    :return: Словарь подстрок с кортежами первых индексов вхождений, если было передано несколько подстрок;
        Кортеж первых индексов вхождений, если была передана одна подстрока;
        None если не было найдено ни одного вхождения.
    """
    if isinstance(sub_string, str):
        sub_string = [sub_string]
    elif isinstance(sub_string, tuple):
        sub_string = list(sub_string)
    if not case_sensitivity:
        string = string.lower()
        for i, char in enumerate(sub_string):
            sub_string[i] = char.lower()
    if count is not None and count < 0:
        count = None

    entries = {sub_str: None for sub_str in sub_string}
    for sub_str in sub_string:
        entries[sub_str] = search_alg(string, sub_str, method, count)

    if tuple(entries.values()) == (None,) * len(entries):
        entries = None
    if isinstance(entries, dict) and len(entries) == 1:
        entries = tuple(entries.values())[0]

    return entries


def get_prefix_tuple(string: str) -> Tuple[int, ...]:
    """
    Функция нахождения кортежа максимальной длины префиксов и суффиксов для каждой подстроки
    :param string: Подстрока
    :return: Кортеж длин префиксов
    """
    i = 1
    j = 0
    prefix = [0] * len(string)
    while i < len(string):
        if string[j] == string[i]:
            prefix[i] = j + 1
            i += 1
            j += 1
        else:
            if j == 0:
                prefix[i] = 0
                i += 1
            else:
                j = prefix[j - 1]
    return tuple(prefix)


def search_alg(string: str,
               sub_str: str,
               method: str,
               count: Optional[int]) -> Optional[Tuple[int, ...]]:
    """
    Функия поиска вхождения подстрок в строку по алгоритму Кнута-Морриса-Пратта
    :param string: Строка в которой ведётся поиск
    :param sub_str: Подстрока для поиска
    :param method: Метод поиска
    :param count: Число искомых вхождений
    :return: Кортеж индексов первых вхождений или None если их нет
    """
    indexes = []
    prefix = get_prefix_tuple(sub_str)
    str_len = len(string)
    sub_str_len = len(sub_str)
    j = 0
    i = 0
    multiplier = 1
    if method == 'last':
        i = str_len - 1
        str_len = 1
        multiplier = -1
    while multiplier * i < str_len:
        if count is not None and len(indexes) == count:
            break
        index = j
        value = i - sub_str_len + 1
        if method == 'last':
            index = sub_str_len - j - 1
            value = i
        if sub_str[index] == string[i]:
            if j == sub_str_len - 1:
                indexes.append(value)
                j = 0
                if sub_str_len == 1:
                    i += multiplier
                continue
            i += multiplier
            j += 1
        else:
            if j > 0:
                j = prefix[j - 1]
            else:
                i += multiplier
    return tuple(indexes) if len(indexes) > 0 else None
