#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль призначено для синтаксичного розбору виразу та присвоєння по частинах.

Вираз може мати вигляд:
(abc + 123.5)*d2-3/(x+y)
присвоєння може мати вигляд:
x = a + b
Вираз може містити:
    змінні - ідентифікатори
    константи - дійсні або цілі числа без знаку
    знаки операцій: +, -, *, /
    дужки: (, )

Функція get_tokens за заданим виразом має повертати
послідовність лексем - токенів
Кожний токен - це кортеж: (<тип токену>, <значення токену>)
"""

from collections import namedtuple

# типи токенів
TOKEN_TYPE = ("variable",
              "constant",
              "operation",
              "left_paren",
              "right_paren",
              "other",
              "equal")

# словник фіксованих токенів, що складаються з одного символа
TOKEN_TYPES = {"+": "operation",
               "-": "operation",
               "*": "operation",
               "/": "operation",
               "(": "left_paren",
               ")": "right_paren",
               "=": "equal"}

# тип токена
Token = namedtuple('Token', ['type', 'value'])


def get_tokens(string):
    """
    Функція за рядком повертає список токенів типу Token
    :param string: рядок
    :return: список токенів
    """
    tokens = []
    while string:
        next_tok, string = _get_next_token(string)
#        print(next_tok, string)
        if next_tok:
            tokens.append(next_tok)
    return tokens

def _get_next_token(string):
    """
    Функція повертає наступний токен та залишок рядка
    Використовує внутрішні функції _get_constant, _get_variable
    :param string: рядок
    :return: next_tok - наступний токен, якщо є, або None
    :return: string - залишок рядка
    """
    string = string.strip()
    if not string:
        return None, string

    if string[0] in TOKEN_TYPES:
        next_tok = Token(TOKEN_TYPES[string[0]], string[0])
        string = string[1:]
    else:
        num, s = _get_constant(string)
        if num:
            next_tok = Token("constant", num)
            string = s
        else:
            var, s = _get_variable(string)
            if var:
                next_tok = Token("variable", var)
                string = s
            else:
                next_tok = Token("other", string[0])
                string = string[1:]

    return next_tok, string


def _get_constant(string):
    """
    Функція за рядком повертає константу (якщо є) та залишок рядка
    :param string: рядок
    :return: константа (або порожній рядок), залишок рядка
    """
    if not string or not string[0].isdigit():
        return "", string

    k = 0
    for i, c in enumerate(string):
        if not c.isdigit() and c != '.' or c == '.' and k > 1:
            break
        if c == '.':
            k += 1
    else:
        i += 1

    return string[:i], string[i:]


def _get_variable(string):
    """
    Функція за рядком повертає змінну (якщо є) та залишок рядка
    :param string: рядок
    :return: змінна (або порожній рядок), залишок рядка
    """
    if not string or not string[0].isalpha() and string[0] != '_':
        return "", string

    for i, c in enumerate(string):
        if not c.isalnum() and c != '_':
            break
    else:
        i += 1

    return string[:i], string[i:]


if __name__ == "__main__":
    success = get_tokens("(((ab1_ - 345.56)(*/.2{_cde23") == (
                [Token(type='left_paren', value='('),
                Token(type='left_paren', value='('),
                Token(type='left_paren', value='('),
                Token(type='variable', value='ab1_'),
                Token(type='operation', value='-'),
                Token(type='constant', value='345.56'),
                Token(type='right_paren', value=')'),
                Token(type='left_paren', value='('),
                Token(type='operation', value='*'),
                Token(type='operation', value='/'),
                Token(type='other', value='.'),
                Token(type='constant', value='2'),
                Token(type='other', value='{'),
                Token(type='variable', value='_cde23')])

    success = success and get_tokens("x = (a + b)")==[
        Token(type='variable', value='x'),
        Token(type='equal', value='='),
        Token(type='left_paren', value='('),
        Token(type='variable', value='a'),
        Token(type='operation', value='+'),
        Token(type='variable', value='b'),
        Token(type='right_paren', value=')')]
    print("Success =", success)
