from tkinter import *
import tkinter.simpledialog
import tkinter as tk
from tkinter import ttk
from tkinter import Entry, END, messagebox, Tk, Button, filedialog, Label, BooleanVar
import customtkinter as ctk
import os, sys, configparser, shelve, win32api, threading, pyaudio, time, random, json
from vosk import Model, KaldiRecognizer
import speech_recognition as sr

from Voice_Commands import handle_user_message
from Speak import va_speak
from Main_Personalization import personalization
from AutoLaunch import new_win
from Personal_Path_WebSite import menu_path
from State_Panel_Word import check_word_panel

greetings = ["Привет!", "Здравствуйте!", "Рада слышать вас!", "Добрый день!", "Приветствую вас!", "Здравствуйте, как могу помочь?", "Приветствую!", "Доброго времени суток!", "Привет, как дела?",
"Рада вас слышать!", "Здравствуйте, чем могу быть полезна?", "Приветствую вас снова!", "Здравствуйте, как я могу вам помочь сегодня?", "Рада слышать вас снова!", 
"Привет, как я могу быть полезна?", "Здравствуйте, как проходит ваш день?", "Рада встрече с вами!", "Приветствую вас с радостью!", "Здравствуйте, как ваше настроение?",
"Привет, какие планы на сегодня?", "Здравствуйте, как прошел день?", "Рада снова вас слышать!", "Доброго времени суток! Чем могу помочь?"]

goodbyes = ["До свидания!", "Пока!", "Удачного дня!", "Всего хорошего!", "До скорой встречи!",
"Удачи!", "Хорошего времени!", "До встречи!","До свидания! Было приятно помочь!","Пока-пока!","Прощайте!","Хорошего настроения!","Увидимся!","Желаю успехов!","До следующего раза!", 
"До свидания! Будьте здоровы!","Приятно было поговорить!","Всего доброго!","Успехов в делах!","До скорого!","Желаю всего наилучшего!","Счастливого дня!",
"Прощай! Береги себя!", "Удачи во всём!", "До встречи! Пишите, если что!", "Желаю хорошего настроения!", "Успешного завершения дел!"]

documents_path = os.path.expanduser("~")
bot_helper_path = os.path.join(documents_path, "Documents", "BotHelper")
CONFIG_FILE = os.path.join(bot_helper_path, "config.ini")
SAMPLE_RATE = 44100
CHUNK_SIZE = 48000
extra_wait_time = 2
AUTO_RUN_MODEL = False
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
selected_model = config.get('Settings', 'SelectedModel', fallback='vosk-model-small-ru-0.4')
EXTRA_WAIT_TIME = config.getfloat('Settings', 'ExtraWaitTime', fallback=2.0)
selected_recognizer = 'Vosk'
running_flag = threading.Event()

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

if not config.has_section('WebSearch'):
    config.add_section('WebSearch')
    config.set('WebSearch', 'web_search', 'True')
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

web_search = config.getboolean('WebSearch', 'web_search')

recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Создать папку "BotHelper", если она не существует
if not os.path.exists(bot_helper_path):
    os.makedirs(bot_helper_path)

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

