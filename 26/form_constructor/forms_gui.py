from tkinter import *
from form_constructor import FormConstructor

DATA_FILE = "data.txt"
FORM_FILE = "form.txt"

class FormsGUI:
    '''Клас для організації введення даних за допомогою форми.

       self.top - вікно верхнього рівня у якому розміщено елементи
                  інтерфейсу
       self.data_file - ім'я файлу з даними
       self.form_file - ім'я файлу опису форми
    '''

    def __init__(self, master, form_file, data_file):
        self.top = master
        self.data_file = data_file
        self.form_file = form_file
        with open(self.data_file, 'w'): # очистити файл
            pass
        self._make_widgets()

    def _make_widgets(self):
        '''Створити елементи інтерфейсу.'''
        self.finput = Frame(self.top)  # контейнер для списку з даними
        self.finput.pack(fill=X, expand=YES)
        self.sb_all = Scrollbar(self.finput)
        self.sb_all.pack(side=RIGHT, fill=Y)
        self.l_all = Listbox(self.finput, height=15, width=70,
                             yscrollcommand=self.sb_all.set,
                             font=('arial', 16))
        self.sb_all.config(command=self.l_all.yview)
        self.l_all.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.fbut = Frame(self.top)  # контейнер для кнопок
        self.fbut.pack(side=LEFT, fill=X, expand='1')
        self.benter = Button(self.fbut, text='Ввести дані',
                            command=self._enter_data,
                            font=('arial', 16))
        self.benter.pack(side=LEFT, padx=5, pady=5)
        self.bquit = Button(self.fbut, text='Закрити',
                            command=top.quit,
                            font=('arial', 16))
        self.bquit.pack(side=RIGHT, padx=5, pady=5)  # кнопка "Закрити"

    def _enter_data(self):
        '''Ввести дані у форму'''
        dialog = Toplevel()
        dl = FormConstructor(dialog, self.form_file, self.data_file)
        # зробити діалог модальним
        dialog.focus_set()
        dialog.grab_set()
        dialog.wait_window()
        self._fill_list()

    def _fill_list(self):
        '''Заповнити список.'''
        self.l_all.delete(0, END)
        with open(self.data_file, 'r', encoding='utf-8') as f:
            for line in f:
                self.l_all.insert(END, line.strip())


if __name__ == '__main__':
    from sys import argv

    if len(argv) < 3:
        form_file = FORM_FILE
        data_file = DATA_FILE
    else:
        form_file = argv[1]
        data_file = argv[2]
    top = Tk()
    r = FormsGUI(top, form_file, data_file)
    mainloop()
