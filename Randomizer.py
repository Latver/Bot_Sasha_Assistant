import customtkinter as ctk
from tkinter import *
from tkinter import Entry, END, messagebox, Tk, Button, filedialog, Label, BooleanVar
import tkinter as tk
from tkinter import ttk
import win32api, random

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

#Функция рандомайзера
def random_exit_menu_random_2(window):
    try:
        random_win.deiconify()
        main_random_win.destroy()
    except NameError:
        window.deiconify()
        main_random_win.destroy()
    except TclError:
        window.deiconify()
        main_random_win.destroy()
    except AttributeError:
        window.deiconify()
        main_random_win.destroy()

# Скрытие меню случайного числа и открытие генератора чисел
def withdraw_generator_number(window):
    try:
        main_random_win.withdraw()
        generator_number(window)
    except NameError:
        window.withdraw()
        generator_number(window)
    except TclError:
        random_number_random_win(window)
    except AttributeError:
        window.withdraw()
        generator_number(window)

# Скрытие меню случайного числа и открытие вывода
def withdraw_random_number(window):
    try:
        main_random_win.withdraw()
        random_number(window)
    except NameError:
        window.withdraw()
        random_number()
    except TclError:
        random_number_random_win()
    except AttributeError:
        window.withdraw()
        random_number(window)

# Меню случайного числа и генератора чисел
def random_number_random_win(window):
    font = ctk.CTkFont(family='Arial', size=20)
    try:
        window.withdraw()
        random_win.withdraw()
    except NameError:
        window.deiconify()
    except TclError:
        window.deiconify()
    except AttributeError:
        window.deiconify()

    global main_random_win
    main_random_win = ctk.CTkToplevel(window)
    main_random_win.resizable(width=False, height=False)
    main_random_win.title('Случайное число')
    main_random_win.protocol('WM_DELETE_WINDOW', lambda: random_exit_menu_random_2(window))

    main_random_win.geometry(f"{center_x - int(window_width / 1.3)}+{center_y - int(window_height / 4)}")

    main_random_win.columnconfigure([0,1], weight=1, minsize=60)
    main_random_win.rowconfigure([0], weight=1, minsize=0)
    
    button1 = ctk.CTkButton(main_random_win, text='от 1 до 100', command=lambda: withdraw_random_number(window), font=font)
    button1.grid(row=0, column=0, sticky='we', pady=2, padx=2)
    button2 = ctk.CTkButton(main_random_win, text='Генератор чисел', command=lambda: withdraw_generator_number(window), font=font)
    button2.grid(row=0, column=1, sticky='we', pady=2, padx=2)

# Вывод из случайного числа от 1 до 100
def random_number(window):
    font = ctk.CTkFont(family='Arial', size=20)
    def exit_menu_random():
        try:
            main_random_win.deiconify()
            output_main_random_win.destroy()
        except NameError:
            window.deiconify()
            output_main_random_win.destroy()
        except TclError:
            window.deiconify()
            output_main_random_win.destroy()
        except AttributeError:
            window.deiconify()
            output_main_random_win.destroy()

    def generated_random_number():
        text_r.configure(text=f'Ваше число: {random.randint(0, 100)}')
    def generated_random_number_enter(Return):
        generated_random_number()

    window.withdraw()
    output_main_random_win = ctk.CTkToplevel(window)
    output_main_random_win.resizable(width=False, height=False)
    output_main_random_win.title('Вывод')
    output_main_random_win.protocol('WM_DELETE_WINDOW', exit_menu_random)

    output_main_random_win.geometry(f"{center_x - int(window_width / 1.5)}+{center_y - int(window_height / 5)}")

    text_r = ctk.CTkLabel(output_main_random_win, font=font)
    text_r.grid(row=0, column=0, columnspan=4, rowspan=1, sticky='wens')
    text_r.configure(text=f'Ваше число: {random.randint(0, 100)}')

    button_output_main_random_win = ctk.CTkButton(output_main_random_win, text='Сгенерировать еще раз', command=generated_random_number, font=font)
    button_output_main_random_win.grid(row=1, column=0, columnspan=4, rowspan=1, sticky='we')

    output_main_random_win.bind('<Return>', generated_random_number_enter)
            
