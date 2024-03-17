import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from tkinter import Entry, END, messagebox, Tk, Button, filedialog, Label, BooleanVar
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

words = ["яблоко", "банан", "апельсин", "груша", "персик", "ананас", "слива", "виноград", "манго", "киви", "абрикос",
"мандарин", "грейпфрут", "лайм", "лайчи", "нектарин", "папайя", "слизень", "бамбук", "коала", "бублик", "вертолет",
"корабль", "самолет", "карандаш", "книга", "микроскоп", "компьютер", "автомобиль", "оладушек", "домино", "луна",
"треугольник", "железо", "дракон", "солнце", "радуга", "пароход", "водопад", "гитара", "виолончель", "саксофон",
"горшок", "гамак", "воздушный шар", "крокодил", "стекло", "молоток", "микрофон", "снеговик", "кашалот", "креветка",
"барсук", "краб", "сардинка", "коньки", "кактус", "каштан", "фотоаппарат", "рюкзак", "канат", "ракета", "самовар",
"кокос", "камера", "космонавт", "бомба", "банк", "бухта", "ворона", "гусеница", "дельфин", "дерево", "диск", "ежик",
"жираф", "змея", "зонт", "иголка", "кабан", "календарь", "капуста", "клавиатура", "клюшка", "колесо", "колонка",
"комод", "коробка", "косичка", "лампочка", "лифт", "лужа", "лук", "маяк", "мармелад", "мартышка", "метла", "муравей",
"музыка", "мыло", "мышь", "ножницы", "носок", "ноутбук", "олень", "орел", "паук", "палец", "парашют", "педаль", "печенье",
"пилот", "пистолет", "пицца", "подушка", "поезд", "попугай", "пружина", "пылесос", "радио", "резинка", "розетка", "рубашка",
"рыба", "салат", "салют", "самокат", "макарон", "картина", "молоко", "флейта", "галстук", "шоколад", "кошелек", "метро", 
"бейсбол", "фонарь", "бутылка", "зонтик", "пианино", "камень", "ковер", "кровать", "душ", "кольцо", "картошка", "пыль", 
"кресло", "диван", "зеркало", "конфета", "мороженое", "лимонад", "рыцарь", "бинокль", "клавиша", "лента", "телефон", 
"мыльница", "шарф", "перо", "медведь", "сковорода", "вилка", "ложка", "нож", "пила", "стул", "табурет", "ковш", "карантин", 
"горшочек", "крючок", "веревка", "костюм", "трусы", "галочка", "крючок", "шторы", "часы", "шампунь", "ластик", "бумага", 
"чашка", "сумка", "банка", "дверь", "окно", "полотенце", "море", "небо", "трава", "солнце", "медаль", "котелок", "футбол", 
"змейка", "кошка", "попкорн", "скрипка", "муха", "свеча", "песок", "майка", "бокал", "горшок", "сумочка", "курица", "книжка", 
"ручка", "свитер", "забор", "ваза", "морковь", "динозавр", "бегемот", "овца", "орех", "тапки", "кот", "пес", "крокус", "мак", 
"краски", "кисть", "метка", "листок", "ручей", "океан", "ящик", "роза", "бабочка", "змея", "деревня", "молоток", "жаба", "вода", 
"мука", "торт", "сок", "пиво", "аптечка", "щетка", "морс", "капли", "принцесса", "космос", "футляр", "персона", "кондиционер", 
"вазон", "чехол", "велосипед", "плащ", "сапоги", "куртка", "шапка", "воздух", "золото", "метеорит", "радость", "гитарист", "конь"]

def delete_symbols():
    enter.delete(0, END)

# Игра виселица
def update_remaining_label():
    global remaining_label
    remaining = len([c for c in secret_word if c not in guessed_letters])
    remaining_label.configure(text=f"Осталось неразгаданных букв: {remaining}")

def update_word_label():
    global word_label
    word_state = "".join([c if c in guessed_letters else "_" for c in secret_word])
    word_label.configure(text=f"Слово: {word_state}")

def update_attempts_label():
    global attempts_label
    attempts_label.configure(text=f"Осталось попыток: {num_attempts}")

