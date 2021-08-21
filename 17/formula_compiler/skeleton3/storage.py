#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль призначено для реалізації пам'яті, що складається зі змінних.

Змінні можуть мати числові значення цілого або дійсного типу

"""

# словник, що співствляє коди помилок до їх описи
ERRORS = {0: "",
          1: "Змінна вже є у пам'яті",
          2: "Змінна не існує",
          3: "Змінна невизначена"}


class Storage():
    def __init__(self):
        self._storage = {}      # пам'ять
        self._last_error = 0    # код помилки останньої операції

    def add(self, variable):
        """
        Метод додає змінну у память.
        Якщо така змінна вже існує, то встановлює помилку
        :param variable: змінна
        :return: None
        """


    def is_in(self, variable):
        """
        Метод перевіряє, чи є змінна у пам'яті.
        :param variable: змінна
        :return: булівське значенна (True, якщо є)
        """


    def get(self, variable):
        """
        Метод повертає значення змінної.
        Якщо така змінна не існує або невизначена (==None),
        то встановлює відповідну помилку
        :param variable: змінна
        :return: значення змінної
        """


    def set(self, variable, value):
        """
        Метод встановлює значення змінної
        Якщо змінна не існує, повертає помилку
        :param variable: змінна
        :param value: нове значення
        :return: None
        """
        if variable not in self._storage:
            self._last_error = 2
        else:
            self._last_error = 0
            self._storage[variable] = value

    def input_var(self, variable):
        """
        Метод здійснює введення з клавіатури та встановлення значення змінної
        Якщо змінна не існує, повертає помилку
        :param variable: змінна
        :return: None
        """


    def input_all(self):
        """
        Метод здійснює введення з клавіатури та встановлення значення
        усіх змінних з пам'яті
        :return: None
        """


    def clear(self):
        """
        Метод видаляє усі змінні з пам'яті
        :return: None
        """


    def get_last_error(self):
        """
        Метод повертає код останньої помилки code
        Для виведення повідомлення треба взяти
        storage.ERRORS[code]
        усіх змінних з пам'яті
        :return: код останньої помилки
        """


    def get_all(self):
        """
        Метод повертає словник змінних пам'яті
        :return: словник змінних
        """


if __name__ == "__main__":
    store = Storage()
    store.add("a")
    success = store.get_last_error() == 0
    store.add("a")
    success = success and store.get_last_error() == 1
    c = store.get("a")
    success = success and c == None and store.get_last_error() == 3
    c = store.get("b")
    success = success and c == None and store.get_last_error() == 2
    store.set("a", 1)
    success = success and store.get_last_error() == 0
    c = store.get("a")
    success = success and c == 1 and store.get_last_error() == 0
    store.set("b", 2)
    success = success and store.get_last_error() == 2
    store.add("x")
    store.input_var("x")  # ввести значення x = 2
    success = success and store.get_last_error() == 0
    f = store.get("x")
    success = success and f == 2 and store.get_last_error() == 0
    store.clear()
    success = success and store.get_last_error() == 0
    store.add("a")
    success = success and store.get_last_error() == 0
    store.add("d")
    success = success and store.get_last_error() == 0
    store.input_all()  # ввести значення a = 3, d = 4
    success = success and store.get_last_error() == 0
    c = store.get("a")
    success = success and c == 3 and store.get_last_error() == 0
    f = store.get("d")
    success = success and f == 4 and store.get_last_error() == 0
    success = success and store.is_in("a")
    success = success and {"a", "d"} == set(store.get_all().keys())

    print("Success =", success)
