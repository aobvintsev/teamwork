#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль призначено для генерації коду за списком рядків програми.
Генератор коду повертає список команд.
Кожна команда - це кортеж: (<код_команди>, <операнд>)

У подальшому обчислення будуть виконуватись з використанням стеку.
Стек - це список, у який ми можемо додавати до кінця та брати з кінця числа.

Для виконання арифметичної операції буде братись
два останніх числа зі стеку,
обчислювати результат операції та додавати результат до стеку.
Тому генератор повинен згенерувати команди
завантаження змінних та констант до стеку
а також виконання арифметичних операцій та присвоєння.

Допустимі команди:
("LOADC", <число>) - завантажити число у стек
("LOADV", <змінна>) - завантажити значення змінної у стек
                      (використовується storage)
("ADD", None) - обчислити суму двох верхніх елементів стеку
("SUB", None) - обчислити різницю двох верхніх елементів стеку
("MUL", None) - обчислити добуток двох верхніх елементів стеку
("DIV", None) - обчислити частку від ділення двох верхніх елементів стеку
("SET", <змінна>) - встановити (присвоїти) значення змінної
                    у пам'яті (storage) рівним
                    значенню останнього елементу стеку

Генерація коду виконується за допомогою рекурсивного розбору виразу.
Вираз (expression) представляється як один доданок (term) або сума (різниця)
багатьох доданків.
Доданок (term) представляється як один множник (factor) або добуток
(частка від ділення) багатьох множників.
Множник (factor) представляється як константа або змінна,
або вираз (expression) у дужках.

