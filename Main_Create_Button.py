import os
import pickle
from PIL import Image
import customtkinter as ctk

# Путь к папке с иконками
current_directory = os.path.dirname(os.path.abspath(__file__))
path_to_icons = os.path.join(current_directory, 'icons')

# Путь к файлу настроек
settings_file = os.path.join(current_directory, 'button_settings.pkl')

# Стандартные настройки кнопок
default_button_settings = {
    "Power": {"color": "grey"},
    "Browser": {"color": "grey"},
    "System": {"color": "grey"},
    "ToolPC": {"color": "grey"},
    "Setting": {"color": "grey"},
    "Others": {"color": "grey"},
    "Reference": {"color": "grey"},
    "AI": {"color": "grey"}
}

# Функция для загрузки настроек из файла
def load_button_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'rb') as file:
            button_settings = pickle.load(file)
    else:
        button_settings = default_button_settings
    return button_settings

# Функция для сохранения настроек в файл
def save_button_settings(button_settings):
    with open(settings_file, 'wb') as file:
        pickle.dump(button_settings, file)

# Функция для изменения цвета кнопки
def change_button_color(button_name, new_color, window):
    button_settings = load_button_settings()
    button_settings[button_name]["color"] = new_color
    save_button_settings(button_settings)
    load_button_settings()

# Функция для создания кнопки с настройками
def create_button(window, button_name, button_text, command, row, column):
    button_settings = load_button_settings()
    button_color = button_settings.get(button_name, {}).get("color", "gray")
    button_image = button_settings.get(button_name, {}).get("icon", f"{path_to_icons}\\{button_name}.png")
    button = ctk.CTkButton(window, text=button_text, image=ctk.CTkImage(dark_image=Image.open(button_image), size=(30, 30)), compound="left", command=command, fg_color=button_color, hover_color=adjust_lightness(button_color, 0.2))
    button.grid(row=row, column=column, padx=10, pady=10)
    return button

# Функция для изменения яркости цвета
def adjust_lightness(color, amount=0.5):
    import colorsys
    try:
        r, g, b = [int(x, 16) / 255 for x in [color[1:3], color[3:5], color[5:7]]]
    except ValueError:
        return color
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    new_l = max(0, min(1, amount * l))
    new_r, new_g, new_b = colorsys.hls_to_rgb(h, new_l, s)
    return '#%02x%02x%02x' % (int(new_r * 255), int(new_g * 255), int(new_b * 255))