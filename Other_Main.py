import customtkinter as ctk
import win32api

from AutoClicker import one_click_win, reference
from Randomizer import menu_random
from Main_Weather import Weather
from Main_News import News
from Convert_Files import converter_files
from Games_Menu import main_menu_other
from Speed_Ethernet_Test import test_ethernet
from Search_Game import find_game

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

# Главное окно "Прочее"
def parent_menu(window):
    font = ctk.CTkFont(family='Arial', size=20)
    global window_other_menu
    def exit_back_menu_other():
        try:
            window_other_menu.destroy()
            window.deiconify()
        except NameError:
            window.deiconify()
        except TclError:
            window.deiconify()
        except AttributeError:
            window.deiconify()

    try:
        window.withdraw()
    except NameError:
        window.deiconify()
    except TclError:
        window.deiconify()
    except AttributeError:
        window.deiconify()

    window_other_menu = ctk.CTkToplevel(window)
    window_other_menu.title('Прочее')
    window_other_menu.resizable(width=False, height=False)
    window_other_menu.columnconfigure([0,1], weight=3, minsize=0)
    window_other_menu.rowconfigure([0,1,2,3], weight=3, minsize=0)
    window_other_menu.protocol('WM_DELETE_WINDOW', exit_back_menu_other)
    window_other_menu.geometry(f"{center_x - int(window_width / 1.3)}+{center_y - int(window_height / 4)}")

    # кнопки родительского окна
    button_window_other_menu_1 = ctk.CTkButton(window_other_menu, text='Погода', width=15, command=lambda: Weather(window, window_other_menu), font=font)
    button_window_other_menu_2 = ctk.CTkButton(window_other_menu, text='Новости', width=15, command=lambda: News(window, window_other_menu), font=font)
    button_window_other_menu_3 = ctk.CTkButton(window_other_menu, text='Конвертер', width=15, command=lambda: converter_files(window, window_other_menu), font=font)
    button_window_other_menu_4 = ctk.CTkButton(window_other_menu, text='Игры', width=15, command=lambda: main_menu_other(window, window_other_menu), font=font)
    button_window_other_menu_5 = ctk.CTkButton(window_other_menu, text='Интернет-скорость', width=15, command=lambda: test_ethernet(window, window_other_menu), font=font)
    button_window_other_menu_6 = ctk.CTkButton(window_other_menu, text='Поиск игр', width=15, command=lambda: find_game(window, window_other_menu), font=font)
    button_window_other_menu_7 = ctk.CTkButton(window_other_menu, text='Автокликер', width=15, command=lambda: one_click_win(window, window_other_menu), font=font)
    button_window_other_menu_8 = ctk.CTkButton(window_other_menu, text='Рандомайзер', width=15, command=lambda: menu_random(window, window_other_menu), font=font)

    button_window_other_menu_1.grid(row=0, column=0, sticky='we', pady=2, padx=2)
    button_window_other_menu_2.grid(row=0, column=1, sticky='we', pady=2, padx=2)
    button_window_other_menu_3.grid(row=1, column=0, sticky='we', pady=2, padx=2)
    button_window_other_menu_4.grid(row=1, column=1, sticky='we', pady=2, padx=2)
    button_window_other_menu_5.grid(row=2, column=0, sticky='we', pady=2, padx=2)
    button_window_other_menu_6.grid(row=2, column=1, sticky='we', pady=2, padx=2)
    button_window_other_menu_7.grid(row=3, column=0, sticky='we', pady=2, padx=2)
    button_window_other_menu_8.grid(row=3, column=1, sticky='we', pady=2, padx=2)

    button_window_other_menu_1.configure(width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
    button_window_other_menu_2.configure(width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
    button_window_other_menu_3.configure(width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
    button_window_other_menu_4.configure(width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
    button_window_other_menu_5.configure(width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
    button_window_other_menu_6.configure(width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
    button_window_other_menu_7.configure(width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
    button_window_other_menu_8.configure(width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")