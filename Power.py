import os
import re
import customtkinter as ctk
from PIL import Image as PILImage
import tkinter as tk
from tkinter import *
from tkinter import Entry, END, messagebox, Tk, Button, filedialog, Label, BooleanVar

current_directory = os.path.dirname(os.path.abspath(__file__))
path_to_icons = f'{current_directory}\\icons'

photo_image_exit = ctk.CTkImage(dark_image=PILImage.open(f"{path_to_icons}\\Back_or_Exit.png"), size=(30, 30))

def exit_menu_power(label_line_symbols, button1, button2, button3, button4, button5, button6, button9, button14, button15, window):
    try:
        button1.grid()
        button2.grid()
        button3.grid()
        button4.grid()
        button5.grid()
        button6.destroy()
        button9.destroy()
        button14.destroy()
        button15.destroy()
    except (NameError, TclError, AttributeError):
        label_line_symbols.destroy()
        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()
        button6.destroy()
        button9.destroy()
        button14.destroy()
        button15.destroy()

def exit_menu_reboot(label_line_symbols, button1, button2, button3, button4, button5, button7, button8, button9, button10, button15, window):
    try:
        label_line_symbols.destroy()
        button1.grid()
        button2.grid()
        button3.grid()
        button4.grid()
        button5.grid()
        button7.destroy()
        button8.destroy()
        button9.destroy()
        button10.destroy()
        button15.destroy()
    except (NameError, TclError, AttributeError):
        label_line_symbols.destroy()
        button1.grid()
        button2.grid()
        button3.grid()
        button4.grid()
        button5.grid()
        button7.destroy()
        button8.destroy()
        button9.destroy()
        button10.destroy()
        button15.destroy()

def exit_menu_reboot_templates(label_line_symbols, button1, button2, button3, button4, button5, button6, button7, button9, button14, button15, window):
    try:
        button7.grid()
        button8.grid()
        button9.grid()
        button10.grid()
        button6.destroy()
        button9.destroy()
        button14.destroy()
        button15.destroy()
    except (NameError, TclError, AttributeError):
        label_line_symbols.destroy()
        button7.grid()
        button8.grid()
        button9.grid()
        button10.grid()
        button6.destroy()
        button9.destroy()
        button14.destroy()
        button15.destroy()

def exit_menu_calc_sec(label_line_symbols, button1, button2, button3, button4, button5, button15, button1_calc_sec, button2_calc_sec, button3_calc_sec, button4_calc_sec, time_1, hours, hours1, minutes, minutes1, seconds, seconds1, window):
    try:
        button1.grid()
        button2.grid()
        button3.grid()
        button4.grid()
        button5.grid()
        hours.destroy()
        minutes.destroy()
        seconds.destroy()
        hours1.destroy()
        minutes1.destroy()
        seconds1.destroy()
        button1_calc_sec.destroy()
        button2_calc_sec.destroy()
        button3_calc_sec.destroy()
        button4_calc_sec.destroy()
        time_1.destroy()
        button15.destroy()
    except (NameError, TclError, AttributeError):
        label_line_symbols.destroy()
        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()
        hours.destroy()
        minutes.destroy()
        seconds.destroy()
        hours1.destroy()
        minutes1.destroy()
        seconds1.destroy()
        button1_calc_sec.destroy()
        button2_calc_sec.destroy()
        button3_calc_sec.destroy()
        button4_calc_sec.destroy()
        time_1.destroy()
        button15.destroy()

# Выход из "Питание пк"
def exit_menu(button2_main_menu_bot, label_line_symbols, button1, button2, button3, button4, button5, button15, window):
    try:
        button2_main_menu_bot.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
        label_line_symbols.destroy()
        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()
        button15.destroy()
    except (NameError, TclError, AttributeError):
        button2_main_menu_bot.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
        label_line_symbols.destroy()
        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()
        button15.destroy()

