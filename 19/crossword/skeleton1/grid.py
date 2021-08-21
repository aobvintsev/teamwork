"""
Модуль grid призначено для обробки сітки кросворду
Модуль містить класи:
OneCrossedWord
Grid
"""

from copy import copy
from collections import namedtuple

Cross = namedtuple(     # перетин слова з іншим словом
    "Cross",
    ["crossed_word",    # слово, що перетинається з даним,
                        # об'єкт класу OneCrossedWord
     "crossed_index"])  # індекс перетину у слові, що перетинається з даним


class OneCrossedWord:
    """
    Клас для обробки одного слова кросворду.
    """
    def __init__(self, no, pos, word_len, is_vert):
        self.no = no            # порядковий номер слова у кросворді: 1, 2 ...
        self.pos = pos          # позиція слова у сітці (рядок, стовпчик)
        self.len = word_len     # довжина слова
        self.is_vert = is_vert  # чи розташовано слово по вертикалі
        self.crosses = dict()   # словник перетинів, ключ - індекс перетину
        self.word = ""          # слово
        self.candidates = set() # слова-кандидати на входження у кросворд

    def add_cross(self, index, cross):
        """
        Додати перетин для слова.
        :param index: індекс перетину у даному слові
        :param cross: іменований кортеж для перетину Cross
        :return: None
        """
        self.crosses[index] = cross

    def set_candidates(self, candidates):
        """
        Встановити множину слів-кандидатів
        :param candidates: множина слів-кандидатів
        :return: None
        """
        self.candidates = candidates

    def next_match(self):
        """
        Перевіряє допустимість входження у кросворд слів-кандидатів
        Видаляє перевірені слова з множини кандидатів
        В разі успішності встановлює значення поля word
        :return: успішність bool
        """
        for candidate in copy(self.candidates):
            self.candidates.discard(candidate)
            if len(candidate) != self.len:
                continue

            if self._match(candidate):
                self.word = candidate
                return True

        return False

    def _match(self, candidate):
        """
        Перевіряє допустимість входження у кросворд одного слова-кандидата
        :param candidate: конадидат str
        :return: успішність bool
        """
        for index, cross in self.crosses.items():
            letter = cross.crossed_word.get_crossed_letter(
                cross.crossed_index)
            if letter and letter != candidate[index]:
                return False

        return True

    def get_crossed_letter(self, index):
        """
        Повертає літеру, що стоїть (можливо) на перетині за заданим індексом
        :param index: індекс літери
        :return: літера або None
        """
        if not self.word:
            return None

        return self.word[index]

    def clear(self):
        """
        Очищує слово
        :return:
        """
        self.word = ""

    def __str__(self):
        return "OneCrossedWord(no={}, pos={}, len={}, word={}, crosses={})" \
            .format(self.no, self.pos, self.len, self.word, self.crosses)


class WrongGrid(Exception):
    """
    Клас виключення для неправильної сітки
    """
    pass


class Grid:
    """
    Клас обробки сітки кросворду
    Сітка зберігається у текстововму файлі у вигляді
    _v_______
    h*****___
    _*____v__
    _*____*__
    Літерами v, h, b позначається початок слова по
        h - горизонталі
        v - вертикалі
        b - горизонталі та вертикалі
    Слова позначаються зірочкамиЮ порожні місця - підкресленнями
    Усі рядки файлу мають бути однакової довжини
    Після завантаження з файлу сітка міститься у двовимірному масиві символів
    """
    def __init__(self, filename):
        self._filename = filename   # ім'я файлу сітки
        self._grid = []             # масив сітки
        self._words = list()        # список слів - об'єктів класу OneCrossedWord
        self._cur_index = 0         # індекс поточного слова

    def read(self):
        """
        Читає сітку з файлу у масив
        Будує список слів, для кожного слова будує словник перетинів
        У масиві замінює символи початку слова на номер слова
        :return: None
        """


    def find_word_by_pos(self, pos, is_vert=True):
        """
        Знаходить слово за позицією у масиві
        :param pos: кортеж (рядок, стовпчик)
        :param is_vert: чи розташоване слово по вертикалі
        :return: слово (str) або None
        """

    def __iter__(self):
        """
        Метод ітератора
        :return: повертає себе
        """

    def __next__(self):
        """
        Метод ітератора
        повертає наступне слово
        :return:
        """

    def undo_next(self):
        """
        Відмінити останнє передане слово та повернутись до попереднього,
        змінює поточний індекс слова
        Ініціює помилку WrongGrid, якщо не можемо повернутись
        до попереднього слова
        :return:
        """

    def reset(self):
        """
        Перезапустити ітератор спочатку
        :return: None
        """

    def show(self):
        """
        Показати сітку, замінивши символи початку слова на номер слова,
        та '_'  на ' '
        :return: None
        """

    def show_words(self):
        """
        Показати слова
        :return: None
        """


if __name__ == "__main__":
    g = Grid("grid.txt")
    g.read()
    g.show()
    g.show_words()
