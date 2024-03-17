import customtkinter as ctk
import win32api

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

def hotkeys():
    window_hotkeys = ctk.CTkToplevel(window_what)
    window_hotkeys.title('Горячие клавиши')
    window_hotkeys.columnconfigure([0], weight=1, minsize=200)
    window_hotkeys.rowconfigure([0], weight=1, minsize=0)
    window_hotkeys.geometry('350x200')

    # Создание виджета скроллбара
    scrollbar = ctk.CTkScrollbar(window_hotkeys)
    scrollbar.grid(column=1, row=0, sticky='ns')

    # Создание виджета текста для отображения надписей
    text_widget = ctk.CTkTextbox(window_hotkeys, activate_scrollbars=False)
    text_widget.grid(column=0, row=0, sticky='nsew')

    # Привязка скроллбара к виджету текста
    scrollbar.configure(command=text_widget.yview)

    # Добавление текста в виджет текста
    text_widget.insert('end', '0 <команда> - Командная строка\n')
    text_widget.insert('end', '────────────────────────')
    text_widget.insert('end', '11 - Меню выключения ПК\n111 - Принудительное выключение ПК\n112 - Шаблоны выключения ПК\n113 - Отмена выключения ПК\n114 - Задать время выключения ПК\n1121 - Выключение ПК через 30 минут\n1122 - Выключение ПК через 1 час\n1123 - Выключение ПК через 1.5 часа\n1124 - Выключение ПК через 2 часа\n')
    text_widget.insert('end', '────────────────────────')
    text_widget.insert('end', '12 - Меню перезагрузки ПК\n121 - Принудительная перезагрузка ПК\n122 - Шаблоны перезагрузки ПК\n123 - Отмена перезагрузки ПК\n124 - Задать время перезагрузки ПК\n1221 - Перезагрузка ПК через 30 минут\n1222 - Перезагрузка ПК через 1 час\n1223 - Перезагрузка ПК через 1.5 часа\n1224 - Перезагрузка ПК через 2 часа\n')
    text_widget.insert('end', '────────────────────────')
    text_widget.insert('end', '13 - Гибернация пк\n14 - Выход из системы\n15 - Задать время\n')
    text_widget.insert('end', '────────────────────────')
    text_widget.insert('end', '21 - Открыть "Вконтакте" и "YouTube"\n22 - Меню "Вконтакте"\n221 - Открыть "Моя страница" в "Вконтакте"\n222 - Открыть "Сообщения" в "Вконтакте"\n223 - Открыть "Моя страница" в "Вконтакте\n')
    text_widget.insert('end', '────────────────────────')
    text_widget.insert('end', '23 - Открыть "YouTube"\n24 - Открыть "Переводчик"\n25 - Открыть "Гугл диск"\n26 - Открыть "Gmail"\n27 - Менеджер сайтов\n')
    text_widget.insert('end', '────────────────────────')
    text_widget.insert('end', '31 - Открыть командную строку\n32 - Открыть папку автозагрузки\n33 - Открыть реестр\n34 - Открыть службы\n35 - Открыть appdata\n36 - Открыть диспетчер устройств\n37 - Завершить процесс приложения\n')
    text_widget.insert('end', '────────────────────────')
    text_widget.insert('end', '51 - Автозагрузка программы\n52 - Настройка ассистента\n')
    text_widget.insert('end', '────────────────────────')
    text_widget.insert('end', '61 - Погода\n62 - Новости\n63 - PDF → WORD\n64 - Игры\n641 - Игра "Отгадай слово"\n642 - Игра "Змейка"\n643 - Игра "Крестики-нолики"\n644 - Игра "Арканоид"\n65 - Проверка скорости интернета\n66 - Поиск игр по минимальным ценам\n')
    text_widget.insert('end', '────────────────────────')
    text_widget.insert('end', '67 - Автокликер\n674 - Справка об автокликере\n')
    text_widget.insert('end', '────────────────────────')
    text_widget.insert('end', '68 - Меню рандомайзера\n6811 - Случайное число от 1 до 100\n6812 - Генератор чисел\n682 - Орел или решка')

    # Установка параметров отображения текста
    text_widget.configure(state='disabled', wrap='word')

    # Положение и растяжение виджетов в окне
    window_hotkeys.grid_columnconfigure(0, weight=1)
    window_hotkeys.grid_rowconfigure(0, weight=1)

    # Расположение скроллбара и виджета текста в окне
    text_widget.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=text_widget.yview)

