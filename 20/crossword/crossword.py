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
        count = 0
        words_in_use = []
        for word in self._grid:
            if word.no > count:
                count += 1
                words_in_use.append("")
                candidates = self._thesaurus.get_words_with_len(word.len) - \
                             set(words_in_use)
                word.set_candidates(candidates)
            if not word.next_match():
                word.clear()
                words_in_use.pop()
                count -= 1
                self._grid.undo_next()
                self._grid.undo_next()
            else:
                words_in_use[-1] = word.word

        self._grid.reset()
        for word in self._grid:
            if word.is_vert:
                self._descriptions_vert.append(
                    (word.no, self._thesaurus.get_description(word.word)))
            else:
                self._descriptions_hor.append(
                    (word.no, self._thesaurus.get_description(word.word)))

    def show(self):
        """
        Показує сітку кросворду та описи слів
        :return:
        """
        self._grid.show()
        self._grid.show_words()
        print("Horizontal", *self._descriptions_hor, sep='\n')
        print("Vertical", *self._descriptions_vert, sep='\n')


if __name__ == "__main__":
    cw = CrossWord("thesaurus.txt", "grid.txt")
    cw.check_cross_word()
    cw.show()
