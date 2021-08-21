import time
from chain_code import ChainCodePicture, ChainCodeReader


SCALE = 10
COLOR = "black"

class ChainCodeFigure:
    def __init__(self, codes=()):
        self._codes = list(codes)
        self._weight = sum(c[2] for c in self._codes)

    def add_code(self, code):
        self._codes.append(code)
        self._weight += code[2]

    @property
    def codes(self):
        return self._codes

    def intersects(self, code):
        code_row, code_col, code_length = code
        for row, col, length in self._codes:
            if abs(row - code_row) == 1 and (
                    code_col <= col < code_col + code_length or
                    col <= code_col < col + length or
                    code_col <= col + length - 1 < code_col + code_length or
                    col <= code_col + code_length - 1 < col + length):
                return True

        return False

    def merge(self, other):
        self._codes.extend(other.codes)
        self._weight += other._weight
        self._codes.sort()

    def weight(self):
        return self._weight

    def rect(self):
        x_min = min(c[1] for c in self._codes)
        y_min = min(c[0] for c in self._codes)
        x_max = max(c[1] + c[2] - 1 for c in self._codes)
        y_max = max(c[0] for c in self._codes)
        return x_min, y_min, x_max, y_max

    def start_row(self):
        return min(c[0] for c in self._codes)

    def start_col(self):
        return min(c[1] for c in self._codes)

    def mass_center(self):
        weight = self.weight()
        assert weight, "Can't calculate mass center for empty figure"

        x_sum = y_sum = 0
        for row, col, length in self._codes:
            y_sum += row * length
            x_sum +=  sum(range(col, col + length))
        return x_sum / weight, y_sum / weight

    def __lt__(self, other):
        return self.start_row() < other.start_row() or \
               (self.start_row() == other.start_row() and
                self.start_col() < other.start_col())

    def show(self):
        cp = ChainCodePicture(self._codes, SCALE, COLOR)
        cp.show()


if __name__ == '__main__':
    def build_figures(reader):
        figures = list()
        for code in reader:
            intersected = list()
            for figure in figures:
                if figure.intersects(code):
                    intersected.append(figure)

            if intersected:
                new_figure = intersected[0]
                new_figure.add_code(code)
                figures.remove(new_figure)
                for isect in intersected[1:]:
                    new_figure.merge(isect)
                    figures.remove(isect)
            else:
                new_figure = ChainCodeFigure([code])
            figures.append(new_figure)
        return figures


    reader = ChainCodeReader('ht23.txt')
    mass_centers = list()
    figures = build_figures(reader)
    figures.sort()
    figures_num = len(figures)
    print("Figures number:", figures_num)
    for i, figure in enumerate(figures, 1):
        figure.show()
        weight = figure.weight()
        rect = figure.rect()
        x, y = figure.mass_center()
        print("Figure {}. Rect: {} Weight: {}, Mass center ({}, {})".format(
            i, rect, weight, x, y))
        mass_centers.append((int(y), int(x), 1))

    cp = ChainCodePicture(mass_centers, SCALE, "red")
    cp.show()
    time.sleep(5)
