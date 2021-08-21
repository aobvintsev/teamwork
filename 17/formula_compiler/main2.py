#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль призначено для перевірки роботи модулів
tokenizer
syntax_analyzer
storage
code_generator
interpreter
та виконання лінійних програм, що складаються з присвоєнь
"""

from storage import Storage
from code_generator import CodeGenerator
from interpreter import Interpreter, ERRORS


def load_program(filename):
    """
    Функція завантажує програму з файлу filename
    та повертає список рядків програми.
    :param filename: ім'я файлу
    :return: список рядків
    """
    f = open(filename, 'r')
    program_lines = f.read().splitlines()
    f.close()
    return program_lines


def print_program(program_lines):
    """
    Функція показує програму за списком її рядків
    :param program_lines: список рядків програми
    :return: None
    """
    for line in program_lines:
        print(line)


def execute_program(program_lines):
    """
    Функція виконує програму та показує стан пам'яті після виконання
    :param program_lines: список рядків програми
    :return: None
    """
    print_program(program_lines)

    storage = Storage()
    cd = CodeGenerator(program_lines, storage)
    code, error = cd.generate_code()
    if error:
        print("Помилка при генерації коду: {}".format(error))
        return None, error

    interpreter = Interpreter(code, storage)
    last_error = interpreter.execute()
    if last_error:
        error = ERRORS[last_error]
        print("Помилка виконання програми {}".format(error))
        return interpreter, error

    print("Стан пам'яті")
    interpreter.show_variables()
    return interpreter, ""


if __name__ == '__main__':
    print("\nprogram1")
    interpreter, error = execute_program(load_program('program1.txt'))
    success = error == "Неправильно розставлені дужки"

    print("\nprogram2")
    interpreter, error = execute_program(load_program('program2.txt'))
    success = success and error == "Ділення на 0"

    print("\nprogram3")
    interpreter, error = execute_program(load_program('program3.txt'))
    z = interpreter.get_value('z')
    success = success and error == "" and z == 27.0

    print("\nSuccess =", success)
