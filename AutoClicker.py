import customtkinter as ctk
from tkinter import *
from tkinter import Entry, END, messagebox, Tk, Button, filedialog, Label, BooleanVar
import pyautogui, win32api, threading, keyboard

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

#Функция автокликера
counter = 0
dbs = 0

# Справка о баге
def bug(window):
    messagebox.showinfo("Подсказка", "Если вы хотите больше кликов чем 3 в секунду, то нажмите на кнопку автокликера несколько раз и клик суммируется.\n\nЕсли вы выберете для каждого клика свою клавишу, то при нажатии на нее, будет происходит тот клик, на который вы назначили клавишу.", parent=window)

# Справка об автокликере
def reference(window):
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)
    def see_one_win():
        try:
            one_win.deiconify()
            ref_win.destroy()
        except NameError:
            ref_win.destroy()
            window.deiconify()

    try:
        window.withdraw()
    except NameError:
        pass

    try:
        one_win.withdraw()
    except NameError:
        pass

    try:
        key_error.destroy()
    except:
        pass

    ref_win = ctk.CTkToplevel(window)
    ref_win.title("Справка")
    ref_win.resizable(width=False, height=False)
    ref_win.columnconfigure([0], weight = 1, minsize = 150)
    ref_win.rowconfigure([0], weight = 1, minsize = 0)
    ref_win.protocol('WM_DELETE_WINDOW', see_one_win)
    ref_win.geometry(f"{center_x - int(window_width / 0.8)}+{center_y - int(window_height / 6)}")

    label_ref = ctk.CTkLabel(ref_win, font=font_2, text="Если удерживать контролирующую клавишу,\nто клик будет происходить по вашему нажатию на клавишу.\nЕсли нажать клавишу 1, то автокликер будет постоянно кликать.\nЕсли нажать клавишу 2, то автокликер перестанет кликать.\nЕсли нажать клавишу 3, то автокликер завершит работу")
    label_ref.grid(column=0, row=0)

    ref_button = ctk.CTkButton(ref_win, text="Подсказка", font=font, command=lambda: bug(window))
    ref_button.grid(column=0, row=1, stick="we")

