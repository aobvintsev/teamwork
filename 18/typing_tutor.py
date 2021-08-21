#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from time import time


class TypingError(Exception):
    pass


class TimeError(Exception):
    pass


class TypingTutor:

    def __init__(self, words_file, words_num, interval):
        self._words_num = words_num
        self._interval = interval
        self._protocol = list()
        with open(words_file, 'r', encoding='utf-8') as f:
            self._all_words = f.read().split()
            random.shuffle(self._all_words)
            self._words = self._all_words[:self._words_num]

    def train(self):
        for word in self._words:
            enterd_ok = time_ok = True
            try:
                self.train_word(word)
                points = len(word)
            except TypingError:
                points = -1
                enterd_ok = False
            except TimeError:
                points = 0
                time_ok = False

            self._protocol.append((word, enterd_ok, time_ok, points))

    def train_word(self, word):
        start_time = time()
        input_word = input(f"слово - {word}: ")
        end_time = time()
        if word != input_word:
            raise TypingError
        if end_time - start_time > self._interval:
            raise TimeError

    def get_protocol(self):
        return self._protocol

    def clear(self):
        self._protocol.clear()
        random.shuffle(self._all_words)
        self._words = self._all_words[:self._words_num]


if __name__ == '__main__':
    tutor = TypingTutor('words.txt', words_num=5, interval=4)
    tutor.train()
    protocol = tutor.get_protocol()
    print("Сума:", sum(list(zip(*protocol))[3]))
    print('Протокол')
    print(*protocol, sep='\n')
