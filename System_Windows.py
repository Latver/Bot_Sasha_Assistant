import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import Entry, END, messagebox, Tk, Button, filedialog, Label, BooleanVar
import os, win32api, subprocess

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

#Функция системы Windows
def cmds():
    os.system('explorer C:\\Windows\\System32\\cmd.exe')
def autoloading():
    os.system('explorer C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
def regedit():
    os.system('%windir%\\regedit.exe')
def services():
    os.system('%windir%\\system32\\services.msc')
def appdata():
    os.system('explorer C:\\Users\\' + os.environ['USERNAME'] + '\\AppData')
def device_manager():
    os.system('explorer C:\\Windows\\System32\\devmgmt.msc')

def on_closing(window):
    try:
        window.deiconify()
        window_system.destroy()
    except NameError:
        window.deiconify()
        window_system.destroy()
    except TclError:
        window.deiconify()
        window_system.destroy()
    except AttributeError:
        window.deiconify()
        window_system.destroy()

#Завершение процесса
def finish_process(window):
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)
    try:
        window_system.withdraw()
    except NameError:
        pass
    except TclError:
        window.deiconify()
    except AttributeError:
        pass

    def kill_finish_process():
        nonlocal entry_finish_process
        value = entry_finish_process.get()
        os.system('Taskkill /PID ' + value + ' /F /T')

    def enter_finish_process(event=None):
        kill_finish_process()

    # Множество для отслеживания добавленных процессов
    added_processes = set()

    taskkill = subprocess.getoutput('TASKLIST /FI "USERNAME ne NT AUTHORITY\\SYSTEM" /FI "STATUS eq running"')
    process_list = []
    max_name_length = 0
    for line in taskkill.split('\n')[3:]:
        line = line.split()
        if len(line) > 1:
            name = line[0]
            pid = line[1]
            process_list.append((name, pid))
            max_name_length = max(max_name_length, len(name))

    def exit_back_system():
        try:
            window_system.deiconify()
            finish_process_win.destroy()
        except NameError:
            window.deiconify()
            finish_process_win.destroy()
        except TclError:
            window.deiconify()
            finish_process_win.destroy()
        except AttributeError:
            window.deiconify()
            finish_process_win.destroy()

    finish_process_win = ctk.CTk()
    finish_process_win.title('Завершить процесс')
    finish_process_win.protocol('WM_DELETE_WINDOW', exit_back_system)

    # Задаем размеры окна
    finish_process_win.geometry(f"350x350+{center_x - int(window_width / 1.3)}+{center_y - int(window_height / 4)}")

    label_finish_process = ctk.CTkLabel(finish_process_win, text='Выберите процесс:', font=font_2)
    label_finish_process.grid(column=0, row=0, sticky='we')

    lb = Listbox(finish_process_win, font=('Verdana', 10, 'bold'), height=len(process_list), width=max_name_length + 10)
    lb.grid(column=0, row=1, sticky='wens')

    # Показ только имени процесса и его PID
    for process in process_list:
        lb.insert(END, f'{process[0]}, [{process[1]}]')

    entry_finish_process = ctk.CTkEntry(finish_process_win, font=font_2, placeholder_text='Введите PID', justify='center')
    entry_finish_process.grid(column=0, row=2, sticky='wens')
    
    def update_process_list():
        current_selection = lb.curselection()
        current_position = lb.yview()
        taskkill = subprocess.getoutput('TASKLIST /FI "USERNAME ne NT AUTHORITY\\SYSTEM" /FI "STATUS eq running"')
        process_dict = {}
        max_name_length = 0
        for line in taskkill.split('\n')[3:]:
            line = line.split()
            if len(line) > 1:
                name = line[0]
                pid = line[1]
                process_dict[name] = pid
                max_name_length = max(max_name_length, len(name))

        # Сортировка списка процессов
        sorted_processes = sorted(process_dict.items(), key=lambda x: x[0].lower())

        lb.delete(0, tk.END)

        # Показ только имени процесса и его PID
        for name, pid in sorted_processes:
            lb.insert(tk.END, f'{name}, [{pid}]')

        lb.yview_moveto(current_position[0])
        if current_selection:
            lb.select_set(current_selection[0])

        # Рекурсивный вызов для обновления списка
        finish_process_win.after(1000, update_process_list)

    update_process_list()

    button_finish_process = ctk.CTkButton(finish_process_win, text='Завершить процесс', command=kill_finish_process, font=font)
    button_finish_process.grid(column=0, row=3, sticky='we', pady=2, padx=2)

    def on_select(evt):
        nonlocal entry_finish_process
        selected_process = lb.get(lb.curselection())
        selected_pid = selected_process[selected_process.index('[') + 1:selected_process.index(']')]
        entry_finish_process.delete(0, END)
        entry_finish_process.insert(END, selected_pid)

    lb.bind('<<ListboxSelect>>', on_select)

    finish_process_win.bind('<Return>', enter_finish_process)
    finish_process_win.columnconfigure([0], weight=1, minsize=150)
    finish_process_win.rowconfigure([0, 1, 2], weight=1, minsize=0)
    finish_process_win.mainloop()

    taskkill = subprocess.getoutput('TASKLIST /FI "USERNAME ne NT AUTHORITY\\SYSTEM" /FI "STATUS eq running"')
    process_list = []
    max_name_length = 0
    for line in taskkill.split('\n')[3:]:
        line = line.split()
        if len(line) > 1:
            name = line[0]
            pid = line[1]
            process_list.append((name, pid))
            max_name_length = max(max_name_length, len(name))
    lb.delete(0, END)
    # Показ только имени процесса и его PID
    for process in process_list:
        lb.insert(END, f'{process[0]}, [{process[1]}]')