# Функции настроек бота
# Загрузка настроек программы
def load_config():
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)
    global SAMPLE_RATE, extra_wait_time, AUTO_RUN_MODEL, selected_model, selected_recognizer, noise_reduction_level

    program_files_folder = os.path.dirname(sys.executable)
    bot_helper_folder = os.path.join(program_files_folder, "Бот-помощник")

    documents_folder = os.path.expanduser("~\\Documents")
    bot_config_folder = os.path.join(documents_folder, "BotHelper")
    os.makedirs(bot_config_folder, exist_ok=True)

    config_file_path = os.path.join(bot_config_folder, "config.ini")

    if not os.path.isfile(CONFIG_FILE):
        config.add_section('Settings')
        config.set('Settings', 'SelectedModel', selected_model)
        config.set('Settings', 'ExtraWaitTime', str(extra_wait_time))
        config.set('Settings', 'SampleRate', str(SAMPLE_RATE))
        config.set('Settings', 'AutoRunModel', str(AUTO_RUN_MODEL))
        config.set('Settings', 'SelectedRecognizer', selected_recognizer)
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(CONFIG_FILE)

    try:
        AUTO_RUN_MODEL = config.getboolean('Settings', 'AutoRunModel')
    except (configparser.NoOptionError, ValueError):
        AUTO_RUN_MODEL = False

    if not config.has_section('Settings'):
        config.add_section('Settings')

    if not config.has_option('Settings', 'SelectedModel'):
        config.set('Settings', 'SelectedModel', 'vosk-model-small-ru-0.4')

    if not config.has_option('Settings', 'ExtraWaitTime'):
        config.set('Settings', 'ExtraWaitTime', '2')

    if not config.has_option('Settings', 'SampleRate'):
        config.set('Settings', 'SampleRate', '44100')

    if not config.has_option('Settings', 'AutoRunModel'):
        config.set('Settings', 'AutoRunModel', 'False')

    if not config.has_option('Settings', 'SelectedRecognizer'):
        config.set('Settings', 'SelectedRecognizer', 'Vosk')

    if not config.has_option('Settings', 'web_search'):
        config.set('Settings', 'web_search', 'True')

    web_search = config.getboolean('Settings', 'web_search')
    SAMPLE_RATE = config.getint('Settings', 'SampleRate')
    extra_wait_time = config.getfloat('Settings', 'ExtraWaitTime')
    selected_recognizer = config.get('Settings', 'SelectedRecognizer')
    
    try:
        AUTO_RUN_MODEL = config.getboolean('Settings', 'AutoRunModel')
    except (configparser.NoOptionError, ValueError):
        AUTO_RUN_MODEL = False

