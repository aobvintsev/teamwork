import turtle

X_START = -200
Y_START = 200

# ToDo think about abstract writer for console or turtle instead of iterator


class ChainCodeReader:
    """
    Клас читає бінарне зображення, яке записано у текстовому файлі
    зірочками та крапками, та повертає послідовність ланцюгових кодів
    """
    def __init__(self, filename):
        self._codes = list()
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                self._extract_codes(line.strip(), i)
        self._index = 0

    def _extract_codes(self, line, row):
        """
        Виділити коди з рядка файлу.
        Модифікує поле self._codes
        :param line: рядок файлу без '\n' [str]
        :param row: номер рядка зображення [int]
        :return: None
        """
        line += '.'
        in_chain = False
        for i, c in enumerate(line):
            if c == '*':
                if not in_chain:
                    col = i
                    length = 0
                    in_chain = True
                length += 1
            else:
                if in_chain:
                    self._codes.append((row, col, length))
                in_chain = False

    @property
    def codes(self):
        """
        Властивість повертає список ланцюгових кодів зораження
        :return: список кодів [list]
        """
        return self._codes

    def __iter__(self):
        """
        Метод для підтримки ітеаційного протоколу
        Повертає себе в якості ітератора
        :return: self [ChainCodeReader]
        """
        return self

    def __next__(self):
        """
        Метод для підтримки ітеаційного протоколу
        Повертаэ наступний ланцюговий код
        :return:
        """
        if self._index >= len(self._codes):
            raise StopIteration

        elem = self._codes[self._index]
        self._index += 1
        return elem

    def reset(self):
        """
        Реініціалізувати ітератор
        :return: None
        """
        self._index = 0


class ChainCodePicture:
    """
    Клас зображує бінарне зображення у ланцюгових кодах
    за допомогою turtle
    """
    def __init__(self, codes, scale, color):
        self._codes = codes         # ланцюгові коди
        self._scale = scale         # масштаб зображення (кількість пікселів
                                    # у 1 точці
        self._color = color         # колір зображення
        self._x_start = X_START     # зсув зображення по x
        self._y_start = Y_START     # зсув зображення по y

    def show(self):
        """
        Показати зобаження
        :return: None
        """
        turtle.up()
        turtle.home()
        turtle.delay(0)
        turtle.color(self._color, self._color)
        for code in self._codes:
            self._show_code(code)

    def _show_point(self, row, col):
        """
        Показати 1 точку зображення у вигляді квадрата
        :param row: номер рядка
        :param col: номер стовпчика
        :return: None
        """
        turtle.up()
        turtle.setpos(self._x_start + col * self._scale,
                       self._y_start - row * self._scale)
        turtle.down()
        turtle.begin_fill()
        for i in range(4):
            turtle.fd(self._scale)
            turtle.right(90)
        turtle.end_fill()

    def _show_code(self, code):
        """
        Показати 1 ланцюговий код
        :param code:
        :return:
        """
        row, start_col, length = code
        for i in range(start_col, start_col + length):
            self._show_point(row, i)


if __name__ == '__main__':
    reader = ChainCodeReader('ht23.txt')
    picture = ChainCodePicture(reader.codes, 5, 'black')
    picture.show()