Під час розбору кожен метод забирає токени зі списку токенів tokens,
а також додає команди до списку команд code
"""
from storage import Storage
from tokenizer import get_tokens
from syntax_analyzer_ext import SyntaxAnalyzerExt

COMMANDS = ("LOADC",
            "LOADV",
            "ADD",
            "SUB",
            "MUL",
            "DIV",
            "SET")

class CodeGenerator:
    def __init__(self, program_lines, storage):
        self._storage = storage
        self._program_lines = program_lines

    def generate_code(self):
        """
        Метод генерує код за списком рядків програми program_lines
        Повертає програмний код у вигляді списку кортежів
        (<код_команди>, <операнд>)
        Також, якщо під час генерації коду або аналізу виникає помилка,
        то повертає текст помилки. Якщо помилки немає, то повертає порожній рядок.
        Побічний ефект: очищує пам'ять.
        :param program_lines: список рядків програми
        :return: список команд - кортежів (<код_команди>, <операнд>)
        :return: текст помилки
        """
        code = []
        self._storage.clear()
        for program_line in self._program_lines:
            line_code, error = self._generate_line_code(program_line)
            if error:
                break
            code += line_code
        return code, error

    def _generate_line_code(self, program_line):
        """
        Метод генерує код за рядком програми program_line.
        Рядок програми має бути присвоэнням виду x = e,
        де x - змінна, e - вираз, або порожнім рядком.
        Використовує модулі tokenizer та syntax_analyzer для розбору
        та аналізу правильності синтаксису рядка програми.
        Використовує функцію _expression для генерації коду виразу, після чого
        генерує команду SET для змінної з лівої частини присвоєння, та додає
        змінну до пам'яті (storage), якщо потрібно.
        Якщо program_line - порожній рядок, то функція його ігнорує.
        Повертає програмний код для рядка програми у вигляді списку кортежів
        (<код_команди>, <операнд>)
        Також, якщо під час генерації коду або аналізу виникає помилка,
        то повертає текст помилки. Якщо помилки немає, то повертає порожній рядок.
        :param program_line: рядок програми
        :return: список команд - кортежів (<код_команди>, <операнд>)
        :return: текст помилки
        """
        code = []
        tokens = get_tokens(program_line)
        if not tokens:
            return code, ""

        analyzer = SyntaxAnalyzerExt(tokens)
        success, error = analyzer.check_assignment_syntax()
        if error:
            return code, error

        self._expression(code, tokens[2:])
        variable = tokens[0].value
        if not self._storage.is_in(variable):
            self._storage.add(variable)
        code.append(("SET", variable))
        return code, error

    def _expression(self, code, tokens):
        """
        Метод генерує код за списком токенів виразу.
        Використовує функцію _term для генерації коду доданку, після чого,
        поки список токенів не спорожніє і поточний токен - це операція
        '+' або '-', знову використовує _term для наступного доданку та
        генерує команду ADD або SUB.
        Побічний ефект: змінює список code та список tokens
        (видаляє розглянуті токени)
        :param code: список команд - кортежів (<код_команди>, <операнд>)
        :param tokens: список токенів
        :return: None
        """
        self._term(code, tokens)

        while tokens and tokens[0].type == "operation" \
                and tokens[0].value in ('+', '-'):
            token = tokens.pop(0)
            operation = token.value
            self._term(code, tokens)
            if operation == '+':
                code.append(("ADD", None))
            elif operation == '-':
                code.append(("SUB", None))

    def _term(self, code, tokens):
        """
        Метод генерує код за списком токенів, що починається токенами доданку.
        Використовує функцію _factor для генерації коду множника, після чого,
        поки список токенів не спорожніє і поточний токен - це операція
        '*' або '/', знову використовує _factor для наступного множника та
        генерує команду MUL або DIV.
        Побічний ефект: змінює список code та список tokens
        (видаляє розглянуті токени)
        :param code: список команд - кортежів (<код_команди>, <операнд>)
        :param tokens: список токенів
        :return: None
        """
        self._factor(code, tokens)
        while tokens and tokens[0].type == "operation" \
                and tokens[0].value in ('*', '/'):
            token = tokens.pop(0)
            operation = token.value
            self._factor(code, tokens)
            if operation == '*':
                code.append(("MUL", None))
            elif operation == '/':
                code.append(("DIV", None))

    def _factor(self, code, tokens):
        """
        Метод генерує код за списком токенів, що починається токенами множника.
        Якщо перший токен - "left_paren", то множник - це вираз у дужках і треба
        викликати функцію _expression, після чого пропустити праву дужку.
        Якщо перший токен - константа або змінна, то треба згенерувати команду
        LOADC (додатково - перетворити константу з рядка у дійсне число) або
        LOADV (додатково - додати змінну до пам'яті, якщо необхідно).
        Побічний ефект: змінює список code та список tokens
        (видаляє розглянуті токени)
        :param code: список команд - кортежів (<код_команди>, <операнд>)
        :param tokens: список токенів
        :return: None
        """
        token = tokens.pop(0)
        if token.type == "left_paren":
            self._expression(code, tokens)
            if not tokens or tokens[0].type != "right_paren":
                print("Factor: ')' expected")
                return
            tokens.pop(0)
        elif token.type == "constant":
            code.append(("LOADC", float(token.value)))
        elif token.type == "variable":
            variable = token.value
            if not self._storage.is_in(variable):
                self._storage.add(variable)
            code.append(("LOADV", variable))
        else:
            print("Factor: Invalid token", token.type)

    def in_storage(self, variable):
        """
        Метод перевіряє, чи міститься змінна variable у пам'яті.
        :param variable: ім'я змінної
        :return: bool - и міститься змінна variable у пам'яті
        """
        return self._storage.is_in(variable)

if __name__ == "__main__":
    generator = CodeGenerator(["a = b + c", "y = (2 - 1"],
                              Storage())
    code, error = generator.generate_code()
    success = error == "Неправильно розставлені дужки"

    generator = CodeGenerator(["x = 1",
                               "z = (((a)))",
                               "a = b + c * (d - e)",
                               "y = (2 - 1) * (x345 + 3 * d) / 234.5 - z"],
                              Storage())
    code, error = generator.generate_code()
    success = success and not error and \
        code == [('LOADC', 1.0),
                 ('SET', 'x'),
                 ('LOADV', 'a'),
                 ('SET', 'z'),
                 ('LOADV', 'b'),
                 ('LOADV', 'c'),
                 ('LOADV', 'd'),
                 ('LOADV', 'e'),
                 ('SUB', None),
                 ('MUL', None),
                 ('ADD', None),
                 ('SET', 'a'),
                 ('LOADC', 2.0),
                 ('LOADC', 1.0),
                 ('SUB', None),
                 ('LOADV', 'x345'),
                 ('LOADC', 3.0),
                 ('LOADV', 'd'),
                 ('MUL', None),
                 ('ADD', None),
                 ('MUL', None),
                 ('LOADC', 234.5),
                 ('DIV', None),
                 ('LOADV', 'z'),
                 ('SUB', None),
                 ('SET', 'y')]

    success = success and generator.in_storage('a')
    success = success and generator.in_storage('x')

    print("Success =", success)