def save_web_search_setting(web_search_state):
    config.set('Settings', 'web_search', str(web_search_state))
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def ChatGPT_setting(window, window_setting_bot):
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)
    global selected_model, SAMPLE_RATE, extra_wait_time, AUTO_RUN_MODEL, selected_recognizer, model_Label, wait_Label, sample_Label, auto_run_Label, web_search
    load_config()

    web_search = config.getboolean('Settings', 'web_search', fallback=True)

    def ChatGPT_setting_exit():
        try:
            window_setting_bot.deiconify()
            window_setting_ChatGPT.destroy()
        except:
            window.deiconify()
            window_setting_ChatGPT.destroy()

    try:
        window_setting_bot.withdraw()
    except:
        pass

    def save_settings():
        global selected_model, selected_recognizer

        def save_selected_model(model_path):
            config.set('Settings', 'SelectedModel', model_path)
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)

        def save_extra_wait_time(wait_time):
            config.set('Settings', 'ExtraWaitTime', str(int(wait_time)))
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)

        def save_sample_rate(sample_rate):
            config.set('Settings', 'SampleRate', str(int(sample_rate)))
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)

        def save_auto_run(auto_run):
            config.set('Settings', 'AutoRunModel', str(auto_run))
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)

        def save_recognizer(recognizer_choice):
            config.set('Settings', 'SelectedRecognizer', recognizer_choice)
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)

        web_search = web_search_var.get() == "Да"
        save_web_search_setting(web_search)

        try:
            selected_model = "vosk-model-small-ru-0.4" if selected_model_var.get() == "Маленькая модель" else "vosk-model-ru-0.10"
            wait_time = wait_time_var.get()
            sample_rate = sample_rate_var.get()
            auto_run = auto_run_var.get()
            selected_recognizer = recognizer_var.get()

            if not wait_time:
                wait_time = 2

            if not sample_rate:
                sample_rate = 44100

            try:
                wait_time_float = float(wait_time)
            except ValueError:
                wait_time_float = None

            try:
                sample_rate_float = float(sample_rate)
            except ValueError:
                sample_rate_float = None

            if wait_time_float is None:
                messagebox.showerror("Ошибка", "Неверный ввод. Время ожидания должно быть числом.")
                return

            if sample_rate_float is None:
                messagebox.showerror("Ошибка", "Неверный ввод. Частота микрофона должна быть числом.")
                return

            config.set('Settings', 'SelectedModel', selected_model)
            config.set('Settings', 'ExtraWaitTime', str(int(wait_time_float)))
            config.set('Settings', 'SampleRate', str(int(sample_rate_float)))
            config.set('Settings', 'AutoRunModel', str(auto_run == "Да"))
            config.set('Settings', 'SelectedRecognizer', selected_recognizer)

            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)

            messagebox.showinfo("Настройки сохранены.", f"Выбран распознаватель речи: {selected_recognizer}.\nВыбрана модель: {selected_model}\nВыбрано время ожидания: {wait_time}\nВыбрана частота микрофона: {sample_rate}\nАвтоматический запуск ассистента: {auto_run}\n\nПерезапустите программу для применения настроек.\n", parent=window_setting_ChatGPT) #Поиск информации в интернете: {web_search}

            # Обновление глобальной переменной
            AUTO_RUN_MODEL = auto_run_var.get() == "Да"

            save_selected_model(selected_model)
            save_extra_wait_time(wait_time_float)
            save_sample_rate(sample_rate_float)
            save_auto_run(auto_run == "Да")
            save_recognizer(selected_recognizer)

        except KeyError:
            selected_model_text = 'Неизвестная модель'

    window_setting_ChatGPT = ctk.CTkToplevel(window)
    window_setting_ChatGPT.resizable(width=False, height=False)
    window_setting_ChatGPT.title('Настройки ассистента')
    window_setting_ChatGPT.protocol('WM_DELETE_WINDOW', ChatGPT_setting_exit)
    window_setting_ChatGPT.geometry(f"{center_x - int(window_width / 1)}+{center_y - int(window_height / 8)}")

    selected_model_var = tk.StringVar(value='Маленькая модель' if selected_model == 'vosk-model-small-ru-0.4' else 'Большая модель')
    sample_rate_var = tk.StringVar(value=str(SAMPLE_RATE))
    wait_time_var = tk.StringVar(value=str(EXTRA_WAIT_TIME))
    auto_run_var = tk.StringVar(value="Да" if AUTO_RUN_MODEL else "Нет")
    recognizer_var = tk.StringVar(value=selected_recognizer)
    web_search_var = tk.StringVar(value="Да" if web_search else "Нет")

    recognizer_Label = ctk.CTkLabel(window_setting_ChatGPT, text="Выберите распознаватель:", font=font).grid(row=0, column=0, sticky="w")
    recognizer_choices = ['Vosk', 'Google']
    recognizer_var.set(selected_recognizer)
    recognizer_dropdown = ttk.Combobox(window_setting_ChatGPT, textvariable=recognizer_var, values=recognizer_choices)
    recognizer_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    model_Label = ctk.CTkLabel(window_setting_ChatGPT, text="Выберите модель распознавания:", font=font).grid(row=1, column=0, sticky="w")
    model_choices = ['Большая модель', 'Маленькая модель']
    model_choices_dict = {'Большая модель': 'vosk-model-ru-0.10', 'Маленькая модель': 'vosk-model-small-ru-0.4'}
    model_dropdown = ttk.Combobox(window_setting_ChatGPT, textvariable=selected_model_var, values=model_choices)
    model_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    wait_Label = ctk.CTkLabel(window_setting_ChatGPT, text="Время ожидания после речи (сек):", font=font).grid(row=2, column=0, sticky="w")
    wait_time_values = ['0', '1', '2', '3', '4', '5']
    wait_time_combobox = ttk.Combobox(window_setting_ChatGPT, textvariable=wait_time_var, values=wait_time_values)
    wait_time_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    sample_Label = ctk.CTkLabel(window_setting_ChatGPT, text="Выберите частоту микрофона:", font=font).grid(row=3, column=0, sticky="w")
    sample_rate_choices = ['44100', '48000', '96000', '192000']
    sample_rate_var.set(str(config.getint('Settings', 'SampleRate')))
    sample_rate_dropdown = ttk.Combobox(window_setting_ChatGPT, textvariable=sample_rate_var, values=sample_rate_choices)
    sample_rate_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    auto_run_Label = ctk.CTkLabel(window_setting_ChatGPT, text="Автоматический запуск ассистента:", font=font).grid(row=4, column=0, sticky="w")
    auto_run_choices = ['Да', 'Нет']
    auto_run_choices_dict = {'Да': 'True', 'Нет': 'False'}
    auto_run_dropdown = ttk.Combobox(window_setting_ChatGPT, textvariable=auto_run_var, values=auto_run_choices)
    auto_run_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # web_search_label = ctk.CTkLabel(window_setting_ChatGPT, text="Поиск информации в Интернете:", font=font).grid(row=5, column=0, sticky="w")
    # web_search_choices = ['Да', 'Нет']
    # web_search_dropdown = ttk.Combobox(window_setting_ChatGPT, textvariable=web_search_var, values=web_search_choices)
    # web_search_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    button_setting_ChatGPT = ctk.CTkButton(window_setting_ChatGPT, text="Сохранить настройки", command=save_settings)
    button_setting_ChatGPT.grid(row=6, columnspan=2, pady=10)
    button_setting_ChatGPT.configure(corner_radius=8, hover=True, hover_color='green', font=font)

    # Начальные значения переменных на основе текущих настроек
    selected_model_var.set('Маленькая модель' if selected_model == 'vosk-model-small-ru-0.4' else 'Большая модель')
    wait_time_combobox.set(extra_wait_time)
    sample_rate_dropdown.set(SAMPLE_RATE)
    auto_run_dropdown.set("Да" if AUTO_RUN_MODEL else "Нет")

