import tkinter as tk 
from tkinter import filedialog
import tkinter.simpledialog
import tkinter.ttk as ttk
import customtkinter as ctk
import win32api, os

bot_helper_dir = os.path.expanduser("~\\Documents\\BotHelper")
bot_helper_path_app = os.path.join(bot_helper_dir, "saved_app_path.txt")
app_paths = {}

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

# Добавить/убрать/изменить путь до программы
def menu_path(window, window_setting_bot):
    global app_name_entry, app_path_entry

    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)

    def exit_window_menu_path():
        try:
            window_menu_path.destroy()
            window_setting_bot.deiconify()
        except:
            window.deiconify()

    def add_path():
        app_name = app_name_entry.get()
        app_path = app_path_entry.get()
        
        if app_name and app_path:
            # Преобразуйте слеши обратно в обратные слеши
            app_path = app_path.replace("/", "\\")
            write_path_to_file(app_name, app_path)
            app_name_entry.delete(0, tk.END)
            app_path_entry.delete(0, tk.END)
            update_app_list()

    # Функция для удаления выбранного приложения
    def delete_selected_app():
        selected_item = app_tree.selection()
        if selected_item:
            app_name = app_tree.item(selected_item, "values")[0]
            if app_name in app_paths:
                del app_paths[app_name]
                write_paths_to_file()
                update_app_list()

    # Функция для выбора пути через диалоговое окно
    def select_path():
        selected_path = filedialog.askopenfilename()
        app_path_entry.delete(0, tk.END)
        app_path_entry.insert(0, selected_path)

    # Функция для обновления списка приложений в окне
    def update_app_list():
        app_tree.delete(*app_tree.get_children())
        sorted_app_paths = sorted(app_paths.items(), key=lambda x: x[0].lower())  # Сортировка по ключам (названиям) приложений
        for app, path in sorted_app_paths:
            app_tree.insert("", "end", values=(app, path))


    # Чтение существующих путей из файла и обновление списка
    def read_path_from_file(file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    parts = line.split(": ")
                    if len(parts) == 2:
                        app_name, app_path = parts
                        app_paths[app_name] = app_path
        except FileNotFoundError:
            pass

    # Функция для записи путей в файл
    def write_paths_to_file():
        with open(bot_helper_path_app, 'w') as file:
            for app_name, app_path in app_paths.items():
                file.write(f"{app_name}: {app_path}\n")

    def edit_selected_app():
        selected_item = app_tree.selection()
        if selected_item:
            selected_item = selected_item[0]  # Получить первый выбранный элемент
            app_name = app_tree.item(selected_item, "values")[0]  # Получить название приложения
            app_path = app_tree.item(selected_item, "values")[1]  # Получить путь к приложению

            # Запросить новое имя приложения
            new_app_name = tkinter.simpledialog.askstring("Изменить", "Введите новое название приложения:", initialvalue=app_name)

            if new_app_name is not None:  # Проверяем, была ли нажата кнопка "Отмена"
                # Отобразить диалоговое окно выбора файла для нового пути к приложению
                file_path = filedialog.askopenfilename(title="Выберите путь к приложению", initialfile=app_path)

                if file_path:  # Проверяем, был ли выбран новый файл
                    # Заменяем обратные слеши "\" на прямые "/"
                    file_path = file_path.replace("/", "\\")

                    # Удаляем старую запись
                    del app_paths[app_name]

                    # Если пользователь ввел новые данные, добавляем новую запись
                    app_tree.item(selected_item, values=(new_app_name, file_path))
                    app_paths[new_app_name] = file_path

                    # Записываем все изменения в файл
                    write_paths_to_file()

    try:
        window_setting_bot.withdraw()
    except (NameError, AttributeError):
        window.deiconify()

    try:
        window.withdraw()
    except (NameError, AttributeError):
        pass

    # Создание окна
    window_menu_path = ctk.CTkToplevel(window)
    window_menu_path.title("Установка путей приложений")
    window_menu_path.protocol('WM_DELETE_WINDOW', exit_window_menu_path)
    window_menu_path.resizable(width=False, height=False)
    window_menu_path.geometry(f"{center_x - int(window_width / 1.1)}+{center_y - int(window_height / 4)}")

    # Создание и настройка элементов интерфейса
    app_name_label = ctk.CTkLabel(window_menu_path, text="Название приложения:")
    app_name_entry = ctk.CTkEntry(window_menu_path, placeholder_text='Введите название...')

    app_path_label = ctk.CTkLabel(window_menu_path, text="Путь к приложению:")
    app_path_entry = ctk.CTkEntry(window_menu_path, placeholder_text='Введите путь...')

    select_path_button = ctk.CTkButton(window_menu_path, text="Выбрать файл", command=select_path)
    add_button = ctk.CTkButton(window_menu_path, text="Добавить", command=add_path)
    delete_button = ctk.CTkButton(window_menu_path, text="Удалить", command=delete_selected_app)
    edit_button = ctk.CTkButton(window_menu_path, text='Изменить', command=edit_selected_app)

    app_tree = ttk.Treeview(window_menu_path, columns=("App", "Path"), show="headings")
    app_tree.heading("App", text="Название приложения")
    app_tree.heading("Path", text="Путь к приложению")

    # Упорядочивание элементов интерфейса с помощью сетки
    app_name_label.grid(row=0, column=0, padx=2, pady=2, sticky="w")
    app_name_entry.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

    app_path_label.grid(row=1, column=0, padx=2, pady=2, sticky="w")
    app_path_entry.grid(row=1, column=1, padx=2, pady=2, sticky="ew")

    select_path_button.grid(row=0, column=2, padx=2)
    edit_button.grid(row=1, column=2, padx=2, pady=2, sticky="ew")
    add_button.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
    delete_button.grid(row=2, column=2, padx=2, pady=2, sticky="ew")

    app_tree.grid(row=3, column=0, columnspan=3, padx=2, pady=2, sticky="nsew")

    select_path_button.configure(width=5, corner_radius=8, hover=True, hover_color='green', font=font)
    edit_button.configure(width=5, corner_radius=8, hover=True, hover_color='green', font=font)
    add_button.configure(width=5, corner_radius=8, hover=True, hover_color='green', font=font)
    delete_button.configure(width=5, corner_radius=8, hover=True, hover_color='green', font=font)

    # Чтение существующих путей из файла и обновление списка
    read_path_from_file(bot_helper_path_app)
    update_app_list()