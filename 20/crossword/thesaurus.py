
class Thesaurus:
    """
    Клас працює з тезаурусом (тлумачним словником)
    Словник записано у файлі у форматі:
    "слово":"опис"
    Кожне слово разом з описо записано у окремому рядку файлу
    """
    def __init__(self, filename):
        self._filename = filename   # ім'я файлу тезаурусу
        self._thesaurus = dict()    # тезаурус - словник з ключами - словами
                                    # та значеннями - описами слів
        self._words_lists = dict()  # словник списків слів заданої довжини
                                    # ключі - довжини слів, значення - списки слів

    def read(self):
        """
        Читає тезаурус з файлу, будує словник self._thesaurus та списки слів
        :return:
        """
        with open(self._filename, 'r') as f:
            for line in f:
                line = line.strip()
                # print(line)
                if not line:
                    break

                word, description = line.split(':')
                self._thesaurus[word.strip('"')] = description.strip('"')

        self._build_words_lists()

    def _build_words_lists(self):
        maxlen = len(max(self._thesaurus, key=len))
        for word_len in range(1, maxlen + 1):
            self._words_lists[word_len] = [w for w in self._thesaurus
                                           if len(w) == word_len]

    def get_words_with_len(self, word_len):
        """
        Повертає список слів заданої довжини word_len
        :param word_len: довжина слова
        :return: список слів [list]
        """
        return set(self._words_lists.get(word_len, []))

    def get_description(self, word):
        """
        Повертає опис слова word
        :param word: слово
        :return: опис [str]
        """
        return self._thesaurus.get(word, "")


if __name__ == "__main__":
    t = Thesaurus("thesaurus.txt")
    t.read()
    for i in range(1, 6):
        words_i = t.get_words_with_len(i)
        for word in words_i:
            print(word, t.get_description(word))