# Загрузить выбранный распознаватель речи
def load_selected_recognizer():
    try:
        return config.get('Settings', 'SelectedRecognizer')
    except (configparser.NoOptionError, ValueError):
        return 'Vosk'

# Распознаватель речи от Google
def recognize_google(audio, language="ru-RU"):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU").lower()
        return text
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        va_speak(f'Ошибка при подключении к распознаванию речи от гугл. Проверьте подключение к интернету или используйте другую модель распознавания речи')

def select_model():
    load_config()

def set_extra_wait_time():
    load_config()

def window_upper(window):
    global topmost
    topmost = BooleanVar()
    update_checkbox_state(window)

# Выход в меню главное бота
def exit_menu(window):
    try:
        window.deiconify()
        window_setting_bot.destroy()
    except (NameError, AttributeError):
        window.deiconify()
        window_setting_bot.destroy()

# Сохранить состояние чекбокса
def save_checkbox_state(state):
    # Создать путь к файлу базы данных в папке "BotHelper"
    db_path = os.path.join(bot_helper_path, 'checkbox_state.db')
    # Открыть или создать файл базы данных
    with shelve.open(db_path) as db:
        # Сохранить состояние чекбокса в базе данных
        db["checkbox_state"] = state

# Загрузить состояние чекбокса
def load_checkbox_state():
    try:
        # Создать путь к файлу базы данных в папке "BotHelper"
        db_path = os.path.join(bot_helper_path, 'checkbox_state.db')
        # Открыть или создать файл базы данных
        with shelve.open(db_path) as db:
            # Загрузить состояние чекбокса из базы данных
            return db.get("checkbox_state")
    except KeyError:
        return None

# Обновить состояние чекбокса
def update_checkbox_state(window):
    # Загрузить состояние чекбокса из базы данных
    saved_state = load_checkbox_state()
    if saved_state is not None:
        topmost.set(saved_state)
        # Установить атрибут "-topmost" для главного окна в зависимости от состояния чекбокса
        window.attributes("-topmost", saved_state)

