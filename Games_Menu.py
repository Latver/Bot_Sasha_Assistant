import customtkinter as ctk
import win32api

from Guess_the_Word import create_widgets
from Snake import gameLoop
from Tic_Tac_Toe import tic_tac_toe
from Arcanoid import arcanoid

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

def main_menu_other(window, window_other_menu):
    global window_game_menu
    
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)

    def exit_back_game_menu():
        try:
            window_other_menu.deiconify()
            window_game_menu.destroy()
        except (NameError, AttributeError):
            window.deiconify()
            window_game_menu.destroy()
    try:
        window_other_menu.withdraw()
        window.withdraw()
    except (NameError, AttributeError):
        pass

    window_game_menu = ctk.CTkToplevel(window)
    window_game_menu.title('Игры')
    window_game_menu.resizable(width=False, height=False)
    window_game_menu.columnconfigure([0], weight=1, minsize=150)
    window_game_menu.rowconfigure([0,1,2,3], weight=1, minsize=0)
    window_game_menu.protocol('WM_DELETE_WINDOW', exit_back_game_menu)
    window_game_menu.geometry(f"{center_x - int(window_width / 1.8)}+{center_y - int(window_height / 4)}")

    #Создаем кнопки
    button_window_game_1 = ctk.CTkButton(window_game_menu, text='Отгадай слово', width=15, command=lambda: create_widgets(window, window_game_menu))
    button_window_game_2 = ctk.CTkButton(window_game_menu, text='Змейка', width=15, command=lambda: gameLoop(window, window_game_menu))
    button_window_game_3 = ctk.CTkButton(window_game_menu, text='Крестики-нолики', width=15, command=lambda: tic_tac_toe(window, window_game_menu))
    button_window_game_4 = ctk.CTkButton(window_game_menu, text='Арканоид', width=15, command=lambda: arcanoid(window, window_game_menu))

    button_window_game_1.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button_window_game_2.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button_window_game_3.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button_window_game_4.configure(corner_radius=8, hover=True, hover_color='green', font=font)

    button_window_game_1.grid(column=0, row=0, sticky='we', pady=2, padx=2)
    button_window_game_2.grid(column=0, row=1, sticky='we', pady=2, padx=2)
    button_window_game_3.grid(column=0, row=2, sticky='we', pady=2, padx=2)
    button_window_game_4.grid(column=0, row=3, sticky='we', pady=2, padx=2)

    window_game_menu.mainloop()