def one_click_win(window, window_other_menu):
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)
    def clicks_one():
        global dbs, counter
        four_win_button.destroy()
        five_win_button.destroy()
        value = enter_one_win.get()
        dbs += 1
        counter += 1
        label_one_win.configure(font = font_2, text = 'Вы назначили контролирующую клавишу "' + str(value) + '"\nВы нажали на кнопку запуск ' + str(counter) + ' раз\nВаш текущий клик: ' + str(dbs) + ' раз в секунду')
        enter_one_win.configure(state=DISABLED)

    def clicks_two():
        global dbs, counter
        three_win_button.destroy()
        five_win_button.destroy()
        value = enter_one_win.get()
        dbs += 2
        counter += 1
        label_one_win.configure(font = font_2, text = 'Вы назначили контролирующую клавишу "' + str(value) + '"\nВы нажали на кнопку запуск ' + str(counter) + ' раз\nВаш текущий клик: ' + str(dbs) + ' раз в секунду')
        enter_one_win.configure(state=DISABLED)

    def clicks_three():
        global dbs, counter
        three_win_button.destroy()
        four_win_button.destroy()
        value = enter_one_win.get()
        dbs += 3
        counter += 1
        label_one_win.configure(font = font_2, text = 'Вы назначили контролирующую клавишу "' + str(value) + '"\nВы нажали на кнопку запуск ' + str(counter) + ' раз\nВаш текущий клик: ' + str(dbs) + ' раз в секунду')
        enter_one_win.configure(state=DISABLED)

    # Сброс значений dbs и counter
    def reset_values_one():
        global dbs, counter
        dbs = 0
        counter = 0
        label_one_win.configure(text="Назначьте контролирующую клавишу", font=font_2)
        enter_one_win.configure(state=NORMAL)
        enter_one_win.delete(0, END)

    def type_error():
        global key_error

        def see_one_win():
            one_win.deiconify()
            key_error.destroy()

        three_win_button = ctk.CTkButton(one_win, text="1 нажатие в секунду", width=15, font=font, command=thread1)
        four_win_button = ctk.CTkButton(one_win, text="2 нажатия в секунду", width=15, font=font, command=thread2)
        five_win_button = ctk.CTkButton(one_win, text="3 нажатия в секунду", width=15, font=font, command=thread3)

        three_win_button.grid(column=0, row=3, stick="we", pady=2, padx=(2, 2))
        four_win_button.grid(column=0, row=4, stick="we", pady=2, padx=(2, 2))
        five_win_button.grid(column=0, row=5, stick="we", pady=2, padx=(2, 2))

        three_win_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
        four_win_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
        five_win_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)

        one_win.withdraw()

        value = enter_one_win.get()

        key_error = ctk.CTkToplevel(window)
        key_error.title("Ошибка!")
        key_error.resizable(width=False, height=False)
        key_error.protocol('WM_DELETE_WINDOW', see_one_win)
        key_error.geometry(f"{center_x - int(window_width / 1.13)}+{center_y - int(window_height / 8)}")

        key_error.columnconfigure([0, 1], minsize=0)
        key_error.rowconfigure([0], minsize=0)

        key_label = ctk.CTkLabel(key_error, font=font, text='Невозможно использовать клавишу "{}"'.format(value))
        key_label.grid(column=0, row=0)

        key_error_button = ctk.CTkButton(key_error, font=font, text='Как пользоваться?', command=lambda: reference(window))
        key_error_button.grid(column=0, row=1, stick='we', pady=2, padx=2)

        reset_values_one()

    def one_click():
        global value
        value = enter_one_win.get()

        if value in ["1", "2", "3", ""]:
            type_error()
        else:
            try:
                while True:
                    if keyboard.is_pressed(value):
                        pyautogui.click()
                    elif keyboard.is_pressed("1"):
                        while True:
                            pyautogui.click()
                            if keyboard.is_pressed("2"):
                                break
                            elif keyboard.is_pressed("3"):
                                reset_values_one()
                                try:
                                    window_other_menu.deiconify()
                                    one_win.destroy()
                                    return
                                except AttributeError:
                                    window.deiconify()
                                    one_win.destroy()
                    elif keyboard.is_pressed("3"):
                        reset_values_one()
                        try:
                            window_other_menu.deiconify()
                            one_win.destroy()
                            return
                        except AttributeError:
                            window.deiconify()
                            one_win.destroy()
            except ValueError:
                one_win.withdraw()
                messagebox.showerror("Ошибка", "Введите пожалуйста любой символ", parent=window)
                one_win.deiconify()

    def two_click():
        global value
        value = enter_one_win.get()

        if value in ["1", "2", "3", ""]:
            type_error()
        else:
            try:
                while True:
                    if keyboard.is_pressed(value):
                        pyautogui.doubleClick()
                    elif keyboard.is_pressed("1"):
                        while True:
                            pyautogui.doubleClick()
                            if keyboard.is_pressed("2"):
                                break
                            elif keyboard.is_pressed("3"):
                                reset_values_one()
                                try:
                                    window_other_menu.deiconify()
                                    one_win.destroy()
                                    return
                                except AttributeError:
                                    window.deiconify()
                                    one_win.destroy()
                    elif keyboard.is_pressed("3"):
                        reset_values_one()
                        try:
                            window_other_menu.deiconify()
                            one_win.destroy()
                            return
                        except AttributeError:
                            window.deiconify()
                            one_win.destroy()
            except ValueError:
                one_win.withdraw()
                messagebox.showerror("Ошибка", "Введите пожалуйста любой символ", parent=window)
                one_win.deiconify()

    def three_click():
        global value
        value = enter_one_win.get()

        if value in ["1", "2", "3", ""]:
            type_error()
        else:
            try:
                while True:
                    if keyboard.is_pressed(value):
                        pyautogui.click()
                    elif keyboard.is_pressed("1"):
                        while True:
                            pyautogui.tripleClick()
                            if keyboard.is_pressed("2"):
                                break
                            elif keyboard.is_pressed("3"):
                                reset_values_one()
                                try:
                                    window_other_menu.deiconify()
                                    one_win.destroy()
                                    return
                                except AttributeError:
                                    window.deiconify()
                                    one_win.destroy()
                    elif keyboard.is_pressed("3"):
                        reset_values_one()
                        try:
                            window_other_menu.deiconify()
                            one_win.destroy()
                            return
                        except AttributeError:
                            window.deiconify()
                            one_win.destroy()
            except ValueError:
                one_win.withdraw()
                messagebox.showerror("Ошибка", "Введите пожалуйста любой символ", parent=window)
                one_win.deiconify()

    def one_win_close_window():
        if enter_one_win.get() and three_win_button and keyboard != '3':
            one_win.withdraw()
            messagebox.showerror("Ошибка", 'Выйдите из цикла нажав на цифру "3"\nЕсли вы не нажали клавишу запуска, то уберите символ из поля ввода\nПодробнее в "Справка"', parent=window)
            one_win.deiconify()
        elif enter_one_win.get() and four_win_button and keyboard != '3':
            one_win.withdraw()
            messagebox.showerror("Ошибка", 'Выйдите из цикла нажав на цифру "3"\nЕсли вы не нажали клавишу запуска, то уберите символ из поля ввода\nПодробнее в "Справка"', parent=window)
            one_win.deiconify()
        elif enter_one_win.get() and five_win_button and keyboard != '3':
            one_win.withdraw()
            messagebox.showerror("Ошибка", 'Выйдите из цикла нажав на цифру "3"\nЕсли вы не нажали клавишу запуска, то уберите символ из поля ввода\nПодробнее в "Справка"', parent=window)
            one_win.deiconify()
        else:
            try:
                window_other_menu.deiconify()
                one_win.destroy()
            except NameError:
                window.deiconify()
                one_win.destroy()
            except AttributeError:
                window.deiconify()
                one_win.destroy()
    try:
        status_win.withdraw()
        window.withdraw()
    except NameError:
        pass

    def all_clicks_one():
        clicks_one()
        one_click()
    def all_clicks_two():
        clicks_two()
        two_click()
    def all_clicks_three():
        clicks_three()
        three_click()

    def thread1():
        threading.Thread(target=all_clicks_one).start()
    def thread2():
        threading.Thread(target=all_clicks_two).start()
    def thread3():
        threading.Thread(target=all_clicks_three).start()

    def validate_entry(text):
        return len(text) <= 1

    try:
        window_other_menu.withdraw()
    except NameError:
        pass
    except AttributeError:
        pass

    try:
        window.withdraw()
    except NameError:
        pass

    global one_win

    one_win = ctk.CTkToplevel(window)
    one_win.title("Автокликер")
    one_win.resizable(width=False, height=False)
    one_win.protocol('WM_DELETE_WINDOW', one_win_close_window)
    one_win.columnconfigure([0,1], weight=15, minsize=0)
    one_win.rowconfigure([0,1,2], weight=15, minsize=0)
    one_win.geometry(f"{center_x - int(window_width / 1.2)}+{center_y - int(window_height / 4.5)}")

    label_one_win = ctk.CTkLabel(one_win, text="Назначьте контролирующую клавишу", font=font_2)
    label_one_win.grid(column=0, row=0)

    enter_one_win = ctk.CTkEntry(one_win, font=font_2, justify='center', validate="key", width=200, placeholder_text='Введите символ...')
    enter_one_win.grid(column=0, row=1)
    vcmd = (one_win.register(validate_entry), '%P')
    enter_one_win.configure(validatecommand=vcmd)

    two_win_button = ctk.CTkButton(one_win, text="Справка", width=15, font=font, command=lambda: reference(window))
    three_win_button = ctk.CTkButton(one_win, text="1 нажатие в секунду", width=15, font=font, command=thread1)
    four_win_button = ctk.CTkButton(one_win, text="2 нажатия в секунду", width=15, font=font, command=thread2)
    five_win_button = ctk.CTkButton(one_win, text="3 нажатия в секунду", width=15, font=font, command=thread3)

    two_win_button.grid(column=0, row=6, stick="we", pady=2, padx=(2, 2))
    three_win_button.grid(column=0, row=3, stick="we", pady=2, padx=(2, 2))
    four_win_button.grid(column=0, row=4, stick="we", pady=2, padx=(2, 2))
    five_win_button.grid(column=0, row=5, stick="we", pady=2, padx=(2, 2))

    two_win_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
    three_win_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
    four_win_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
    five_win_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)