import customtkinter as ctk
from tkinter import ttk
from tkinter import *
import tkinter as tk
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests, win32api, threading, re, webbrowser

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

# Поиск игр
def find_game(window, window_other_menu):
    global find_game_window

    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)

    def closing_find_game():
        try:
            window_other_menu.deiconify()
            find_game_window.destroy()
        except (NameError, AttributeError):
            window.deiconify()
            find_game_window.destroy()

    try:
        window_other_menu.withdraw()
    except (NameError, AttributeError):
        window.withdraw()

    def search_game(event=None):
        search_button.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        game_name = game_name_entry.get()
        url = f"https://iwillplay.ru/games?search={quote(game_name)}"
        try:
            response = requests.get(url)
            response.raise_for_status() # проверка на ошибки
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}", parent=find_game_window)
            return
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", class_="iwp-card-body mt-3")
        game_list.delete(*game_list.get_children())
        for result in results:
            game_name = result.find("h6", class_="text-dark mb-1").text.strip()
            price = result.find("span", class_="text-dark").text.strip()
            game_link = result.find("a")
            if game_link:
                parsed_url = urlparse(game_link["href"])
                game_slug = parsed_url.path.split("/")[-1]
                game_url = f"https://iwillplay.ru/game/{game_slug}"
                game_list.insert('', 'end', values=(game_name, price, game_url))
            else:
                game_list.insert('', 'end', values=(game_name, price))
        search_button.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)

    def top_games(event=None):
        search_button.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        url = "https://iwillplay.ru/top-games"
        try:
            response = requests.get(url)
            response.raise_for_status() # проверка на ошибки
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}", parent=find_game_window)
            return
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", class_="iwp-card-body mt-3")
        game_list.delete(*game_list.get_children())
        for result in results:
            game_name = result.find("h6", class_="text-dark mb-1").text.strip()
            price = result.find("span", class_="text-dark").text.strip()
            game_link = result.find("a")
            if game_link:
                parsed_url = urlparse(game_link["href"])
                game_slug = parsed_url.path.split("/")[-1]
                game_url = f"https://iwillplay.ru/game/{game_slug}"
                game_list.insert('', 'end', values=(game_name, price, game_url))
            else:
                game_list.insert('', 'end', values=(game_name, price))
        search_button.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)

    def all_games(event=None):
        search_button.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        url = "https://iwillplay.ru/games"
        try:
            response = requests.get(url)
            response.raise_for_status() # проверка на ошибки
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}", parent=find_game_window)
            return
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", class_="iwp-card-body mt-3")
        game_list.delete(*game_list.get_children())
        for result in results:
            game_name = result.find("h6", class_="text-dark mb-1").text.strip()
            price = result.find("span", class_="text-dark").text.strip()
            game_link = result.find("a")
            if game_link:
                parsed_url = urlparse(game_link["href"])
                game_slug = parsed_url.path.split("/")[-1]
                game_url = f"https://iwillplay.ru/game/{game_slug}"
                game_list.insert('', 'end', values=(game_name, price, game_url))
            else:
                game_list.insert('', 'end', values=(game_name, price))
        search_button.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)

    def sales(event=None):
        search_button.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        url = "https://iwillplay.ru/sales"
        try:
            response = requests.get(url)
            response.raise_for_status() # проверка на ошибки
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}", parent=find_game_window)
            return
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", class_="iwp-card-body mt-3")
        game_list.delete(*game_list.get_children())
        for result in results:
            game_name = result.find("h6", class_="text-dark mb-1").text.strip()
            price = result.find("span", class_="text-dark").text.strip()
            game_link = result.find("a")
            if game_link:
                parsed_url = urlparse(game_link["href"])
                game_slug = parsed_url.path.split("/")[-1]
                game_url = f"https://iwillplay.ru/game/{game_slug}"
                game_list.insert('', 'end', values=(game_name, price, game_url))
            else:
                game_list.insert('', 'end', values=(game_name, price))
        search_button.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)

    def popular_games(event=None):
        search_button.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        url = "https://iwillplay.ru/popular"
        try:
            response = requests.get(url)
            response.raise_for_status() # проверка на ошибки
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}", parent=find_game_window)
            return
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", class_="iwp-card-body mt-3")
        game_list.delete(*game_list.get_children())
        for result in results:
            game_name = result.find("h6", class_="text-dark mb-1").text.strip()
            price = result.find("span", class_="text-dark").text.strip()
            game_link = result.find("a")
            if game_link:
                parsed_url = urlparse(game_link["href"])
                game_slug = parsed_url.path.split("/")[-1]
                game_url = f"https://iwillplay.ru/game/{game_slug}"
                game_list.insert('', 'end', values=(game_name, price, game_url))
            else:
                game_list.insert('', 'end', values=(game_name, price))
        search_button.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)

    def preorder(event=None):
        search_button.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        url = "https://iwillplay.ru/preorder"
        try:
            response = requests.get(url)
            response.raise_for_status() # проверка на ошибки
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}", parent=find_game_window)
            return
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", class_="iwp-card-body mt-3")
        game_list.delete(*game_list.get_children())
        for result in results:
            game_name = result.find("h6", class_="text-dark mb-1").text.strip()
            price = result.find("span", class_="text-dark").text.strip()
            game_link = result.find("a")
            if game_link:
                parsed_url = urlparse(game_link["href"])
                game_slug = parsed_url.path.split("/")[-1]
                game_url = f"https://iwillplay.ru/game/{game_slug}"
                game_list.insert('', 'end', values=(game_name, price, game_url))
            else:
                game_list.insert('', 'end', values=(game_name, price))
        search_button.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)

    def new_games(event=None):
        search_button.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=DISABLED, corner_radius=8, hover=True, hover_color='green', font=font)
        url = "https://iwillplay.ru/new"
        try:
            response = requests.get(url)
            response.raise_for_status() # проверка на ошибки
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}", parent=find_game_window)
            return
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", class_="iwp-card-body mt-3")
        game_list.delete(*game_list.get_children())
        for result in results:
            game_name = result.find("h6", class_="text-dark mb-1").text.strip()
            price = result.find("span", class_="text-dark").text.strip()
            game_link = result.find("a")
            if game_link:
                parsed_url = urlparse(game_link["href"])
                game_slug = parsed_url.path.split("/")[-1]
                game_url = f"https://iwillplay.ru/game/{game_slug}"
                game_list.insert('', 'end', values=(game_name, price, game_url))
            else:
                game_list.insert('', 'end', values=(game_name, price))
        search_button.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_sales.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_preorder.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_all_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_top_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_popular_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)
        button_new_games.configure(state=ACTIVE, corner_radius=8, hover=True, hover_color='green', font=font)

    def open_game(event):
        item = game_list.selection()[0]
        game_name = game_list.item(item)["values"][0]

        # заменяем пробелы на дефисы только в имени игры
        def replace_characters(game_name):
            game_name = game_name.replace("|", "-")
            game_name = game_name.replace("$", "")
            game_name = game_name.replace("+", "")
            game_name = game_name.replace(" ", "-")
            game_name = game_name.replace("’", "-")
            game_name = game_name.replace(":", "")
            game_name = game_name.replace("!", "")
            game_name = game_name.replace(".", "-")
            game_name = game_name.replace("&", "")
            game_name = game_name.replace(",", "-")
            game_name = game_name.replace("'", "-")
            game_name = game_name.replace("а", "a")
            game_name = game_name.replace("б", "b")
            game_name = game_name.replace("в", "v")
            game_name = game_name.replace("г", "g")
            game_name = game_name.replace("д", "d")
            game_name = game_name.replace("е", "e")
            game_name = game_name.replace("ё", "yo")
            game_name = game_name.replace("ж", "zh")
            game_name = game_name.replace("з", "z")
            game_name = game_name.replace("и", "i")
            game_name = game_name.replace("й", "j")
            game_name = game_name.replace("к", "k")
            game_name = game_name.replace("л", "l")
            game_name = game_name.replace("м", "m")
            game_name = game_name.replace("н", "n")
            game_name = game_name.replace("о", "o")
            game_name = game_name.replace("п", "p")
            game_name = game_name.replace("р", "r")
            game_name = game_name.replace("с", "s")
            game_name = game_name.replace("т", "t")
            game_name = game_name.replace("у", "u")
            game_name = game_name.replace("ф", "f")
            game_name = game_name.replace("х", "h")
            game_name = game_name.replace("ц", "ts")
            game_name = game_name.replace("ч", "ch")
            game_name = game_name.replace("ш", "sh")
            game_name = game_name.replace("щ", "sh")
            game_name = game_name.replace("ъ", "")
            game_name = game_name.replace("ы", "y")
            game_name = game_name.replace("ь", "")
            game_name = game_name.replace("э", "e")
            game_name = game_name.replace("ю", "yu")
            game_name = game_name.replace("я", "ya")
            game_name = game_name.replace("А", "a")
            game_name = game_name.replace("Б", "b")
            game_name = game_name.replace("В", "v")
            game_name = game_name.replace("Г", "g")
            game_name = game_name.replace("Д", "d")
            game_name = game_name.replace("Е", "e")
            game_name = game_name.replace("Ё", "yo")
            game_name = game_name.replace("Ж", "zh")
            game_name = game_name.replace("З", "z")
            game_name = game_name.replace("И", "i")
            game_name = game_name.replace("Й", "j")
            game_name = game_name.replace("К", "k")
            game_name = game_name.replace("Л", "l")
            game_name = game_name.replace("М", "m")
            game_name = game_name.replace("Н", "n")
            game_name = game_name.replace("О", "o")
            game_name = game_name.replace("П", "p")
            game_name = game_name.replace("Р", "r")
            game_name = game_name.replace("С", "s")
            game_name = game_name.replace("Т", "t")
            game_name = game_name.replace("У", "u")
            game_name = game_name.replace("Ф", "f")
            game_name = game_name.replace("Х", "h")
            game_name = game_name.replace("Ц", "ts")
            game_name = game_name.replace("Ч", "ch")
            game_name = game_name.replace("Ш", "sh")
            game_name = game_name.replace("Щ", "sh")
            game_name = game_name.replace("Ъ", "")
            game_name = game_name.replace("Ы", "j")
            game_name = game_name.replace("Ь", "")
            game_name = game_name.replace("Э", "e")
            game_name = game_name.replace("Ю", "yu")
            game_name = game_name.replace("Я", "ya")

            return game_name

        game_name = re.sub(r'-+', '-', replace_characters(game_name))

        url = f"https://iwillplay.ru/game/{game_name}"
        webbrowser.open(url)

    def search_game_return(Return):
        threading.Thread(target=search_game).start()

    def search_game_thread():
        threading.Thread(target=search_game).start()
    def top_games_thread():
        threading.Thread(target=top_games).start()
    def all_games_thread():
        threading.Thread(target=all_games).start()
    def sales_thread():
        threading.Thread(target=sales).start()
    def popular_games_thread():
        threading.Thread(target=popular_games).start()
    def preorder_thread():
        threading.Thread(target=preorder).start()
    def new_games_thread():
        threading.Thread(target=new_games).start()
    def see_more_thread():
        threading.Thread(target=see_more).start()

    # создаем окно приложения
    find_game_window = ctk.CTkToplevel(window)
    find_game_window.title("Поиск игр")
    find_game_window.columnconfigure([0], weight=1, minsize=200)
    find_game_window.rowconfigure([0, 1, 2], weight=1, minsize=0)
    find_game_window.protocol('WM_DELETE_WINDOW', lambda: closing_find_game(window))
    find_game_window.resizable(width=False, height=False)
    find_game_window.geometry(f"603x350+{center_x - int(window_width / 0.75)}+{center_y - int(window_height / 3)}")

    # создаем поле ввода
    game_name_entry = ctk.CTkEntry(find_game_window, placeholder_text="Название игры...")
    game_name_entry.configure(font=font, width=170)
    game_name_entry.place(x=215, y=5)

    # создаем надпись "при поддержке iwillplay"
    find_game_label = ctk.CTkLabel(find_game_window, text='при поддержке iwillplay')
    find_game_label.grid(row=0, column=0)
    find_game_label.place(x=406, y=5)
    find_game_label.configure(font=font_2, width=170)

    # создаем кнопку для поиска игры
    search_button = ctk.CTkButton(find_game_window, text="Поиск", command=search_game_thread)
    search_button.configure(font=font, width=170, corner_radius=8, hover=True, hover_color='green')
    search_button.place(x=25, y=5)

    # создаем кнопку для вывода топ игр за месяц
    button_top_games = ctk.CTkButton(find_game_window, text="Топ игр за месяц", command=top_games_thread)
    button_top_games.configure(font=font, width=170, corner_radius=8, hover=True, hover_color='green')
    button_top_games.place(x=25, y=45)

    # создаем кнопку для вывода всех игр
    button_all_games = ctk.CTkButton(find_game_window, text="Все игры", command=all_games_thread)
    button_all_games.configure(font=font, width=170, corner_radius=8, hover=True, hover_color='green')
    button_all_games.place(x=215, y=45)

    # создаем кнопку для вывода лучших скидок
    button_sales = ctk.CTkButton(find_game_window, text="Лучшие скидки", command=sales_thread)
    button_sales.configure(font=font, width=170, corner_radius=8, hover=True, hover_color='green')
    button_sales.place(x=406, y=45)

    # создаем кнопку для вывода популярных игр
    button_popular_games = ctk.CTkButton(find_game_window, text="Лидеры продаж", command=popular_games_thread)
    button_popular_games.configure(font=font, width=170, corner_radius=8, hover=True, hover_color='green')
    button_popular_games.place(x=25, y=85)

    # создаем кнопку для вывода предзаказа
    button_preorder = ctk.CTkButton(find_game_window, text="Предзаказ", command=preorder_thread)
    button_preorder.configure(font=font, width=170, corner_radius=8, hover=True, hover_color='green')
    button_preorder.place(x=215, y=85)

    # создаем кнопку для вывода предзаказа
    button_new_games = ctk.CTkButton(find_game_window, text="Новинки", command=new_games_thread)
    button_new_games.configure(font=font, width=170, corner_radius=8, hover=True, hover_color='green')
    button_new_games.place(x=406, y=85)

    # создаем виджет Treeview для отображения результатов
    cols = ("Название игры", "Цена")
    game_list = ttk.Treeview(find_game_window, columns=cols, show="headings")
    for col in cols:
        game_list.heading(col, text=col, anchor=tk.CENTER)
        game_list.column(col, width=100, anchor=tk.CENTER) # задаем ширину и выравнивание для колонки
    game_list.grid(row=3, column=0, columnspan=2, stick='wens')

    # привязываем обработчик события "double click" к виджету Treeview
    game_list.bind("<Double-1>", open_game)

    find_game_window.bind('<Return>', search_game_return)

    # запускаем главный цикл приложения
    find_game_window.mainloop()