# Поверх всех окон
def on_top(window):
    # Функция, которая вызывается при изменении состояния чекбокса
    state = topmost.get()
    save_checkbox_state(state)
    
    # Установить атрибут "-topmost" для главного окна
    window.attributes("-topmost", state)

def limit_text_length(text, max_length=46):
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    else:
        return text

def on_button_start_click(user_va_speak):
    global running_flag

    user_va_speak.configure(text='Ожидайте...')

    font = ctk.CTkFont(family='Arial', size=20)

    running_flag.set()

    button8.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=DISABLED)
    button9.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)
    stream.start_stream()

    threading.Thread(target=start_ChatGPT, args=(stream, user_va_speak, va_speak, selected_recognizer, Model, KaldiRecognizer)).start()
    check_word_panel(user_va_speak, selected_recognizer)

    user_va_speak.configure(text='Скажите "Привет Саша"...')

def on_button_stop_click(user_va_speak):
    global running_flag

    font = ctk.CTkFont(family='Arial', size=20)
    
    running_flag.clear()
    
    user_va_speak.configure(text='Для общения включите AI')
    
    button8.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
    button9.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=DISABLED)
    
    check_word_panel(user_va_speak, selected_recognizer)

    off_ChatGPT(config, selected_recognizer, user_va_speak, va_speak)
    return

def listen_for_input(stream, recognizer, user_va_speak):
    global chat_activated, running_flag

    try:
        remove_old_wav_files()
    except:
        pass

    user_va_speak.configure(text='Ожидайте...')

    greeting = random.choice(greetings)
    va_speak(greeting)

    while running_flag.is_set():
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        
        selected_recognizer = load_selected_recognizer()

        user_va_speak.configure(text='Говорите...')
        
        if selected_recognizer == 'Vosk':
            if (recognizer.AcceptWaveform(data)) and (len(data) > 0):
                answer = json.loads(recognizer.Result())
                if answer['text']:
                    last_time_spoken = time.time()
                    user_input = answer['text']

                    user_va_speak.configure(text=limit_text_length(f'Вы сказали: {user_input}'))

                    try:
                        if any(phrase in user_input.lower() for phrase in ["пока саша", "пока саш", "пк саша", "пк саш", "саша пока", "саш пока", "саша пк", 
                                                                           "пока сань", "пока саня", "пк сань", "пк саня", "саня пока", "сань пока", "саня пк",
                                                                           "пока сша", "пк сша", "сша пока", "сша пока", "сша пк", "пока сошел", "пока сошёл", "сошел пока", "сошёл пока"]):
                            user_va_speak.configure(text='Ожидайте...')
                            chat_activated = False
                            goodbye = random.choice(goodbyes)
                            va_speak(goodbye)
                            remove_old_wav_files()
                            wait_response(stream, recognizer)
                            user_va_speak.configure(text='Скажите "Привет Саша"...')
                            return
                        else:
                            user_va_speak.configure(text='Ожидайте...')
                            handle_user_message(user_input)
                            user_va_speak.configure(text='Говорите...')
                    except PermissionError:
                        user_va_speak.configure(text='Ожидайте...')
                        wait_response(stream, recognizer)
                        user_va_speak.configure(text='Говорите...')

        elif selected_recognizer == 'Google':
            text = recognize_google(recognizer, language="ru-RU")
            if text:
                last_time_spoken = time.time()
                user_input = text

                user_va_speak.configure(text=limit_text_length(f'Вы сказали: {user_input}'))

                selected_recognizer = load_selected_recognizer()

                try:
                    if any(phrase in user_input.lower() for phrase in ["пока саша", "пока саш", "пк саша", "пк саш", "саша пока", "саш пока", "саша пк", 
                                                                       "пока сань", "пока саня", "пк сань", "пк саня", "саня пока", "сань пока", "саня пк",
                                                                       "пока сша", "пк сша", "сша пока", "сша пока", "сша пк", "пока сошел", "пока сошёл", "сошел пока", "сошёл пока"]):
                        chat_activated = False
                        goodbye = random.choice(goodbyes)
                        user_va_speak.configure(text='Ожидайте...')
                        va_speak(goodbye)
                        user_va_speak.configure(text='Скажите "Привет Саша"...')
                        remove_old_wav_files()
                        wait_response_google(stream, selected_recognizer, user_va_speak)
                        return
                    else:
                        handle_user_message(user_input, user_va_speak)
                except PermissionError:
                    wait_response(stream, recognizer)