def voice_help():
    window_hotkeys = ctk.CTkToplevel(window_what)
    window_hotkeys.title('Голосовые команды')
    window_hotkeys.columnconfigure([0], weight=1, minsize=200)
    window_hotkeys.rowconfigure([0], weight=1, minsize=0)
    window_hotkeys.geometry('382x200')

    # Создание виджета скроллбара
    scrollbar = ctk.CTkScrollbar(window_hotkeys)
    scrollbar.grid(column=1, row=0, sticky='ns')

    # Создание виджета текста для отображения надписей
    text_widget = ctk.CTkTextbox(window_hotkeys, activate_scrollbars=False)
    text_widget.grid(column=0, row=0, sticky='nsew')

    # Привязка скроллбара к виджету текста
    scrollbar.configure(command=text_widget.yview)

    # Добавление текста в виджет текста
    text_widget.insert('end', 'Активация ассистента: "Привет Саша"\nДеактивация ассистента: "Пока Саша"\nОчистка истории общения: "Новый диалог"\nГенерация изображнения: "Нарисуй мне <ваш запрос>"\nОткрытие приложений: "Открой <название программы>"\n')
    text_widget.insert('end', '────────────────────────\n')
    text_widget.insert('end', 'Выключи компьютер\nВыключи компьютер через - Google\nПерезагрузи компьютер\nПерезагрузи компьютер через - Google\nГибернация компьютера\nВыйди из системы\n')
    text_widget.insert('end', '────────────────────────\n')
    text_widget.insert('end', 'Включи вконтакте\nВключи ютуб\nВключи почту\nВключи переводчик\nВключи гугл диск\nВключи менеджер сайтов\n')
    text_widget.insert('end', '────────────────────────\n')
    text_widget.insert('end', 'Открой командную строку\nОткрой папку автозагрузки\nОткрой реестр\nОткрой службы\nОткрой диспетчер устройств\nОткрой завершение процесса\n')
    text_widget.insert('end', '────────────────────────\n')
    text_widget.insert('end', 'Открой автозагрузку программы\nОткрой настройки ассистента\n')
    text_widget.insert('end', '────────────────────────\n')
    text_widget.insert('end', 'Открой новости\nОткрой конвертацию файлов\n')
    text_widget.insert('end', '────────────────────────\n')
    text_widget.insert('end', 'Включи угадай слово\nВключи змейку\nВключи крестики-нолики\nВключи арканоид')

    # Установка параметров отображения текста
    text_widget.configure(state='disabled', wrap='word')

    # Положение и растяжение виджетов в окне
    window_hotkeys.grid_columnconfigure(0, weight=1)
    window_hotkeys.grid_rowconfigure(0, weight=1)

    # Расположение скроллбара и виджета текста в окне
    text_widget.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=text_widget.yview)

def what(window):
    global window_what

    font = ctk.CTkFont(family='Arial', size=20)

    window_what = ctk.CTkToplevel(window)
    window_what.title('Справка')
    window_what.columnconfigure([0], weight=1, minsize=0)
    window_what.rowconfigure([0, 1], weight=1, minsize=0)
    window_what.resizable(width=False, height=False)

    window_what.geometry(f"{center_x - int(window_width / 0.5)}+{center_y - int(window_height / 4)}")

    button1 = ctk.CTkButton(window_what, text='Горячие клавиши', width=15, height=30, command=hotkeys)
    button2 = ctk.CTkButton(window_what, text='Голосовые команды', width=15, height=30, command=voice_help)

    button1.grid(column=0, row=0, sticky='we', pady=2, padx=2)
    button2.grid(column=0, row=1, sticky='we', pady=2, padx=2)

    button1.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button2.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")

    version_label = ctk.CTkLabel(window_what, text="Version: 1.8.2", justify='center')
    version_label.grid(column=0, row=2, sticky='wens')