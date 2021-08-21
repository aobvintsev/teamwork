import turtle


SCALE_X = 40
SCALE_Y = 60

HOR_UP = 1
HOR_DOWN = 2
DESCEND = 3
ASCEND = 4
VERT = 6
ELEMENTS = {
    0: (),
    1: (HOR_UP, ),
    2: (HOR_DOWN, ),
    3: (DESCEND, ),
    4: (ASCEND, ),
    5: (HOR_UP, ASCEND),
    6: (VERT, ),
    7: (HOR_UP, VERT),
    8: (HOR_DOWN, VERT),
    9: (HOR_UP, HOR_DOWN, VERT)
}

class CisterianNumber:
    def __init__(self, number):
        self._number = number
        self._digits = []
        n = self._number
        for i in range(4):
            self._digits.append(n % 10)
            n //= 10

    def add(self, other):
        return CisterianNumber((self._number + other._number) % 10000)

    def sub(self, other):
        return CisterianNumber(max(self._number - other._number, 0))

    def show(self, x, y):
        self._show_base(x, y)
        for order in range(4):
            self._show_digit(self._digits[order], order + 1, x, y)

    def _line(self, x1, y1, x2, y2):
        turtle.up()
        turtle.setpos(x1, y1)
        turtle.down()
        turtle.setpos(x2, y2)

    def _show_base(self, x, y):
        x1 = x2 = x + SCALE_X // 2
        y1 = y
        y2 = y - SCALE_Y
        self._line(x1, y1, x2, y2)

    def _mirror_hor(self, x, xx):
        delta = xx - (x + SCALE_X // 2)
        return (x + SCALE_X // 2) - delta

    def _mirror_vert(self, y, yy):
        delta = yy - (y - SCALE_Y // 2)
        return (y - SCALE_Y // 2) - delta

    def _define_coords(self, element, order, x, y):
        if element == HOR_UP:
            x1 = x + SCALE_X // 2
            x2 = x + SCALE_X
            y1 = y2 = y
        elif element == HOR_DOWN:
            x1 = x + SCALE_X // 2
            x2 = x + SCALE_X
            y1 = y2 = y - SCALE_Y // 3
        elif element == DESCEND:
            x1 = x + SCALE_X // 2
            x2 = x + SCALE_X
            y1 = y
            y2 = y - SCALE_Y // 3
        elif element == ASCEND:
            x1 = x + SCALE_X // 2
            x2 = x + SCALE_X
            y1 = y - SCALE_Y // 3
            y2 = y
        elif element == VERT:
            x1 = x2 = x + SCALE_X
            y1 = y
            y2 = y - SCALE_Y // 3

        if order in {2, 4}:
            x1 = self._mirror_hor(x, x1)
            x2 = self._mirror_hor(x, x2)
        if order in {3, 4}:
            y1 = self._mirror_vert(y, y1)
            y2 = self._mirror_vert(y, y2)
        return x1, y1, x2, y2

    def _show_digit(self, digit, order, x, y):
        for element in ELEMENTS[digit]:
            x1, y1, x2, y2 = self._define_coords(element, order, x, y)
            self._line(x1, y1, x2, y2)

if __name__ == '__main__':
    n = int(input('n=? '))
    c = CisterianNumber(n)
    c.show(-100, 100)
    m = input()