def wait_response(stream, recognizer):
    global running_flag

    try:
        remove_old_wav_files()
    except:
        pass

    last_time_spoken = time.time()

    while running_flag.is_set():
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)

        selected_recognizer = load_selected_recognizer()

        if selected_recognizer == 'Vosk':
            if (recognizer.AcceptWaveform(data)) and (len(data) > 0):
                answer = json.loads(recognizer.Result())
                if answer['text']:
                    last_time_spoken = time.time()
                    user_input = answer['text']

                    user_va_speak.configure(text=limit_text_length(f'Вы сказали: {user_input}'))

                    if any(phrase in user_input.lower() for phrase in ["пока саша", "пока саш", "пк саша", "пк саш", "саша пока", "саш пока", "саша пк", 
                                                                       "пока сань", "пока саня", "пк сань", "пк саня", "саня пока", "сань пока", "саня пк",
                                                                       "пока сша", "пк сша", "сша пока", "сша пока", "сша пк"]):
                        user_va_speak.configure(text='Ожидайте...')
                        va_speak('Я уже с вами прощалась. Позовите меня, когда будет нужно')
                        user_va_speak.configure(text='Скажите "Привет Саша"...')
                    elif any(word == user_input.lower() for word in ["алло", "ты здесь", "здесь", "ты тут", "тут", "прием", "але", "где ты",
                        "саша алло", "саша ты здесь", "саша тут", "саша прием", "саша але", "саша где ты", "саша здесь", "саша ты тут",
                        "саш алло", "саш ты здесь", "саш тут", "саш прием", "саш але", "саш где ты", "саш здесь", "саш ты тут",
                        "сша алло", "сша ты здесь", "сша тут", "сша прием", "сша але", "сша где ты", "сша здесь", "сша ты тут",
                        'сажать здесь', "что здесь"]):
                        user_va_speak.configure(text='Ожидайте...')
                        va_speak("Нет, я не здесь")
                        user_va_speak.configure(text='Скажите "Привет Саша"...')
                    elif any(phrase in user_input.lower() for phrase in ["привет саша", "привет саш", "саша", "саш", 'аша', 'наша', 'санек', 'санок', 
                                                                        "привет саня", "привет сань", "саня привет", "сань привет", "саня", "сань",
                                                                        "сша привет", "привет сша", "сша", "суше", "саж", "привет сошел", "привет сошёл", "сошел привет", "сошёл привет"]):
                        user_va_speak.configure(text='Ожидайте...')
                        chat_activated = True
                        listen_for_input(stream, recognizer)

