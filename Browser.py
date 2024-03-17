import os, win32api, webbrowser
import customtkinter as ctk
import tkinter as tk
from tkinter import Entry, END, messagebox, Tk, Button, filedialog, Label, BooleanVar

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

def news():
    webbrowser.open('https://vk.com/feed')
def messages():
    webbrowser.open('https://vk.com/im')
def my_page():
    webbrowser.open('https://vk.com/id0')

def exit_back_browser_3(window):
    try:
        win.deiconify()
        top.destroy()
    except NameError:
        window.deiconify()
        top.destroy()
    except TclError:
        window.deiconify()
        top.destroy()

def window_vk(window):
    global font, top
    font = ctk.CTkFont(family='Arial', size=20)
    try:
        win.withdraw()
    except NameError:
        window.withdraw()
    except TclError:
        window.deiconify()

    top = ctk.CTkToplevel(window)
    top.title('VK')
    top.resizable(width=False, height=False)
    top.columnconfigure([0], weight = 1, minsize = 200)
    top.rowconfigure([0, 1, 2], weight = 1, minsize = 0)
    top.protocol('WM_DELETE_WINDOW', lambda: exit_back_browser_3(window))

    top.geometry(f"{center_x - int(window_width / 2)}+{center_y - int(window_height / 5)}")

    topbut1 = ctk.CTkButton(top, text='Новости', command=news, font=font)
    topbut1.grid(column=0, row=0, stick='we', pady=2)

    topbut2 = ctk.CTkButton(top, text='Сообщения', command=messages, font=font)
    topbut2.grid(column=0, row=1, stick='we', pady=2)

    topbut3 = ctk.CTkButton(top, text='Моя страница', command=my_page, font=font)
    topbut3.grid(column=0, row=2, stick='we', pady=2)

def youtube():
    webbrowser.open('https://youtube.com')
def vk_and_youtube():
    webbrowser.open('https://youtube.com')
    webbrowser.open('https://vk.com/id0')
def google_translate():
    webbrowser.open('https://translate.yandex.ru')
def google_disk():
    webbrowser.open('https://drive.google.com/drive')
def gmail():
    webbrowser.open('https://gmail.com')

#Менеджер сайтов
def read_site_com():
    read = open('C:\\Users\\' + os.environ['USERNAME'] + '\\Desktop\\Sites.txt', 'r')

def save_site_com():
    site = adress.get().strip()
    if not site:
        return
    with open('C:\\Users\\' + os.environ['USERNAME'] + '\\Desktop\\Sites.txt', 'r') as f:
        sites = f.read()
    if site in sites:
        messagebox.showwarning("Предупреждение", "Сайт уже добавлен в список", parent=window_browser)
        return
    with open('C:\\Users\\' + os.environ['USERNAME'] + '\\Desktop\\Sites.txt', 'a') as f:
        f.write(site + '\n')
    messagebox.showinfo("Добавление", "Сайт добавлен в список", parent=window_browser)

