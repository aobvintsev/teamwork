#!/usr/bin/env python3
import re

EMPTY_LINE = '\n'

def get_next_paragraph(lines, i):
    while i < len(lines) and lines[i] == EMPTY_LINE:
        i+=1

    para = []
    while i < len(lines) and lines[i] != EMPTY_LINE:
        para.append(lines[i])
        i+=1

    return para, i

def get_word(para, word, para_no):
    words = []
    for line in para:
        string = re.sub(r'''[!?.,+:;"'()\-…—«»]+''', ' ', line)
        string = string.lower()
        words += string.split()
#        print(words)

    word_indeces = []
    while word in words:
        i = words.index(word) + 1
        words = words[i:]
        word_indeces.append((para_no, i))

    return word_indeces

def get_all_words(lines, word):
    para_no = 0
    line_no = 0
    indeces = []
    while True:
        para, line_no = get_next_paragraph(lines, line_no)
#        print(para)
        if not para:
            break
        para_no += 1
        indeces += get_word(para, word, para_no)

    return indeces


def show_word_occures():
    word = input("word: ")
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            ind = get_all_words(lines, word)
        print(filename)
        for j, i in enumerate(ind):
            if j > 10:
                break
            print(i)
    

def test_para_word_no():
    para_no = int(input("paragraph no: "))
    word_no = int(input("word no: "))

    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        line_no = 0
        for i in range(para_no):
            para, line_no = get_next_paragraph(lines, line_no)
            if line_no >= len(lines):
                print("no para")
                break
        
        words = []
        for line in para:
            string = re.sub(r'''[!?.,+:;"'()\-…—«»]+''', ' ', line)
            string = string.lower()
            words += string.split()

        print(filename)
        
        print(words[word_no - 1] if word_no <= len(words) else "no word")
    
# hardcode paths to 3 texts
files = ["1.txt",
         "2.txt",
         "3.txt"]
    
mode = int(input("mode [1 - word, 2 - test]"))

if mode == 1:
    show_word_occures()
else:
    test_para_word_no()

