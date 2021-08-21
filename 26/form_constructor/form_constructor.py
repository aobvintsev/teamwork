# Клас конструктор форм

from tkinter import *

class FormConstructor:
    '''
    Клас призначено для створення форми у графічному режимі
    за описом у файлі.

    self.master - вікно, у якому розміщується вікно редагування.
    self.filename - ім'я файлу з описом форми
    self.out_file - ім'я файлу для збереження результатів введення
    self.elements - список рядків файлу з описами полів
    self.has_buttons - чи є власні кнопки у вікна редагування
    self.vars - список з текстовими змінними для зв'язування
               з полями введення та списками
    self.labels - список з надписами
    self.ent_lists - список з полями введення або списками
    '''
    def __init__(self, master, filename, out_file, has_buttons=True):
        self.master = master
        self.filename = filename
        with open(self.filename, 'r', encoding='utf-8') as f:
            self.elements = f.readlines()
            self.elements = list(map(lambda x: x.strip(), self.elements))
        self.out_file = out_file
        self.has_buttons = has_buttons
        self._make_widgets()

    def _make_widgets(self):
        '''Створити елементи інтерфейсу форми.'''
        # рамка для полів введення та списків
        self.fedit = Frame(self.master, bd=1, relief=SUNKEN) 
        self._make_entries()
        self._layout_entries()
        if self.has_buttons:
            fbut = Frame(self.master)   # рамка з кнопками
            fbut.grid(row=1, column=0, sticky=(E, W))
            # кнопка 'Відмінити'
            bcancel = Button(fbut, text = 'Відмінити',
                   command = self.cancel_handler)
            bcancel.grid(row=0,column=2, sticky=(E), padx=5, pady=5)
            # кнопка 'Готово'
            bok = Button(fbut, text = 'Готово',
                   command = self.ok_handler)
            bok.grid(row=0,column=1, sticky=(E), padx=5, pady=5)
            # кнопка 'Далі'
            bnext = Button(fbut, text = 'Далі',
                   command = self.next_handler)
            bnext.grid(row=0,column=0, sticky=(E), padx=5, pady=5)
            # забезпечити зміну розмірів області кнопок
            fbut.columnconfigure(0, weight=1)

    def _get_label_type_values(self, line):
        if line[-1] == '}': # поле введення
            label = line.split('{')[0].strip()
            typ = "entry"
            values = []
        else:   # список
            parts = line.split('[')
            label = parts[0].strip()
            typ = "list"
            values_str = parts[1].strip(']')
            values = values_str.split(',')
        return label, typ, values

    def _make_entries(self):
        '''Створити надписи та поля введення або списки.'''
        self.vars = []
        self.labels = []
        self.ent_lists = []
        for i, line in enumerate(self.elements):
            label, typ, values = self._get_label_type_values(line)
            # додати надпис до словника надписів
            self.labels.append(Label(self.fedit, text=label))
            # створити текстову змінну для поля введення або списку
            # та встановити її початкове значення
            self.vars.append(StringVar())
            self.vars[-1].set("")
            # додати поле введення або список та зв'язати з текстовою змінною
            if typ == "entry":
                self.ent_lists.append(
                    Entry(self.fedit, textvariable=self.vars[-1]))
            else:
                self.ent_lists.append(
                    Listbox(self.fedit, exportselection=0,
                            width=len(max(values, key=len)),
                            height=len(values)))
                self.ent_lists[-1].bind('<<ListboxSelect>>', self.select_handler(i))
                for val in values:
                    self.ent_lists[-1].insert(END, val)

    def _layout_entries(self):
        '''Розмістити надписи та поля введення або списки.'''
        for i in range(len(self.labels)):
            # розмістити надписи у першому стовпчику
            self.labels[i].grid(row=i, column=0,
                                sticky=(W), padx=1, pady=1)
            # розмістити поля введення у другому стовпчику
            self.ent_lists[i].grid(row=i, column=1,
                                   sticky=(W, E), padx=1, pady=1)
        # розташувати рамку у вікні self.master
        self.fedit.grid(row=0, column=0, sticky=(W,E,N,S)) 
        # забезпечити зміну розмірів рамок з елементами та кнопками    
        self.master.columnconfigure(0, weight=1)
        # забезпечити зміну розмірів області елементів    
        self.fedit.columnconfigure(0, weight=1)
        self.fedit.columnconfigure(1, weight=2)

    def select_handler(self, i):
        '''Обробити вибір елементу зі списку.'''
        def handle(ev):
            self.vars[i].set(self.ent_lists[i].get(
                self.ent_lists[i].curselection()))

        return handle

    def ok_handler(self, ev=None):
        '''Обробити натиснення кнопки "Готово".'''
        self._save()
        self.master.destroy()   # закрити вікно self.master
        
    def next_handler(self, ev=None):
        '''Обробити натиснення кнопки "Далі".'''
        self._save()
        self._clear()

    def cancel_handler(self, ev=None):
        '''Обробити натиснення кнопки "Відмінити".'''
        self._clear()

    def _clear(self):
        for v in self.vars:
            v.set("")

    def _save(self):
        with open(self.out_file, 'a', encoding='utf-8') as f:
            parts = ['"{}"'.format(x.get()) for x in self.vars]
            line = ','.join(parts) + '\n'
            f.write(line)

    def get(self):
        '''Повернути останні значення усіх полів введення або списків.'''
        return [v.get() for v in self.vars]


if __name__ == '__main__':    
    top = Tk()
    fc = FormConstructor(top, 'form.txt', 'data.txt')
    top.mainloop()
    d = fc.get()
    print(d)
