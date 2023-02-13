"""Модуль приложения командной строки"""

from typing import Optional, Union, List, Tuple, Dict

from math import ceil

import os

import argparse
import colorama
from colorama import Fore

from search import search


def search_app():
    """Функция обработки вызова из командной строки"""
    parser = argparse.ArgumentParser(
        description="Приложение поиска подстроки(-ок) в строке по алгоритму Кнута-Морриса-Пратта",
        prog="search"
    )
    parser.add_argument('substr', nargs='+', type=str, help="Подстроки для поиска")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', dest='string', help="Строка в которой ведётся поиск")
    group.add_argument('-f', dest='file', nargs='?', type=argparse.FileType('r', encoding='UTF-8'),
                       help="Файл в котором требуется провести поиск")
    parser.add_argument('-c', dest='count', default=None, type=int, help="Число искомых вхождений")
    parser.add_argument('--case', action='store_true', help="Чуствительность к регистру")
    parser.add_argument('--method', default='first', action='store_const', const='last',
                        help="Метод поиска с конца")
    args = parser.parse_args()
    string = ''
    if args.file is not None:
        with args.file:
            for line in args.file:
                string += line
    else:
        string = args.string
    string = limit_string(string)
    sub_string = args.substr
    entries = search(string=string, sub_string=sub_string, case_sensitivity=args.case,
                     method=args.method, count=args.count)
    output(string, sub_string, entries)


def limit_string(string: str) -> str:
    """
    Функция ограничиния длины строки
    :param string: Строка для ограничения
    :return: Ограниченная строка
    """
    max_str_len = os.get_terminal_size().columns
    max_str_val = 10
    lines_val = min(ceil(len(string) / max_str_len) + string.count("\n"), max_str_val)
    lines = [''] * lines_val
    shift = 0
    start = 0
    end = max_str_len
    for i in range(lines_val):
        lines[i] = string[start:end]
        if "\n" in lines[i]:
            shift += 1
            index = lines[i].find("\n") + 1
            lines[i] = lines[i][:index]
            start += index
            end += index
        else:
            start += max_str_len
            end += max_str_len
    return "".join(lines)


def output(string: str,
           sub_str: List[str],
           entries: Optional[Union[Tuple[int, ...], Dict[str, Tuple[int, ...]]]]):
    """
    Функция цветного вывода
    :param string: Строка для вывода
    :param sub_str: Список подстрок для поиска
    :param entries: Словарь вхождений подстрок
    :return:
    """
    if entries is None:
        print("Вхождений не найдено")
        return
    if isinstance(entries, tuple):
        entries = {sub_str[0]: entries}

    colorama.init()
    colors = (Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.BLACK, Fore.LIGHTBLACK_EX)
    max_sub_str_val = len(colors)

    i = 0
    colors_dict = {}
    for sub, values in entries.items():
        if i == max_sub_str_val:
            i -= max_sub_str_val
        if values is not None:
            colors_dict[sub] = colors[i]
            print(colors_dict[sub] + f"{sub}" + Fore.RESET + f": {values}")
            i += 1
        else:
            print(f"{sub}: Не найдено вхождений")

    entries = {k: v for k, v in sorted(entries.items(), key=lambda item: len(item[0])) if v is not None}
    indexes = {}
    for sub, values in entries.items():
        indexes[sub] = []
        for value in values:
            indexes[sub].extend(range(value, value + len(sub)))
        indexes[sub] = tuple(indexes.get(sub))

    for i, char in enumerate(string):
        for sub, values in indexes.items():
            if i in values:
                print(colors_dict[sub] + char + Fore.RESET, end="")
                break
        else:
            print(char, end="")


if __name__ == '__main__':
    search_app()
