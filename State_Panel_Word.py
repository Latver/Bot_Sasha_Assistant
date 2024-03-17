import os
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

file_path = os.path.expanduser("~\\Documents\\BotHelper\\panel_state.txt")

# Сохранить панель слов
def save_panel_state(state):
    # Запись состояния панели слов в файл
    with open(file_path, "w") as file:
        file.write(state)

# Прочитать панель слов
def read_panel_state():
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "enabled"

# Загрузить состояние панели слов
def toggle_panel_state():
    state = read_panel_state()
    if state == "enabled":
        save_panel_state("disabled")
    else:
        save_panel_state("enabled")

# Проверка панели слов
def check_word_panel(user_va_speak, selected_recognizer):
    panel_state = read_panel_state()
    if panel_state == "enabled":
        user_va_speak.grid(row=6, column=0, columnspan=2, sticky='we', padx=0, pady=2)
    else:
        user_va_speak.grid_remove()