def wait_response_google(stream, selected_recognizer, user_va_speak):
    global running_flag

    last_time_spoken = time.time()

    while running_flag.is_set():
        if selected_recognizer == 'Google':
            text = recognize_google(selected_recognizer, language="ru-RU")
            if text:
                last_time_spoken = time.time()
                user_input = text

                user_va_speak.configure(text=limit_text_length(f'Вы сказали: {user_input}'))

                if any(phrase in user_input.lower() for phrase in ["пока саша", "пока саш", "пк саша", "пк саш", "саша пока", "саш пока", "саша пк",
                                                                   "пока сань", "пока саня", "пк сань", "пк саня", "саня пока", "сань пока", "саня пк",
                                                                   "пока сша", "пк сша", "сша пока", "сша пока", "сша пк"]):
                    user_va_speak.configure(text='Ожидайте...')
                    va_speak('Я уже с вами прощалась. Позовите меня, когда будет нужно')
                    user_va_speak.configure(text='Скажите "Привет Саша..."')
                elif any(word == user_input.lower() for word in ["алло", "ты здесь", "здесь", "ты тут", "тут", "прием", "але", "где ты",
                    "саша алло", "саша ты здесь", "саша тут", "саша прием", "саша але", "саша где ты", "саша здесь", "саша ты тут",
                    "саш алло", "саш ты здесь", "саш тут", "саш прием", "саш але", "саш где ты", "саш здесь", "саш ты тут",
                    "сша алло", "сша ты здесь", "сша тут", "сша прием", "сша але", "сша где ты", "сша здесь", "сша ты тут",
                    'сажать здесь', "что здесь"]):
                    va_speak("Нет, я не здесь")
                elif any(phrase in user_input.lower() for phrase in ["привет саша", "привет саш", "саша", "саш", 'аша', 'наша', 'санек', 'санок', 
                                                                    "привет саня", "привет сань", "саня привет", "сань привет", "саня", "сань",
                                                                    "сша привет", "привет сша", "сша", "суше", "саж", "привет сошел", "привет сошёл", "сошел привет", "сошёл привет"]):
                    user_va_speak.configure(text='Ожидайте...')
                    chat_activated = True
                    listen_for_input(stream, recognizer, user_va_speak)

def remove_old_wav_files():
    try:
        bot_helper_path = os.path.join(os.path.expanduser("~"), "Documents", "BotHelper")
        log_file_path = os.path.join(bot_helper_path, "remove_old_files_log.txt")

        for file_name in os.listdir(bot_helper_path):
            if file_name.startswith("ChatGPT_Voice_") and file_name.endswith(".wav"):
                os.remove(os.path.join(bot_helper_path, file_name))
            if file_name.startswith("Text_ChatGPT-") and file_name.endswith(".txt"):
                try:
                    os.remove(os.path.join(bot_helper_path, file_name))
                except Exception as e:
                    log_error(log_file_path, file_name, e)
            if file_name.startswith("Code_ChatGPT-") and file_name.endswith(".txt"):
                try:
                    os.remove(os.path.join(bot_helper_path, file_name))
                except Exception as e:
                    log_error(log_file_path, file_name, e)
    except PermissionError:
        pass

def start_ChatGPT(stream, user_va_speak, va_speak, selected_recognizer, Model, KaldiRecognizer):
    try:
        remove_old_wav_files()
    except:
        pass

    if not config.has_section('Settings'):
        select_model()
        set_extra_wait_time()

    if selected_recognizer == 'Vosk':
        user_va_speak.configure(text='Загрузка модели...')
        va_speak('Подождите, идет загрузка модели.')

        model = Model(selected_model)
        recognizer = KaldiRecognizer(model, SAMPLE_RATE)

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)
        stream.start_stream()

        user_va_speak.configure(text='Скажите "Привет Саша"...')

        va_speak('Я готова к работе!')

        wait_response(stream, recognizer)

        stream.stop_stream()
        stream.close()
        p.terminate()
    elif selected_recognizer == 'Google':
        user_va_speak.configure(text='Ожидайте...')
        va_speak('Я готова к работе!')
        user_va_speak.configure(text='Скажите "Привет Саша"...')
        wait_response_google(stream, selected_recognizer, user_va_speak)

def off_ChatGPT(config, selected_recognizer, user_va_speak, va_speak):
    try:
        remove_old_wav_files()
    except:
        pass

    if not config.has_section('Settings'):
        select_model()
        set_extra_wait_time()

    if selected_recognizer == 'Vosk':
        user_va_speak.configure(text='Для общения включите AI')
        va_speak('Отключаюсь.')

    elif selected_recognizer == 'Google':
        user_va_speak.configure(text='Для общения включите AI')
        va_speak('Отключаюсь.')