def menu_windows_system(window):
    global window_system
    font = ctk.CTkFont(family='Arial', size=20)
    try:
        window.withdraw()
    except NameError:
        pass
    except TclError:
        window.deiconify()
    except AttributeError:
        pass

    window_system = ctk.CTkToplevel(window)
    window_system.title('Система')
    window_system.resizable(width=False, height=False)
    window_system.protocol('WM_DELETE_WINDOW', lambda: on_closing(window))
    window_system.columnconfigure([0], weight=1, minsize = 0)
    window_system.rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1, minsize = 0)

    # Задаем размеры окна
    window_system.geometry(f"{center_x - int(window_width / 1.3)}+{center_y - int(window_height / 4)}")

    #кнопки родительского окна
    button1 = ctk.CTkButton(window_system, text = 'Командная строка', command = cmds, width = 30, font=font)
    button1.grid(column = 0, row = 0, sticky = 'we', pady=2, padx=2)
    button2 = ctk.CTkButton(window_system, text = 'Папка автозагрузки', command = autoloading, width = 30, font=font)
    button2.grid(column = 1, row = 0, sticky = 'we', pady=2, padx=2)
    button3 = ctk.CTkButton(window_system, text = 'Реестр', command = regedit, width = 30, font=font)
    button3.grid(column = 0, row = 1, sticky = 'we', pady=2, padx=2)
    button4 = ctk.CTkButton(window_system, text = 'Службы', command = services, width = 30, font=font)
    button4.grid(column = 1, row = 1, sticky = 'we', pady=2, padx=2)
    button5 = ctk.CTkButton(window_system, text = 'Папка appdata', command = appdata, width = 30, font=font)
    button5.grid(column = 0, row = 2, sticky = 'we', pady=2, padx=2)
    button6 = ctk.CTkButton(window_system, text = 'Диспетчер устройств', command = device_manager, width = 30, font=font)
    button6.grid(column = 1, row = 2, sticky = 'we', pady=2, padx=2)
    button7 = ctk.CTkButton(window_system, text = 'Завершить процесс приложения', command = lambda: finish_process(window), width = 30, font=font)
    button7.grid(column = 0, row = 3, columnspan=2, sticky = 'we', pady=2, padx=2)

    button1.configure(corner_radius=8, hover=True, hover_color='green')
    button2.configure(corner_radius=8, hover=True, hover_color='green')
    button3.configure(corner_radius=8, hover=True, hover_color='green')
    button4.configure(corner_radius=8, hover=True, hover_color='green')
    button5.configure(corner_radius=8, hover=True, hover_color='green')
    button6.configure(corner_radius=8, hover=True, hover_color='green')
    button7.configure(corner_radius=8, hover=True, hover_color='green')