#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль призначено для виконання коду, який згенеровано генератором коду.
Генератор коду повертає список команд.
Кожна команда - це кортеж: (<код_команди>, <операнд>)

Інтрепретатор виконує обчислення з використанням стеку.
Стек - це список, у який ми можемо додавати до кінця та брати з кінця числа.
Щоб додати число до стеку, можна використати
_stack.append(number)
Щоб взяти число зі стеку, можна використати
number = _stack.pop()
Для виконання арифметичної операції інтерпретатор бере два останніх числа зі стеку,
обчислює результат операції та додає результат до стеку.

Допустимі команди:
("LOADC", <число>) - завантажити число у стек
("LOADV", <змінна>) - завантажити значення змінної у стек (використовується storage)
("ADD", None) - обчислити суму двох верхніх елементів стеку
("SUB", None) - обчислити різницю двох верхніх елементів стеку
("MUL", None) - обчислити добуток двох верхніх елементів стеку
("DIV", None) - обчислити частку від ділення двох верхніх елементів стеку
("SET", <змінна>) - встановити значення змінної у пам'яті (storage)
"""
from storage import Storage

# словник, що співствляє коди помилок до їх описи
ERRORS = {0: "",
          1: "Недопустима команда",
          2: "Змінна не існує",
          3: "Ділення на 0"}


class Interpreter():
    def __init__(self, code, storage):
        self._code = code           # програмний код (результат роботи
                                    # генератора коду)
        self._storage = storage     # пам'ять
        self._stack = []            # стек інтерпретатора
                                    # для виконання обчислень
        self._last_error = 0        # код помилки останньої операції

        self._command_funcs = {     # словник методів обробки команд
            "LOADC": self._loadc,
            "LOADV": self._loadv,
            "ADD": self._add,
            "SUB": self._sub,
            "MUL": self._mul,
            "DIV": self._div,
            "SET": self._set,
        }

    def _loadc(self, number):
        """
        Метод завантажує число у стек.
        Щоб додати у стек, використовує _stack.append(...)
        Побічний ефект: встановлює значення _last_error у 0
        :param number: число
        :return: None
        """
        self._last_error = 0
        self._stack.append(number)

    def _loadv(self, variable):
        """
        Метод завантажує значення змінної з пам'яті у стек.
        Якщо змінної не існує, то встановлює відповідну помилку.
        Якщо змінна не визначена, вводить значення зміної
        за допомогою storage.
        Використовує модуль storage
        Щоб додати у стек, використовує _stack.append(...)
        Побічний ефект: змінює значення _last_error
        :param variable: ім'я змінної
        :return: None
        """
        if not self._storage.is_in(variable):
            self._last_error = 2
            return

        self._last_error = 0
        value = self._storage.get(variable)
        if value is None:
            self._storage.input_var(variable)
            value = self._storage.get(variable)
        self._stack.append(value)

    def _add(self, _=None):
        """
        Метод бере 2 останніх елемента зі стеку,
        обчислює їх суму та додає результат у стек.
        Щоб взяти значення зі стеку, використовує _stack.pop()
        Щоб додати у стек, використовує _stack.append(...)
        Побічний ефект: встановлює значення _last_error у 0
        :param _: ігнорується
        :return: None
        """
        self._last_error = 0
        second = self._stack.pop()
        first = self._stack.pop()
        self._stack.append(first + second)

    def _sub(self, _=None):
        """
        Метод бере 2 останніх елемента зі стеку,
        обчислює їх різницю та додає результат у стек.
        Щоб взяти значення зі стеку, використовує _stack.pop()
        Щоб додати у стек, використовує _stack.append(...)
        Побічний ефект: встановлює значення _last_error у 0
        :param _: ігнорується
        :return: None
        """
        self._last_error = 0
        second = self._stack.pop()
        first = self._stack.pop()
        self._stack.append(first - second)

    def _mul(self, _=None):
        """
        Метод бере 2 останніх елемента зі стеку,
        обчислює їх добуток та додає результат у стек.
        Щоб взяти значення зі стеку, використовує _stack.pop()
        Щоб додати у стек, використовує _stack.append(...)
        Побічний ефект: встановлює значення _last_error у 0
        :param _: ігнорується
        :return: None
        """
        self._last_error = 0
        second = self._stack.pop()
        first = self._stack.pop()
        self._stack.append(first * second)

    def _div(self, _=None):
        """
        Метод бере останнй та передостанній елементи зі стеку,
        обчислює частку від ділення передостаннього елемента на останній
        та додає результат у стек.
        Якщо дільник - 0, то встановлює помилку.
        Щоб взяти значення зі стеку, використовує _stack.pop()
        Щоб додати у стек, використовує _stack.append(...)
        Побічний ефект: встановлює значення _last_error у 0
        :param _: ігнорується
        :return: None
        """
        self._last_error = 0
        second = self._stack.pop()
        first = self._stack.pop()
        if second == 0:
            self._last_error = 3
            return

        self._stack.append(first / second)

    def _set(self, variable):
        """
        Метод бере останній елемент зі стеку
        та встановлює значення змінної рівним цьому елементу.
        Якщо змінної не існує, то встановлює відповідну помилку.
        Щоб взяти значення зі стеку, використовує _stack.pop()
        Побічний ефект: змінює значення _last_error
        :param variable: ім'я змінної
        :return: None
        """
        if not self._storage.is_in(variable):
            self._last_error = 2
            return

        self._last_error = 0
        value = self._stack.pop()
        self._storage.set(variable, value)

    def execute(self):
        """
        Метод виконує код програми, записаний у self._code.
        Повертає код останньої помилки або 0, якщо помилки немає.
        Якщо є помилка, то показує її.
        Використовує словник функцій COMMAND_FUNCS
        :return: код останньої помилки або 0, якщо помилки немає
        """
        for command in self._code:
            func = self._command_funcs.get(command[0])
            if not func:
                self._last_error = 1
            else:
                func(command[1])
            if self._last_error:
                print ("Помилка виконання: {}".format(ERRORS[self._last_error]))
                break

        return self._last_error

    def show_variables(self):
        """
        Метод показує значення усіх змінних пам'яті
        у форматі <змінна> = <значення>
        :return: None
        """
        variables = self._storage.get_all()
        for variable in variables:
            print("{} = {}".format(variable, variables[variable]))

    def get_value(self, variable):
        """
        Метод повертає значення зміної variable з пам'яті
        Якщо змінної у пам'яті немає або вона невизначена, повертає None
        :param variable: ім'я змінної
        :return: float (or None)
        """
        value = None
        if self._storage.is_in(variable):
            value = self._storage.get(variable)
        return value

    def add_to_storage(self, variable):
        """
        Метод додає зміну variable до пам'яті
        :param variable: ім'я змінної
        :return: None
        """
        self._storage.add(variable)


if __name__ == "__main__":

    code = [('LOADC', 1.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y'),
            ('LOADV', 'x'),
            ('LOADV', 'a'),
            ('MUL', None),
            ('SET', 't'),
            ('LOADC', 1.0),
            ('LOADV', 'x'),
            ('LOADV', 'y'),
            ('SUB', None),
            ('DIV', None),
            ('SET', 'z')]
    interpreter = Interpreter(code, Storage())
    interpreter.add_to_storage('x')
    interpreter.add_to_storage('y')
    interpreter.add_to_storage('a')
    interpreter.add_to_storage('t')
    interpreter.add_to_storage('z')
    last_error = interpreter.execute()

    success = last_error == 3

    code = [('XXX', 1.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y')]
    interpreter = Interpreter(code, Storage())
    last_error = interpreter.execute()

    success = success and last_error == 1

    code = [('LOADC', 1.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y')]
    interpreter = Interpreter(code, Storage())
    last_error = interpreter.execute()

    success = success and last_error == 2

    code = [('LOADC', 2.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y'),
            ('LOADC', 1.0),
            ('LOADV', 'x'),
            ('LOADV', 'y'),
            ('SUB', None),
            ('DIV', None),
            ('SET', 'z')]
    interpreter = Interpreter(code, Storage())
    interpreter.add_to_storage('x')
    interpreter.add_to_storage('y')
    interpreter.add_to_storage('z')
    last_error = interpreter.execute()

    z = interpreter.get_value('z')
    success = success and last_error == 0 and z == 1.0

    print("Success =", success)