# Проверка автозапуска ассистента
def check_autorun_assistant_model(user_va_speak):
    if AUTO_RUN_MODEL == 'True' or AUTO_RUN_MODEL == 'Да' or AUTO_RUN_MODEL == True:
        on_button_start_click(user_va_speak)
    else:
        pass

def on_buttons_Sasha(window, user_va_speak):
    global button8, button9
    
    font = ctk.CTkFont(family='Arial', size=20)

    button8 = ctk.CTkButton(window, text='Включить AI', command=lambda: on_button_start_click(user_va_speak))
    button9 = ctk.CTkButton(window, text='Выключить AI', command=lambda: on_button_stop_click(user_va_speak))

    button8.grid(row=4, column=0, sticky='we', pady=2)
    button9.grid(row=4, column=1, padx=(5, 0), sticky='we', pady=2)

    button8.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
    button9.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=DISABLED)

# Основное меню настроек бота
def menu_setting_bot(window, user_va_speak):
    global window_setting_bot, topmost

    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)

    try:
        window.withdraw()
    except NameError:
        window.deiconify()
    except AttributeError:
        window.deiconify()

    window_setting_bot = ctk.CTkToplevel(window)
    window_setting_bot.resizable(width=False, height=False)
    window_setting_bot.title('Настройки программы')
    window_setting_bot.columnconfigure([0, 1], weight=1, minsize=140)
    window_setting_bot.rowconfigure([0, 1], weight=1, minsize=0)
    window_setting_bot.protocol('WM_DELETE_WINDOW', lambda: exit_menu(window))

    # Задаем размеры окна
    window_setting_bot.geometry(f"{center_x - int(window_width / 1.55)}+{center_y - int(window_height / 5)}")

    # Чекбокс "поверх окон"
    topmost = BooleanVar()
    update_checkbox_state(window)
    check = ctk.CTkCheckBox(window_setting_bot, text='', variable=topmost, onvalue=True, offvalue=False, command=lambda: on_top(window), corner_radius=20, hover=True, font=font)
    check.grid(row=0, column=1, columnspan=2, padx=0, sticky='e')
    check.configure(width=70)
    ctk.CTkLabel(window_setting_bot, text="Поверх всех окон", font=font).grid(column=0, row=0, columnspan=2, sticky='w', padx=40)

    # Проверить состояние чекбокса
    checkbox_state = topmost.get()
    
    # Сохранить состояние чекбокса
    save_checkbox_state(checkbox_state)
    
    # Установить атрибут "-topmost" для главного окна в зависимости от состояния чекбокса
    window.attributes("-topmost", checkbox_state)

    # Закрыть файл базы данных (если он был открыт)
    if 'db' in locals():
        db.close()

    # Кнопки
    button1 = ctk.CTkButton(window_setting_bot, text='Автозагрузка', width=15, command=lambda: new_win(window, window_setting_bot), font=font)
    button1.grid(row=1, column=0, columnspan=2, sticky='we', pady=2, padx=2)
    button1.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button2 = ctk.CTkButton(window_setting_bot, text='Ассистент', width=15, command=lambda: ChatGPT_setting(window, window_setting_bot), font=font)
    button2.grid(row=2, column=0, columnspan=2, sticky='we', pady=2, padx=2)
    button2.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button3 = ctk.CTkButton(window_setting_bot, text='Добавить пути приложениям', width=15, command=lambda: menu_path(window, window_setting_bot), font=font)
    button3.grid(row=3, column=0, columnspan=2, sticky='we', pady=2, padx=2)
    button3.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button4 = ctk.CTkButton(window_setting_bot, text='Персонализация', width=15, command=lambda: personalization(window, user_va_speak, window_setting_bot), font=font)
    button4.grid(row=4, column=0, columnspan=2, sticky='we', pady=2, padx=2)
    button4.configure(corner_radius=8, hover=True, hover_color='green', font=font)