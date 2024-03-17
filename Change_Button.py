import customtkinter as ctk
from Main_Create_Button import create_button, change_button_color

def open_color_settings(window):
    settings_window = ctk.CTkToplevel(window)
    settings_window.title("Настройки цветов кнопок")

    # Выпадающий список для выбора кнопки
    button_options = ["Power", "Browser", "System", "ToolPC", "Setting", "Others", "Reference", "AI"]
    button_name_var = ctk.StringVar()
    button_name_dropdown = ctk.CTkComboBox(settings_window, values=button_options, variable=button_name_var)
    button_name_dropdown.grid(row=0, column=0, padx=10, pady=10)

    # Выпадающий список для выбора цвета
    color_options = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "gray", "black", "white"]
    color_var = ctk.StringVar()
    color_dropdown = ctk.CTkComboBox(settings_window, values=color_options, variable=color_var)
    color_dropdown.grid(row=0, column=1, padx=10, pady=10)

    # Кнопка для применения изменений
    apply_button = ctk.CTkButton(settings_window, text="Применить", command=lambda: apply_color_change(button_name_var.get(), color_var.get(), window))
    apply_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def apply_color_change(button_name, new_color, window):
        change_button_color(button_name, new_color, window)