import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading

def install_packages():
    global progress_frame
    global progress_label
    global progress_bar

    try:
        # обновляем pip
        subprocess.check_call(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # список пакетов для установки
        selected_packages = [pkg.get() for pkg in check_var_list]
        packages = [
            'pyautogui' if selected_packages[0] else '',
            'keyboard' if selected_packages[1] else '',
            'tk' if selected_packages[2] else '',
            'requests' if selected_packages[3] else '',
            'bs4' if selected_packages[4] else '',
            'DateTime' if selected_packages[5] else '',
            'threaded' if selected_packages[6] else '',
            'subprocess.run' if selected_packages[7] else '',
            'pdfminer' if selected_packages[8] else '',
            'PyPDF2' if selected_packages[9] else '',
            'python-docx' if selected_packages[10] else '',
            'pdf2docx' if selected_packages[11] else '',
            'pygame' if selected_packages[12] else '',
            'speedtest-cli' if selected_packages[13] else '',
            'psutil' if selected_packages[14] else '',
            'pywin32' if selected_packages[15] else '',
            'pyglet' if selected_packages[16] else '',
            'getpass4' if selected_packages[17] else '',
            'autocomplete' if selected_packages[18] else '',
            'SpeechRecognition' if selected_packages[19] else '',
            'pyttsx3' if selected_packages[20] else '',
            'PyAudio' if selected_packages[21] else '',
            'diffusers' if selected_packages[22] else '',
            'transformers' if selected_packages[23] else '',
            'customtkinter' if selected_packages[24] else '',
            'PyMuPDF' if selected_packages[25] else '',
            'docx2pdf' if selected_packages[26] else '',
            'pyttsx3' if selected_packages[27] else '',
            'pyaudio' if selected_packages[28] else '',
            'asyncio' if selected_packages[29] else '',
            'freeGPT' if selected_packages[30] else '',
            'pydub' if selected_packages[31] else '',
            'roman' if selected_packages[32] else '',
            'srt' if selected_packages[33] else '',
            'num2words' if selected_packages[34] else '',
            'googletrans' if selected_packages[35] else '',
            'langdetect' if selected_packages[36] else '',
            'fuzzywuzzy' if selected_packages [37] else '',
            'scikit-learn' if selected_packages [38] else ''
        ]
        packages = [package for package in packages if package] # удаляем пустые строки

        # показываем прогресс бар
        progress_frame.pack(fill=tk.BOTH, expand=True)
        progress_label.pack(side=tk.LEFT)
        progress_bar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # установка пакетов с отображением прогресса
        for i, package in enumerate(packages):
            progress_label.config(text=f"Установка пакета {package}")
            subprocess.check_call(['pip', 'install', package])
            # обновление прогресса
            progress_bar['value'] = (i+1) * (100/len(packages))
            root.update()

        # скрываем прогресс бар
        progress_frame.pack_forget()
    except subprocess.CalledProcessError:
        progress_frame.pack_forget()

def on_install_click():
    # проверка выбранных пакетов
    selected_packages = [pkg.get() for pkg in check_var_list]
    if not any(selected_packages):
        messagebox.showerror("Ошибка", "Выберите пакеты для установки")
        return
    # отключение кнопки "Установить" во время установки
    install_button.config(state=tk.DISABLED)
    # запуск установки в отдельном потоке
    install_thread = threading.Thread(target=install_packages)
    install_thread.start()
    # проверка завершения установки
    def check_install():
        if install_thread.is_alive():
            root.after(100, check_install)
        else:
            messagebox.showinfo("Установка завершена", "Установка пакетов завершена успешно")
            # включение кнопки "Установить"
            install_button.config(state=tk.NORMAL)
    root.after(100, check_install)

def select_all_packages():
    for var in check_var_list:
        var.set(True)

def deselect_all_packages():
    for var in check_var_list:
        var.set(False)

# создание окна
root = tk.Tk()
root.title("Установка пакетов")
root.resizable(width=False, height=False)

#Устанавливаем стиль оформления
style = ttk.Style()
style.theme_use("vista")

# создание фрейма для списка пакетов
package_frame = ttk.Frame(root, padding="10")
package_frame.pack(fill=tk.BOTH, expand=True)
ttk.Label(package_frame, text = "Выберите пакеты для установки:").pack(anchor="w")
check_var_list = []
for package_name in ['PyAutoGui', 'Keyboard', 'Tkinter', 'Requests', 'BS4', 'DateTime', 'Threaded', 'Subprocess', 
'Math', 'Random', 'PDFminer', 'PyPDF2', 'Python-Docx', 'Pdf2Docx', 'PyGame', 'SpeedTest', 'Psutil', 'Win32api',
'Pyglet', 'Getpass', 'Autocomplete', 'SpeechRecognition', 'Pyttsx3', 'PyAudio', 'Diffusers', 'Transformers', 
'CustomTkinter', 'PyMuPDF', 'Docx2PDF', 'PyTTSx3', 'PyAudio', 'Asyncio', 'FreeGPT', 'PyDub', 'Roman', 'SRT', 
'Num2Words', 'Translate', 'LangDetect', 'FuzzyWuzzy', 'Scikit-Learn']:
    var = tk.BooleanVar()
    check_var_list.append(var)
    ttk.Checkbutton(package_frame, text=package_name, variable=var).pack(anchor="w")

#создание кнопки "Выбрать все"
ttk.Button(root, text="Выбрать все", command=select_all_packages).pack(side=tk.LEFT, padx="10")

#создание кнопки "Убрать все"
ttk.Button(root, text="Убрать все", command=deselect_all_packages).pack(side=tk.LEFT, padx="10")

#создание кнопки "Установить"
install_button = ttk.Button(root, text="Установить", command=on_install_click)
install_button.pack(pady="10")

# создаем прогресс бар заранее
progress_frame = ttk.Frame(root, padding="10")
progress_label = ttk.Label(progress_frame, text="Установка пакетов:")
progress_bar = ttk.Progressbar(progress_frame, mode="determinate", variable=tk.IntVar())

#запуск цикла обработки событий
root.mainloop()