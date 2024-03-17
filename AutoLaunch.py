import os
import shutil
import customtkinter as ctk
from tkinter import NORMAL, DISABLED
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

# Автозагрузка бота
def new_win(window, window_setting_bot):
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)
    def update_window():
        # Перерисовываем кнопку but
        but.grid_forget()
        but_text = "Добавить бота в автозагрузку" if not check_startup_file() else "Бот в автозагрузке"
        but_state = NORMAL if not check_startup_file() else DISABLED
        but.configure(text=but_text, state=but_state)
        but.grid(column=0, row=0, sticky='we')

        # Перерисовываем кнопку but2
        but2.grid_forget()
        but2_text = "Убрать бота из автозагрузки" if check_startup_file() else "Бот не в автозагрузке"
        but2_state = NORMAL if check_startup_file() else DISABLED
        but2.configure(text=but2_text, state=but2_state)
        but2.grid(column=0, row=1, sticky='we')

    def check_startup_file():
        return os.path.isfile(os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "Бот-помощник.lnk"))

    def auto_launch():
        try:
            work_dir = os.path.dirname(os.path.abspath(__file__))
            shortcut_path = os.path.join(work_dir, "Бот-помощник.lnk")
            copy_in = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            shutil.copy(shortcut_path, copy_in)
            but.configure(text="Бот успешно добавлен!", state=DISABLED)
            switch_button_states()
            update_window()
        except FileNotFoundError:
            but.configure(corner_radius=8, hover=True, hover_color='green', font=font, state=NORMAL)
            but2.configure(corner_radius=8, hover=True, hover_color='green', font=font, state=DISABLED)

    def not_launch():
        try:
            shortcut_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "Бот-помощник.lnk")
            os.remove(shortcut_path)
            but2.configure(text="Бот успешно убран!", state=DISABLED)
            switch_button_states()
            update_window()
        except FileNotFoundError:
            but.configure(corner_radius=8, hover=True, hover_color='green', font=font, state=DISABLED)
            but2.configure(corner_radius=8, hover=True, hover_color='green', font=font, state=NORMAL)

    def exit_menu_2():
        try:
            nwin.destroy()
            window_setting_bot.deiconify()
        except (NameError, AttributeError):
            nwin.destroy()
            window.deiconify()

    try:
        window_setting_bot.withdraw()
    except (NameError, AttributeError):
        window.withdraw()

    nwin = ctk.CTkToplevel(window)
    nwin.resizable(width=False, height=False)
    nwin.title('Автозагрузка')
    nwin.columnconfigure([0], weight=1, minsize=150)
    nwin.rowconfigure([0, 1], weight=1, minsize=0)
    nwin.protocol('WM_DELETE_WINDOW', exit_menu_2)
    nwin.geometry(f"300x70+{center_x - int(window_width / 1.55)}+{center_y - int(window_height / 4)}")

    check_startup_file_result = check_startup_file()

    but_text = "Добавить бота в автозагрузку" if not check_startup_file_result else "Бот в автозагрузке"
    but_state = NORMAL if not check_startup_file_result else DISABLED
    but = ctk.CTkButton(nwin, text=but_text, width=55, command=auto_launch)
    but.grid(column=0, row=0, sticky='we')
    but.configure(corner_radius=8, hover=True, hover_color='green', font=font, state=but_state)

    but2_text = "Убрать бота из автозагрузки" if check_startup_file_result else "Бот не в автозагрузке"
    but2_state = NORMAL if check_startup_file_result else DISABLED
    but2 = ctk.CTkButton(nwin, text=but2_text, width=55, command=not_launch)
    but2.grid(column=0, row=1, sticky='we')
    but2.configure(corner_radius=8, hover=True, hover_color='green', font=font, state=but2_state)

    def switch_button_states():
        if but_state == NORMAL:
            but.configure(corner_radius=8, hover=True, hover_color='green', font=font, state=DISABLED)
            but2.configure(corner_radius=8, hover=True, hover_color='green', font=font, state=NORMAL)
        elif but2_state == NORMAL:
            but.configure(corner_radius=8, hover=True, hover_color='green', font=font, state=NORMAL)
            but2.configure(corner_radius=8, hover=True, hover_color='green', font=font, state=DISABLED)

    but.configure(command=lambda: [switch_button_states(), auto_launch()])
    but2.configure(command=lambda: [switch_button_states(), not_launch()])