def generator_number(window):
    font = ctk.CTkFont(family='Arial', size=20)
    N = 'N'

    def enter_generate(Return):
        generate()

    def generate():
        try:
            b = before.get()
            t = to.get()
            if b > t:
                text_f.grid(row = 6, column = 2, columnspan = 4, rowspan = 2, sticky = 'we', pady=2, padx=2)
                text_f.configure(text = 'Ошибка!', font=font)
            b1 = int(b)
            t1 = int(t)
            N = random.randint(b1, t1)
            text_f.configure(text = f'Ваше число: {N}')
        except ValueError:
                text_f.grid(row = 6, column = 2, columnspan = 4, rowspan = 2, sticky = 'we', pady=2, padx=2)
                text_f.configure(text = 'Ошибка!', font=font)

    try:
        random_win.withdraw()
    except NameError:
        pass
    except TclError:
        pass
    except AttributeError:
        pass

    def exit_menu():
        try:
            main_random_win.deiconify()
            generator_number_win.destroy()
        except NameError:
            window.deiconify()
            generator_number_win.destroy()
        except TclError:
            window.deiconify()
            generator_number_win.destroy()
        except AttributeError:
            window.deiconify()
            generator_number_win.destroy()

    generator_number_win = ctk.CTkToplevel(window)
    generator_number_win.resizable(width=False, height=False)
    generator_number_win.title('Генератор чисел "От" и "До"')
    generator_number_win.bind('<Return>', enter_generate)
    generator_number_win.protocol('WM_DELETE_WINDOW', exit_menu)
    generator_number_win.geometry(f"{center_x - int(window_width / 2.55)}+{center_y - int(window_height / 4)}")

    generator_number_win.columnconfigure([0,1,2], weight=1, minsize=10)
    generator_number_win.rowconfigure([0,1,2], weight=1, minsize=10)

    text_g = ctk.CTkLabel(generator_number_win, font = font)
    text_g.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, stick = 'we', pady=2, padx=2)
    text_g.configure(text = 'От', font=font)

    text2_g = ctk.CTkLabel(generator_number_win, font = font)
    text2_g.grid(row = 1, column = 0, columnspan = 2, rowspan = 3, stick = 'we', pady=2, padx=2)
    text2_g.configure(text = 'До', font=font)

    before = ctk.CTkEntry(generator_number_win, justify=LEFT, font = font)
    before.grid(row = 0, column = 2, columnspan = 1, sticky='we', pady=2, padx=2)

    to = ctk.CTkEntry(generator_number_win, justify=LEFT, font = font)
    to.grid(row = 1, column = 2, rowspan = 3, columnspan = 1, sticky='we', pady=2, padx=2)

    text_f = ctk.CTkLabel(generator_number_win, font = font)
    text_f.grid(row = 6, column = 1, columnspan = 4, rowspan = 1, stick = 'we', padx=(0, 20))
    text_f.configure(text = f'Ваше число: {N}', font=font)

    button_r = ctk.CTkButton(generator_number_win, text = 'Сгенерировать', command = generate, font=font)
    button_r.grid(row = 4, column = 0, columnspan = 4, sticky = 'we', pady=2, padx=2)

def heads_or_tails(window):
    font = ctk.CTkFont(family='Arial', size=20)
    try:
        random_win.withdraw()
    except NameError:
        window.withdraw()

    def exit_menu():
        try:
            random_win.deiconify()
            heads_or_tails_win.destroy()
        except NameError:
            window.deiconify()
            heads_or_tails_win.destroy()
        except AttributeError:
            window.deiconify()
            heads_or_tails_win.destroy()

    heads_or_tails_win = ctk.CTkToplevel(window)
    heads_or_tails_win.geometry('280x100')
    heads_or_tails_win.resizable(width=False, height=False)
    heads_or_tails_win.title('Орёл или Решка')
    heads_or_tails_win.protocol('WM_DELETE_WINDOW', exit_menu)
    heads_or_tails_win.geometry(f"{center_x - int(window_width / 1.55)}+{center_y - int(window_height / 4)}")

    heads_or_tails_win.columnconfigure([0], weight=1, minsize=0)
    heads_or_tails_win.rowconfigure([0], weight=1, minsize=0)

    text_h = ctk.CTkLabel(heads_or_tails_win,text = 'Нажмите на кнопку', font = font)
    text_h.grid(row = 0, column = 0, stick = 'we')

    def throw_coin_not_enter():
        list = ['Орёл', 'Решка', 'Орёл', 'Решка']
        text_h.configure(text = f'{random.choice(list)}', font=font)
        text_h.grid(row = 0, column = 0, stick = 'we')

    def throw_coin(enter):
        throw_coin_not_enter()

    button1 = ctk.CTkButton(heads_or_tails_win, text = 'Бросить еще раз', command = throw_coin_not_enter, font=font)
    button1.grid(row = 1, column = 0, sticky='we')
    heads_or_tails_win.bind('<Return>', throw_coin)

def menu_random(window, window_other_menu):
    global random_win
    font = ctk.CTkFont(family='Arial', size=20)
    def exit_menu_2():
        try:
            window_other_menu.deiconify()
            random_win.destroy()
        except NameError:
            window.deiconify()
            random_win.destroy()
        except TclError:
            window.deiconify()
            random_win.destroy()
        except AttributeError:
            window.deiconify()
            random_win.destroy()

    try:
        window.withdraw()
        window_other_menu.withdraw()
    except NameError:
        pass
    except TclError:
        pass
    except AttributeError:
        pass

    random_win = ctk.CTkToplevel(window)
    random_win.resizable(width=False, height=False)
    random_win.title('Рандомайзер')
    random_win.protocol('WM_DELETE_WINDOW', exit_menu_2)

    random_win.geometry(f"{center_x - int(window_width / 1.3)}+{center_y - int(window_height / 4)}")

    # добавление кнопок с новым стилем
    button1 = ctk.CTkButton(random_win, text='Случайное число', command=lambda: random_number_random_win(window), font=font)
    button1.grid(row=0, column=0, sticky='we', pady=2, padx=2)
    button3 = ctk.CTkButton(random_win, text='Орёл или Решка', command=lambda: heads_or_tails(window), font=font)
    button3.grid(row=0, column=1, sticky='we', pady=2, padx=2)