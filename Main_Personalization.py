import customtkinter as ctk
import win32api

from Change_Button import open_color_settings
from State_Panel_Word import save_panel_state, read_panel_state, toggle_panel_state, check_word_panel

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

# Персонализация программы
def personalization(window, user_va_speak, window_setting_bot):
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)
    def exit_menu_personalization():
        try:
            window_setting_bot.deiconify()
            window_personalization.destroy()
        except NameError:
            window.deiconify()
            window_personalization.destroy()
        except AttributeError:
            window.deiconify()
            window_personalization.destroy()

    def label_user_va_speak(user_va_speak):
        toggle_panel_state()
        state = read_panel_state()
        if state == "enabled":
            if user_va_speak and user_va_speak.grid_info():
                button_personalization_Label_1.configure(text='Включить панель слов', state="normal", corner_radius=8, hover=True, hover_color='green', font=font)
                button_personalization_Label_2.configure(text='Отключить панель слов', state="disabled", corner_radius=8, hover=True, hover_color='green', font=font)
                user_va_speak.grid_remove()
            else:
                button_personalization_Label_1.configure(text='Включить панель слов', state="disabled", corner_radius=8, hover=True, hover_color='green', font=font)
                button_personalization_Label_2.configure(text='Отключить панель слов', state="normal", corner_radius=8, hover=True, hover_color='green', font=font)
                user_va_speak.grid(row=6, column=0, columnspan=2, sticky='we', padx=0, pady=2)
        elif state == "disabled":
            if user_va_speak and user_va_speak.grid_info():
                button_personalization_Label_1.configure(text='Включить панель слов', state="normal", corner_radius=8, hover=True, hover_color='green', font=font)
                button_personalization_Label_2.configure(text='Отключить панель слов', state="disabled", corner_radius=8, hover=True, hover_color='green', font=font)
                user_va_speak.grid_remove()

    try:
        window_setting_bot.withdraw()
    except NameError:
        window.withdraw()
    except AttributeError:
        window.withdraw()

    window_personalization = ctk.CTkToplevel(window)
    window_personalization.title('Персонализация')
    window_personalization.protocol('WM_DELETE_WINDOW', exit_menu_personalization)
    window_personalization.geometry(f"{center_x - int(window_width / 1)}+{center_y - int(window_height / 7)}")

    panel_state = read_panel_state()
    button_personalization_Label_1 = ctk.CTkButton(window_personalization, text='Включить панель слов', command=lambda: label_user_va_speak(user_va_speak))
    button_personalization_Label_2 = ctk.CTkButton(window_personalization, text='Отключить панель слов', command=lambda: label_user_va_speak(user_va_speak))
    #button_personalization_Label_3 = ctk.CTkButton(window_personalization, text='Изменить кнопки', command=lambda: open_color_settings(window))

    button_personalization_Label_1.grid(row=0, column=0, sticky='we', pady=2)
    button_personalization_Label_2.grid(row=0, column=1, padx=(5, 0), sticky='we', pady=2)
    #button_personalization_Label_3.grid(row=1, column=0, columnspan=2, sticky='we', pady=2)

    button_personalization_Label_1.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    button_personalization_Label_2.configure(corner_radius=8, hover=True, hover_color='green', font=font)
    #button_personalization_Label_3.configure(corner_radius=8, hover=True, hover_color='green', font=font)

    if panel_state == "enabled":
        button_personalization_Label_1.configure(state="disabled", corner_radius=8, hover=True, hover_color='green', font=font)
    else:
        button_personalization_Label_2.configure(state="disabled", corner_radius=8, hover=True, hover_color='green', font=font)

    window_personalization.mainloop()