def sites_open(window):
    global window_browser

    font_2 = ctk.CTkFont(family='Arial', size=18)

    def clear_button():
        site_listbox.delete(0, tk.END)

    def add_site():
        site = site_entry.get().strip()
        if site:
            # получаем все значения из списка
            sites = site_listbox.get(0, tk.END)
            # проверяем наличие сайта в списке
            if site in sites:
                messagebox.showwarning("Предупреждение", "Этот сайт уже есть в списке!", parent=window_browser)
            else:
                # добавляем сайт в список
                site_listbox.insert(tk.END, site)
                site_entry.delete(0, tk.END)

    def delete_site():
        selection = site_listbox.curselection()
        if selection:
            site_listbox.delete(selection)

    def save_sites():
        filename = filename_entry.get().strip()
        if filename:
            if not filename.endswith('.txt'):
                filename += '.txt'
            with open(filename, 'w') as f:
                for site in site_listbox.get(0, tk.END):
                    f.write(site + '\n')
            filename_entry.delete(0, tk.END)
            messagebox.showinfo("Сохранение", "Список сайтов сохранен", parent=window_browser)
        else:
            messagebox.showerror("Ошибка", "Введите имя файла для сохранения", parent=window_browser)

    def load_sites():
        filename = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),))
        if filename:
            with open(filename, 'r') as f:
                site_listbox.delete(0, tk.END)
                for line in f:
                    site = line.strip()
                    if site:
                        site_listbox.insert(tk.END, site)
            messagebox.showinfo("Загрузка", "Список сайтов загружен", parent=window_browser)
        else:
            messagebox.showwarning("Предупреждение", "Не выбран файл для загрузки", parent=window_browser)

    def open_selected_site(event):
        selection = site_listbox.curselection()
        site = site_listbox.get(selection)
        webbrowser.open(site)

    directory = r'C:\Users\{}\Desktop\sites'.format(os.environ["USERNAME"])  # Абсолютный путь к директории

    def exit_back_browser_2():
        try:
            try:
                win.deiconify()
                window_browser.destroy()
            except AttributeError:
                window_browser.destroy()
        except NameError:
            try:
                window.deiconify()
                window_browser.destroy()
            except AttributeError:
                window_browser.destroy()
        except AttributeError:
            try:
                window.deiconify()
                window_browser.destroy()
            except AttributeError:
                window_browser.destroy()

    try:
        try:
            win.withdraw()
        except AttributeError:
            pass
    except NameError:
        try:
            window.withdraw()
        except AttributeError:
            pass
    except AttributeError:
        try:
            window.withdraw()
        except AttributeError:
            pass

    window_browser = ctk.CTkToplevel(window)
    window_browser.title("Менеджер сайтов")
    window_browser.resizable(width=False, height=False)
    window_browser.protocol('WM_DELETE_WINDOW', exit_back_browser_2)

    # Задаем размеры окна
    window_browser.geometry(f"{center_x - int(window_width / 1)}+{center_y - int(window_height / 2.2)}")

    # Создаем основной фрейм
    main_frame = ctk.CTkFrame(window_browser)
    main_frame.pack(fill=tk.BOTH, expand=1)

    # Создаем фрейм для ввода нового сайта
    add_frame = ctk.CTkFrame(main_frame)
    add_frame.pack(padx=10, pady=10)

    site_entry = ctk.CTkEntry(add_frame, font=('Arial', 14, 'bold'), justify='center', placeholder_text='Напишите сайт...')
    site_entry.pack(side=tk.LEFT, padx=5)

    add_button = ctk.CTkButton(add_frame, text="Добавить", command=add_site, font=font_2)
    add_button.pack(side=tk.LEFT, padx=5)

    # Создаем фрейм для списка сохраненных сайтов
    list_frame = ctk.CTkFrame(main_frame)
    list_frame.pack(fill=tk.BOTH, expand=1)

    site_listbox = tk.Listbox(list_frame, width=40, font=font_2)
    site_listbox.pack(fill=tk.BOTH, expand=1)
    site_listbox.bind('<Double-Button-1>', open_selected_site)

    # Создаем фрейм для кнопок управления списком сайтов
    button_frame = ctk.CTkFrame(list_frame)
    button_frame.pack(pady=5)

    delete_button = ctk.CTkButton(button_frame, text="Удалить", command=delete_site, font=font_2)
    delete_button.pack(side=tk.LEFT)

    clear_button = ctk.CTkButton(button_frame, text="Очистить", command=clear_button, font=font_2)
    clear_button.pack(side=tk.LEFT, padx=5)

    # Создаем фрейм для сохранения списка сайтов
    save_frame = ctk.CTkFrame(main_frame)
    save_frame.pack(padx=10, pady=10)

    filename_entry = ctk.CTkEntry(save_frame, font=('Arial', 14), justify='center', placeholder_text='Название файла...')
    filename_entry.pack(side=tk.LEFT, padx=5)

    save_button = ctk.CTkButton(save_frame, text="Сохранить", command=save_sites, font=font_2)
    save_button.pack(side=tk.LEFT, padx=5)

    # Создаем фрейм для загрузки списка сайтов
    load_frame = ctk.CTkFrame(main_frame)
    load_frame.pack(padx=10, pady=10)

    load_button = ctk.CTkButton(load_frame, text="Загрузить", command=load_sites, font=font_2)
    load_button.pack()

#Главное меню
def menu_browser(window):
    global win

    font = ctk.CTkFont(family='Arial', size=20)

    def exit_back_browser():
        try:
            window.deiconify()
            win.destroy()
        except NameError:
            window.deiconify()
            win.destroy()
        except TclError:
            window.deiconify()
            win.destroy()

    try:
        window.withdraw()
    except NameError:
        window.withdraw()
    except TclError:
        window.deiconify()

    win = ctk.CTkToplevel(window)
    win.resizable(width=False, height=False)
    win.title('Браузер')
    win.protocol('WM_DELETE_WINDOW', exit_back_browser)

    # Задаем размеры окна
    win.geometry(f"{center_x - int(window_width / 1.4)}+{center_y - int(window_height / 4.5)}")

    win.columnconfigure([0], weight=3, minsize=0)
    win.rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=3, minsize=0)

    button1 = ctk.CTkButton(win, text='Вконтакте + YouTube', command=vk_and_youtube, font=font)
    button1.grid(row=0, column=0, columnspan=2, stick='we', pady=2, padx=2)
    button2 = ctk.CTkButton(win, text='Вконтакте', command=lambda: window_vk(window), font=font)
    button2.grid(row=1, column=0, stick='we', pady=2, padx=2)
    button3 = ctk.CTkButton(win, text='YouTube', command=youtube, font=font)
    button3.grid(row=1, column=1, stick='we', pady=2, padx=2)
    button4 = ctk.CTkButton(win, text='Переводчик', command=google_translate, font=font)
    button4.grid(row=2, column=0, stick='we', pady=2, padx=2)
    button5 = ctk.CTkButton(win, text='Google Диск', command=google_disk, font=font)
    button5.grid(row=2, column=1, stick='we', pady=2, padx=2)
    button6 = ctk.CTkButton(win, text='Gmail', command=gmail, font=font)
    button6.grid(row=3, column=0, stick='we', pady=2, padx=2)
    button7 = ctk.CTkButton(win, text='Менеджер сайтов', command=lambda: sites_open(window), font=font)
    button7.grid(row=3, column=1, stick='we', pady=2, padx=2)