#Калькулятор секунд
def Calc_sec(label_line_symbols, button1, button2, button3, button4, button5, window):
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)

    try:
        button1.grid_remove()
        button2.grid_remove()
        button3.grid_remove()
        button4.grid_remove()
        button5.grid_remove()
    except (NameError, TclError, AttributeError):
        pass

    timer = '0'
    
    #Выключение
    def shutdown():
        timing = result()
        os.system(f'shutdown /s /t {timing} /f')
    #Перезагрузка
    def reboot():
        timing = result()
        os.system(f'shutdown /r /t {timing} /f')
    #Сон
    def hyber_pc():
        timing = result()
        os.system(f'timeout /t {timing} && rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
    #Отмена неизбежного выключения
    def cancel():
        os.system('shutdown /a')
        time_1.configure(text = f'Отмена неизбежного выключения', font = font_2)

    def enter_result(Return):
        result()

    def result():
        h1 = hours1.get()
        m1 = minutes1.get()
        s1 = seconds1.get()

        if re.search('-', h1):
            time_1.configure(text='Ошибка: Отрицательное значение в часах', font=font_2)
        elif re.search('-', m1):
            time_1.configure(text='Ошибка: Отрицательное значение в минутах', font=font_2)
        elif re.search('-', s1):
            time_1.configure(text='Ошибка: Отрицательное значение в секундах', font=font_2)
        elif h1 == '':
            time_1.configure(text='Ошибка: Пустое значение в часах', font=font_2)
        elif m1 == '':
            time_1.configure(text='Ошибка: Пустое значение в минутах', font=font_2)
        elif s1 == '':
            time_1.configure(text='Ошибка: Пустое значение в секундах', font=font_2)
        else:
            hours_in_seconds1 = int(h1) * 60
            hours_in_seconds2 = hours_in_seconds1 * 60
            minutes_in_seconds = int(m1) * 60

            final = hours_in_seconds2 + minutes_in_seconds + int(s1)
            timer = final
            time_1.configure(text=f'Результат: {timer} секунд', font=font_2)
            return timer

    button15 = ctk.CTkButton(window, text = '', command = lambda: exit_menu_calc_sec(label_line_symbols, button1, button2, button3, button4, button5, button15, button1_calc_sec, button2_calc_sec, button3_calc_sec, button4_calc_sec, time_1, hours, hours1, minutes, minutes1, seconds, seconds1, window))
    button15.grid(column = 4, row = 0, stick = 'w', pady=2, padx=2)
    button15.configure(image=photo_image_exit, compound=LEFT, width=1, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")

    #Строки | Время
    hours1 = ctk.CTkEntry(window, width = 80, font=font, justify='center', placeholder_text='0')
    minutes1 = ctk.CTkEntry(window, width = 80, font=font, justify='center', placeholder_text='0')
    seconds1 = ctk.CTkEntry(window, width = 80, font=font, justify='center', placeholder_text='0')

    hours1.grid(row = 2, column = 4, padx=90)
    minutes1.grid(row = 3, column = 4, padx=90)
    seconds1.grid(row = 4, column = 4, padx=90)

    #Текста обозначений
    hours = ctk.CTkLabel(window)
    minutes = ctk.CTkLabel(window)
    seconds = ctk.CTkLabel(window)

    hours.grid(row = 2, column = 4, stick = 'w')
    minutes.grid(row = 3, column = 4, stick = 'w')
    seconds.grid(row = 4, column = 4, stick = 'w')

    hours.configure(text = 'Часы', font=font, padx=5)
    minutes.configure(text = 'Минуты', font=font, padx=5)
    seconds.configure(text = 'Секунды', font=font, padx=5)

    #Кнопки
    button1_calc_sec = ctk.CTkButton(window, text = 'Рассчитать', width = 10, height = 38, command = result)
    button2_calc_sec = ctk.CTkButton(window, text = 'Выключить', width = 20, height = 38, command = shutdown)
    button3_calc_sec = ctk.CTkButton(window, text = 'Перезагрузить', width = 20, height = 38, command = reboot)
    button4_calc_sec = ctk.CTkButton(window, text = 'Отмена неизбежного выключения', width = 10, command = cancel)

    button1_calc_sec.grid(column = 5, row = 2, columnspan = 4, stick = 'we', padx=(0, 3))
    button2_calc_sec.grid(column = 5, row = 3, stick = 'we', padx=(0, 3))
    button3_calc_sec.grid(column = 6, row = 3, columnspan = 4, stick = 'we', padx=(0, 3))
    button4_calc_sec.grid(column = 5, row = 4, columnspan = 4, stick = 'we', padx=(0, 3))

    button1_calc_sec.configure(font=font, corner_radius=8, hover=True, hover_color='green')
    button2_calc_sec.configure(font=font, corner_radius=8, hover=True, hover_color='green')
    button3_calc_sec.configure(font=font, corner_radius=8, hover=True, hover_color='green')
    button4_calc_sec.configure(font=font, corner_radius=8, hover=True, hover_color='green')

    #Результат
    time_1 = ctk.CTkLabel(window, text='Нажмите "Рассчитать"')
    time_1.grid(row = 5, column = 4, columnspan = 4, sticky = 'wens')
    time_1.configure(font=font_2)

#Шаблоны
def templates(window_power_pc, window):
    font = ctk.CTkFont(family='Arial', size=20)

    def exit_menu_5(window_power_pc, window):
        try:
            win.deiconify()
            window.destroy()
        except NameError:
            window.deiconify()
            window.destroy()
        except TclError:
            window.deiconify()
            window.destroy()
        except AttributeError:
            window.deiconify()
            window.destroy()
    try:
        win.withdraw()
    except NameError:
        pass
    except TclError:
        pass
    except AttributeError:
        pass

    window = ctk.CTkToplevel(window_power_pc)
    window.title('Шаблоны')
    window.resizable(width=False, height=False)
    window.columnconfigure([0], weight = 1, minsize = 150)
    window.rowconfigure([0, 1, 2, 3], weight = 1, minsize = 0)
    window.protocol('WM_DELETE_WINDOW', lambda: exit_menu_5(window_power_pc, window))

    # Задаем размеры окна
    window.geometry(f"{center_x - int(window_width / 1.7)}+{center_y - int(window_height / 5)}")

    button7 = ctk.CTkButton(window, text = 'Выключить через 30 минут', width = 30, command = Power_off2, font=font, anchor='w')
    button7.grid(column = 0, row = 0, stick = 'we', pady=2)
    button7.configure(corner_radius=8, hover=True, hover_color='green', anchor="w")
    button8 = ctk.CTkButton(window, text = 'Выключить через 1 час', width = 30, command = Power_off3, font=font, anchor='w')
    button8.grid(column = 0, row = 1, stick = 'we', pady=2)
    button8.configure(corner_radius=8, hover=True, hover_color='green', anchor="w")
    button9 = ctk.CTkButton(window, text = 'Выключить через 1.5 часа', width = 30, command = Power_off4, font=font, anchor='w')
    button9.grid(column = 0, row = 2, stick = 'we', pady=2)
    button9.configure(corner_radius=8, hover=True, hover_color='green', anchor="w")
    button10 = ctk.CTkButton(window, text = 'Выключить через 2 часа', width = 30, command = Power_off5, font=font, anchor='w')
    button10.grid(column = 0, row = 3, stick = 'we', pady=2)
    button10.configure(corner_radius=8, hover=True, hover_color='green', anchor="w")

#Выключение
def Power_off1():
    os.system('shutdown /s /t 1 /f')

def Power_off2():
    os.system('shutdown /s /t 1800 /f')

def Power_off3():
    os.system('shutdown /s /t 3600 /f')

def Power_off4():
    os.system('shutdown /s /t 5400 /f')

def Power_off5():
    os.system('shutdown /s /t 7200 /f')

#Перезагрузка
def Reboot1():
    os.system('shutdown /r /t 1 /f')

def Reboot2():
    os.system('shutdown /r /t 1800 /f')

def Reboot3():
    os.system('shutdown /r /t 3600 /f')

def Reboot4():
    os.system('shutdown /r /t 5400 /f')

def Reboot5():
    os.system('shutdown /r /t 7200 /f')

#Отмена неизбежного действия
def stop():
    os.system('shutdown /a')

#Выключение пк
def Power_off(label_line_symbols, button1, button2, button3, button4, button5, window):
    font = ctk.CTkFont(family='Arial', size=20)

    try:
        button1.grid_remove()
        button2.grid_remove()
        button3.grid_remove()
        button4.grid_remove()
        button5.grid_remove()
    except (NameError, TclError, AttributeError):
        pass

    button15 = ctk.CTkButton(window, text = '', command = lambda: exit_menu_power(label_line_symbols, button1, button2, button3, button4, button5, button6, button9, button14, button15, window))
    button6 = ctk.CTkButton(window, text = 'Выключить', width = 32, command = Power_off1, font=font)
    button14 = ctk.CTkButton(window, text = 'Шаблоны', width = 32, command = lambda: templates(window_power_pc), font=font)
    button9 = ctk.CTkButton(window, text = 'Отмена неизбежного выключения', width = 32, command = stop, font=font)

    button15.grid(column = 4, row = 0, stick = 'w', pady=2, padx=2)
    button6.grid(column = 4, row = 2, stick = 'wens', pady=2, padx=2)
    button14.grid(column = 5, row = 2, stick = 'wens', pady=2, padx=2)
    button9.grid(column = 4, row = 3, columnspan = 2, stick = 'wens', pady=2, padx=2)

    button15.configure(image=photo_image_exit, compound=LEFT, width=1, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")
    button6.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button14.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button9.configure(corner_radius=8, hover=True, hover_color='green', font=font)

#Перезагрузка пк
def templates_reboot(label_line_symbols, button1, button2, button3, button4, button5, button6, button9, button14, button15, window):
    font = ctk.CTkFont(family='Arial', size=20)

    try:
        button1.grid_remove()
        button2.grid_remove()
        button3.grid_remove()
        button4.grid_remove()
        button5.grid_remove()
        button6.grid_remove()
        button9.grid_remove()
        button14.grid_remove()
    except (NameError, TclError, AttributeError):
        pass

    button15 = ctk.CTkButton(window, text = '', command = lambda: exit_menu_reboot(label_line_symbols, button1, button2, button3, button4, button5, button7, button8, button9, button10, button15, window))
    button7 = ctk.CTkButton(window, text = 'Перезагрузить через 30 минут', width = 30, command = Reboot2, font=font)
    button8 = ctk.CTkButton(window, text = 'Перезагрузить через 1 час', width = 30, command = Reboot3, font=font)
    button9 = ctk.CTkButton(window, text = 'Перезагрузить через 1.5 часа', width = 30, command = Reboot4, font=font)
    button10 = ctk.CTkButton(window, text = 'Перезагрузить через 2 часа', width = 30, command = Reboot5, font=font)

    button15.grid(column = 4, row = 0, stick = 'w', pady=2, padx=2)
    button7.grid(column = 4, row = 1, stick = 'we', pady=2, padx=2)
    button8.grid(column = 4, row = 2, stick = 'we', pady=2, padx=2)
    button9.grid(column = 4, row = 3, stick = 'we', pady=2, padx=2)
    button10.grid(column = 4, row = 4, stick = 'we', pady=2, padx=2)

    button15.configure(image=photo_image_exit, compound=LEFT, width=1, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")
    button7.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button8.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button9.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button10.configure(corner_radius=8, hover=True, hover_color='green', font=font)

def Reboot(label_line_symbols, button1, button2, button3, button4, button5, window):
    font = ctk.CTkFont(family='Arial', size=20)

    try:
        button1.grid_remove()
        button2.grid_remove()
        button3.grid_remove()
        button4.grid_remove()
        button5.grid_remove()
    except (NameError, TclError, AttributeError):
        pass

    label_line_symbols = ctk.CTkLabel(window, text = '║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║')

    button15 = ctk.CTkButton(window, text = '', command = lambda: exit_menu_power(label_line_symbols, button1, button2, button3, button4, button5, button6, button9, button14, button15, window))
    button6 = ctk.CTkButton(window, text = 'Перезагрузить', width = 32, command = Reboot1, font=font)
    button14 = ctk.CTkButton(window, text = 'Шаблоны', width = 32, command = lambda: templates_reboot(label_line_symbols, button1, button2, button3, button4, button5, button6, button9, button14, button15, window), font=font)
    button9 = ctk.CTkButton(window, text = 'Отмена неизбежной перезагрузки', width = 32, command = stop, font=font)

    label_line_symbols.grid(column = 3, row = 0, rowspan = 8, stick = 'wens', pady = 2, padx = 2)
    button15.grid(column = 4, row = 0, stick = 'w', pady=2, padx=2)
    button6.grid(column = 4, row = 2, stick = 'wens', pady=2, padx=2)
    button14.grid(column = 4, row = 3, stick = 'wens', pady=2, padx=2)
    button9.grid(column = 4, row = 4, stick = 'wens', pady=2, padx=2)

    button15.configure(image=photo_image_exit, compound=LEFT, width=1, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")
    button6.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button14.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button9.configure(corner_radius=8, hover=True, hover_color='green', font=font)

#Режим сна пк
def Sleep():
    os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

#Режим гибернации пк
def Hybernation():
    Hybernation_question = messagebox.askyesno('Уверены?', 'Вы точно хотите включить гибернацию?')
    if Hybernation_question == 'Да':
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
    elif Hybernation_question == 'Нет':
        pass

#Выход из учетной записи
def Exit_account():
    exit_question = messagebox.askyesno('Уверены?', 'Вы точно хотите выйти из системы?')
    if exit_question == 'Да':
        os.system('logoff')
        os.system('shutdown /l')
    elif exit_question == 'Нет':
        pass

def menu_pc(button2_main_menu_bot, window):
    global window_power_pc, font

    font = ctk.CTkFont(family='Arial', size=20)

    button2_main_menu_bot.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=DISABLED)

    label_line_symbols = ctk.CTkLabel(window, text = '║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║\n║')
    label_line_symbols.grid(column = 3, row = 0, rowspan = 8, stick = 'wens', pady = 2, padx = 2)

    button15 = ctk.CTkButton(window, text = '', command = lambda: exit_menu(button2_main_menu_bot, label_line_symbols, button1, button2, button3, button4, button5, button15, window))
    button1 = ctk.CTkButton(window, text = 'Меню выключения', width = 25, height = 38, command = lambda: Power_off(label_line_symbols, button1, button2, button3, button4, button5, window), font=font)
    button2 = ctk.CTkButton(window, text = 'Меню перезагрузки', width = 25, height = 38, command = lambda: Reboot(label_line_symbols, button1, button2, button3, button4, button5, window), font=font)
    button3 = ctk.CTkButton(window, text = 'Гибернация', width = 25, height = 38, command = lambda: Hybernation(), font=font)
    button4 = ctk.CTkButton(window, text = 'Выход из системы', width = 25, height = 38, command = lambda: Exit_account(), font=font)
    button5 = ctk.CTkButton(window, text = 'Задать время', width = 25, height = 29, command = lambda: Calc_sec(label_line_symbols, button1, button2, button3, button4, button5, window), font=font)

    button15.grid(column = 4, row = 0, stick = 'w', pady=2, padx=2)
    button1.grid(column = 4, row = 2, stick = 'we', pady=2, padx=2)
    button2.grid(column = 5, row = 2, stick = 'we', pady=2, padx=2)
    button3.grid(column = 4, row = 3, stick = 'we', pady=2, padx=2)
    button4.grid(column = 5, row = 3, stick = 'we', pady=2, padx=2)
    button5.grid(column = 4, row = 4, columnspan=2, stick = 'we', pady=2, padx=2)

    button15.configure(image=photo_image_exit, compound=LEFT, width=1, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")
    button1.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button2.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button3.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button4.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button5.configure(corner_radius=8, hover=True, hover_color='green', font=font)
