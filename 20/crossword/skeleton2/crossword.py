from thesaurus import Thesaurus
from grid import Grid


class CrossWord:
    """
    Будує кросворд за заданою сіткою та тезаурусом, якщо це можливо
    """
    def __init__(self, thes_filename, grid_filename):
        self._thesaurus = Thesaurus(thes_filename)  # тезаурус
        self._grid = Grid(grid_filename)            # сітка

        self._thesaurus.read()
        self._grid.read()
        self._descriptions_vert = list()            # описи слів по вертикалі
        self._descriptions_hor = list()             # описи лів по горизонталі

    def check_cross_word(self):
        """
        Перевіряє можливість побудови та будує кросворд
        Будує описи слів
        :return:
        """


    def show(self):
        """
        Показує сітку кросворду та описи слів
        :return:
        """


if __name__ == "__main__":
    cw = CrossWord("thesaurus.txt", "grid.txt")
    cw.check_cross_word()
    cw.show()