def guess_letter(window):
    global guessed_letters, num_attempts, guess_letter, letter
    letter = letter_entry.get().lower()
    if letter in guessed_letters:
        letter_entry.delete(0, END)
        show_message("Вы уже угадали эту букву. Попробуйте другую.", window)
    elif letter in secret_word:
        guessed_letters.add(letter)
        update_word_label()
        update_remaining_label()
        if all([c in guessed_letters for c in secret_word]):
            show_message(f"Поздравляем! Вы угадали слово '{secret_word}'!", window)
            new_game()
    else:
        num_attempts -= 1
        update_attempts_label()
        if num_attempts == 0:
            show_message(f"Извините, вы израсходовали все попытки. Слово было '{secret_word}'. Удачи в следующий раз!")
            new_game()
    letter_entry.delete(0, tk.END)
    letter_entry.focus_set()

def show_message(message, window):
    tk.messagebox.showinfo("Игра 'Виселица'", message, parent=window)

def get_secret_word():
    return random.choice(words)

def new_game():
    global secret_word, guessed_letters, num_attempts
    secret_word = get_secret_word()
    guessed_letters = set()
    num_attempts = 15
    update_word_label()
    update_remaining_label()
    update_attempts_label()

def create_widgets(window, window_game_menu):
    global word_label, attempts_label, letter_entry, new_game, remaining_label, window_widgets_viselica
    
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)

    def exit_back_viselica_menu():
        try:
            window_game_menu.deiconify()
            window_widgets_viselica.destroy()
        except NameError:
            window.deiconify()
            window_widgets_viselica.destroy()
        except AttributeError:
            window.deiconify()
            window_widgets_viselica.destroy()

    try:
        window_game_menu.withdraw()
    except NameError:
        window.withdraw()
    except AttributeError:
        window.withdraw()

    window_widgets_viselica = ctk.CTkToplevel(window)
    window_widgets_viselica.title('Отгадай слово')
    window_widgets_viselica.resizable(width=False, height=False)
    window_widgets_viselica.protocol('WM_DELETE_WINDOW', exit_back_viselica_menu)

    window_widgets_viselica.geometry(f"{center_x - int(window_width / 1)}+{center_y - int(window_height / 4)}")

    # Отображение загаданного слова
    word_label = ctk.CTkLabel(window_widgets_viselica, text=" ", font=font_2)
    word_label.grid(row=0, column=0)

    # Создание label для отображения количества неразгаданных букв
    remaining_label = ctk.CTkLabel(window_widgets_viselica, text="Осталось неразгаданных букв: 0", font=font_2)
    remaining_label.grid(row=0, column=1)

    def validate_entry(text):
        return len(text) <= 1

    # Поле для ввода буквы
    letter_entry = ctk.CTkEntry(window_widgets_viselica, font=font_2, placeholder_text="Пишите здесь...", validate="key")
    letter_entry.grid(row=1, column=0, padx=10, pady=10)
    letter_entry.focus()
    vcmd = (window_widgets_viselica.register(validate_entry), '%P')
    letter_entry.configure(validatecommand=vcmd)

    # Проверка символа в поле ввода и ограничение поля ввода до 1 символа
    def guess_letter_2():
        letter = letter_entry.get()
        if len(letter) == 0:
            guess_letter(window)
            letter_entry.delete(0, END)
            messagebox.showerror("Ошибка", "Нельзя проверить букву, которой нет в поле ввода", parent=window)
            window_widgets_viselica.focus_force()
            letter_entry.focus()
        elif len(letter) == 1:
            guess_letter(window)
            letter_entry.insert(len(letter_entry.get()) // 2, letter)
            letter_entry.delete(0, END)

    def guess_letter_enter(Return):
        letter = letter_entry.get()
        if len(letter) == 0:
            guess_letter(window)
            letter_entry.delete(0, END)
            messagebox.showerror("Ошибка", "Нельзя проверить букву, которой нет в поле ввода", parent=window)
            window_widgets_viselica.focus_force()
            letter_entry.focus()
        elif len(letter) == 1:
            guess_letter(window)
            letter_entry.insert(len(letter_entry.get()) // 2, letter)
            letter_entry.delete(0, END)

    guess_button = ctk.CTkButton(window_widgets_viselica, text="Угадать", command=guess_letter_2)
    guess_button.grid(row=1, column=1, padx=10, pady=10)
    guess_button.configure(corner_radius=8, hover=True, hover_color='green', font=font)

    # Отображение оставшихся попыток
    attempts_label = ctk.CTkLabel(window_widgets_viselica, font=font_2)
    attempts_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Кнопка для начала новой игры
    new_game_button = ctk.CTkButton(window_widgets_viselica, text="Новая игра", command=new_game)
    new_game_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    new_game_button.configure(corner_radius=8, hover=True, hover_color='green', font=font)

    # Создание новой игры
    new_game()

    window_widgets_viselica.bind("<Return>", guess_letter_enter)