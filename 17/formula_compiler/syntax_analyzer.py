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

Метод check_expression_syntax за заданим списком токенів
для виразу має повернути
булівське значення та (можливо) помилку
Кожний токен - це кортеж: (<тип токену>, <значення токену>)
Перевірка робиться на допустимість сусідніх токенів,
правильний перший та останній токен, порожній вираз,
правильність розставлення дужок

Метод check_assignment_syntax за заданим списком токенів
для присвоєння має повернути
булівське значення та (можливо) помилку.
"""
from tokenizer import Token, get_tokens

# словник множин допустимих наступних токеныв для заданого токена
VALID_PAIRS = {"variable": {"operation", "right_paren"},
               "constant": {"operation", "right_paren"},
               "operation": {"variable", "constant", "left_paren"},
               "left_paren": {"left_paren", "variable", "constant"},
               "right_paren": {"right_paren", "operation"},
               "other": set()}

# словник помилок
ERRORS = {"invalid_pair": "Недопустима пара токенів {}, {}",
          "incorrect_parens": "Неправильно розставлені дужки",
          "empty_expr": "Порожній вираз"}

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self._tokens = tokens[:]
        
    def check_expression_syntax(self):
        """
        Метод перевіряє синтаксичну правильність виразу за списком токенів.
        Використовує внутрішні методи _check_parens, _check_pair
        Повертає булівське значення та рядок помилки.
        Якщо помилки немає, то повертає порожній рядок
        :param tokens: список токенів
        :return: sucess - булівське значення
        :return: error - рядок помилки
        """
        self._tokens = [Token("left_paren", "(")] + self._tokens + [Token("right_paren", ")")]
        if len(self._tokens) == 2:
            return False, ERRORS["empty_expr"]
    
        if not self._check_parens():
            return False, ERRORS["incorrect_parens"]
    
        for i in range(len(self._tokens) - 1):
            if not self._check_pair(self._tokens[i], self._tokens[i + 1]):
                return False, ERRORS["invalid_pair"].format(self._tokens[i],
                                                            self._tokens[i + 1])
        return True, ""
    
    
    def _check_parens(self):
        """
        Метод перевіряє чи правильно розставлені дужки у виразі.
        Повертає булівське значення
        :param tokens: список токенів
        :return: sucess - булівське значення
        """
        depth = 0
        for tok in self._tokens:
            if tok.type == "left_paren":
                depth += 1
            elif tok.type == "right_paren":
                depth -= 1
            if depth < 0:
                break
    
        return depth == 0
    
    
    def _check_pair(self, tok, next_tok):
        """
        Метод перевіряє чи правильна пара токенів.
        Повертає булівське значення
        :param tok: поточний токен
        :param next_tok: наступний токен
        :return: sucess - булівське значення
        """
    
        return next_tok.type in VALID_PAIRS[tok.type]

if __name__ == "__main__":
    analyzer = SyntaxAnalyzer(get_tokens("(((ab1_ - 345.56)(*/.2{_cde23"))
    success1, error1 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzer(get_tokens("(ab1_ - 345.56)*/.2_cde23"))
    success2, error2 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzer(get_tokens(" - 345.56*/.2_cde23"))
    success3, error3 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzer(get_tokens("2 - 345.56 *"))
    success4, error4 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzer(get_tokens("2 - .2"))
    success5, error5 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzer(get_tokens("   "))
    success6, error6 = analyzer.check_expression_syntax()
    analyzer = SyntaxAnalyzer(get_tokens("((abc -3 * b2) + d5 / 7)"))
    success7, error7 = analyzer.check_expression_syntax()

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
        success7 and error7 == ""
    )

    print("Success =", success)
