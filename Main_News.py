import customtkinter as ctk
from tkinter import *
import tkinter as tk
import requests, win32api, threading
from bs4 import BeautifulSoup

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

# Новости
def News(window, window_other_menu):
    global window_news
    font = ctk.CTkFont(family='Arial', size=20)
    # Определить функцию для получения новостей
    def get_news():
        nonlocal news_list
        # Очистить список новостей
        news_list.delete(0, tk.END)

        button.configure(corner_radius=8, hover=True, hover_color='green', text="Идет загрузка новостей, пожалуйста, подождите...", font=font, anchor="n", state=DISABLED)

        # URL сайта TASS, который нужно спарсить
        url = "https://tass.ru/rss/v2.xml"

        # Запросить XML содержимое сайта
        response = requests.get(url)
        xml_content = response.content

        # Разобрать XML содержимое с помощью BeautifulSoup
        soup = BeautifulSoup(xml_content, "xml")

        # Найти заголовки и ссылки всех статей
        articles = soup.find_all("item")

        # Перебрать статьи и добавить в список новостей
        for article in articles:
            headline = article.find("title").text
            link = article.find("link").text
            news_list.insert(tk.END, headline)
            news_list.insert(tk.END, "\n")
            # Сохранить ссылку на статью в список ссылок
            news_links.append(link)

        button.configure(corner_radius=8, hover=True, hover_color='green', text="Получить новости", font=font, anchor="n", state=NORMAL)

    def get_news_thread():
        threading.Thread(target=get_news).start()

    def exit_window_news():
        try:
            window_other_menu.deiconify()
            window_news.destroy()
        except NameError:
            window.deiconify()
            window_news.destroy()
        except AttributeError:
            window.deiconify()
            window_news.destroy()

    try:
        window_other_menu.withdraw()
    except:
        window.withdraw()

    window_news = ctk.CTkToplevel(window)
    window_news.resizable(width=False, height=False)
    window_news.title("Новости")
    window_news.protocol('WM_DELETE_WINDOW', exit_window_news)
    window_news.geometry(f"{center_x - int(window_width / 0.5)}+{center_y - int(window_height / 3)}")

    # Создать кнопку
    button = ctk.CTkButton(window_news, text="Получить новости", command=get_news_thread)
    button.pack(pady=5)
    button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n")

    # Создать список для отображения новостей
    news_list = tk.Listbox(window_news, width=100, height=20, font=('Arial 12'))
    news_list.pack()

    # Создать список ссылок на новости
    news_links = []

    # Создать функцию для открытия ссылки новости в браузере
    def open_link(event):
        if news_list.curselection() and news_links:
            url = news_links[news_list.curselection()[0]]
            webbrowser.open(url)

    # Привязать функцию к событию нажатия на список новостей
    news_list.bind("<Double-Button-1>", open_link)