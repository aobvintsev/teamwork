#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль призначено для перевірки роботи модулів
tokenizer
syntax_analyzer
storage
та обчислення значення простого виразу (сума доданків)

"""

from tokenizer import get_tokens
from syntax_analyzer import SyntaxAnalyzer
from storage import Storage

def fill_storage(tokens, store):
    for tok in tokens:
        if tok.type == "variable":
            store.add(tok.value)


def compute_sum(tokens, store):
    s = 0
    for tok in tokens:
        if tok.type == "constant":
            value = float(tok.value)
            s += value
        elif tok.type == "variable":
            value = store.get(tok.value)
            s += value
    return s


expression = "5 + a + 3"
tokens = get_tokens(expression)

analyzer = SyntaxAnalyzer(tokens)
success, error = analyzer.check_expression_syntax()

if success:
    store = Storage()
    fill_storage(tokens, store)
    store.set("a", 2)
    s = compute_sum(tokens, store)
    success = s == 10

print("Success =", success)
