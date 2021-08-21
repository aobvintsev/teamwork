#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль призначено для перевірки синтаксичної правильності виразу та присвоєння.

Вираз може мати вигляд:
(abc + 123.5)*d2-3/(x+y)
Вираз може містити:
    змінні - ідентифікатори
    константи - дійсні або цілі числа без знаку
    знаки операцій: +, -, *, /
    дужки: (, )

Присвоєння - це

<змінна> = <вираз>
наприклад
 x = a + b


Метод check_assignment_syntax за заданим списком токенів
для присвоєння має повернути
булівське значення та (можливо) помилку.
"""
from tokenizer import Token, get_tokens
from syntax_analyzer import SyntaxAnalyzer

# словник помилок
ERRORS = {"invalid_pair": "Недопустима пара токенів {}, {}",
          "incorrect_parens": "Неправильно розставлені дужки",
          "empty_expr": "Порожній вираз",
          "incorrect_assignment": "Неправильне присвоєння"}


class SyntaxAnalyzerExt(SyntaxAnalyzer):
    def __init__(self, tokens):
        SyntaxAnalyzer.__init__(self, tokens)

    def check_assignment_syntax(self):
        """
        Метод перевіряє синтаксичну правильність присвоєння за списком токенів.
        Повертає булівське значення та рядок помилки.
        Якщо помилки немає, то повертає порожній рядок.
        Використовує метод check_expression_syntax
        :param tokens: список токенів
        :return: sucess - булівське значення
        :return: error - рядок помилки
        """


if __name__ == "__main__":
    analyzer = SyntaxAnalyzerExt(get_tokens("(((ab1_ - 345.56)(*/.2{_cde23"))
    success1, error1 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzerExt(get_tokens("(ab1_ - 345.56)*/.2_cde23"))
    success2, error2 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzerExt(get_tokens(" - 345.56*/.2_cde23"))
    success3, error3 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzerExt(get_tokens("2 - 345.56 *"))
    success4, error4 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzerExt(get_tokens("2 - .2"))
    success5, error5 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzerExt(get_tokens("   "))
    success6, error6 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzerExt(get_tokens("((abc -3 * b2) + d5 / 7)"))
    success7, error7 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzerExt(get_tokens("x + y"))
    success8, error8 = analyzer.check_assignment_syntax()
    analyzer = SyntaxAnalyzerExt(get_tokens("x ="))
    success9, error9 = analyzer.check_assignment_syntax()
    analyzer = SyntaxAnalyzerExt(get_tokens("x = (a+b)"))
    success10, error10 = analyzer.check_assignment_syntax()

    success = (
        not success1 and error1 == 'Неправильно розставлені дужки' and
        not success2 and error2 ==
        "Недопустима пара токенів Token(type='operation', value='*'),"
        " Token(type='operation', value='/')" and
        not success3 and not success4 and
        not success5 and error5 ==
        "Недопустима пара токенів Token(type='operation', value='-'), "
        "Token(type='other', value='.')" and
        not success6 and error6 == "Порожній вираз" and
        success7 and error7 == "" and
        not success8 and error8 == "Неправильне присвоєння" and
        not success9 and error9 == "Порожній вираз" and
        success10 and error10 == ""
    )

    print("Success =", success)
