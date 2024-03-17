import customtkinter as ctk
from tkinter import ttk
from tkinter import *
from tkinter import Entry, END, messagebox, Tk, Button, filedialog, Label, BooleanVar
import os, win32api, threading, subprocess

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

#Функция починки пк
def clear_pc():
    global progress_bar
    font_2 = ctk.CTkFont(family='Arial', size=18)
    progress_bar = ttk.Progressbar(fixpc_window, orient=HORIZONTAL, length=200, mode='indeterminate')
    progress_bar.grid(column=0, row=4, pady=10)

    def task():
        try:
            fixpc_window.wm_attributes('-disabled', True)

            button1.configure(state='disabled', corner_radius=8, hover=True, hover_color='green')
            button2.configure(state='disabled', corner_radius=8, hover=True, hover_color='green')
            button3.configure(state='disabled', corner_radius=8, hover=True, hover_color='green')

            progress_bar.configure(mode='determinate', maximum=10, value=0)
            progress_bar.start()

            fix_label.configure(text='', font=font_2)

            # Список команд для выполнения с названиями операций
            commands = {
            'Удаление временных файлов': f'RMDIR /S /Q "{os.path.join(os.environ["LOCALAPPDATA"], "Temp")}"',
            'Очистка корзины': r'PowerShell.exe -Command "Clear-RecycleBin -Force"',
            'Очистка журналов приложений': r'PowerShell.exe -Command "wevtutil el | ForEach-Object {wevtutil cl $_}"',
            'Очистка журналов системы': r'PowerShell.exe -Command "wevtutil.exe cl System"',
            'Остановка службы обновления Windows': r'PowerShell.exe -Command "Stop-Service wuauserv"',
            'Очистка загрузок обновлений Windows': f'RMDIR /S /Q "{os.path.join("C:", "Windows", "SoftwareDistribution", "Download")}"',
            'Запуск службы обновления Windows': 'PowerShell.exe -Command "Start-Service wuauserv"',
            'Очистка кэша Microsoft Store': r'PowerShell.exe -Command "Remove-Item -Force -Recurse $env:LOCALAPPDATA\\Packages\\Microsoft.WindowsStore*\\LocalCache"',
            'Очистка кэша Prefetch': r'PowerShell.exe -Command "del /q/f/s "%systemwindow_converter%\Prefetch\*""',
            'Очистка журналов проверки обновлений': r'net stop wuauserv',
            'Очистка журналов проверки обновлений': r'net stop usosvc',
            'Очистка журналов проверки обновлений': r'DEL /F /S /Q /A %systemroot%\SoftwareDistribution\DataStore\Logs\edb.log',
            'Очистка журналов проверки обновлений': r'DEL /F /S /Q /A %ProgramData%\USOPrivate\UpdateStore\*',
            'Очистка журналов проверки обновлений': r'net start wuauserv',
            'Очистка журналов проверки обновлений': r'net start usosvc',
            'Очистка истории браузера IE': r'PowerShell.exe -Command "RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 8"',
            'Очистка временной папки': r'PowerShell.exe -Command "Get-ChildItem -Path $env:TEMP -Force | Remove-Item -Force -Recurse"',
            'Очистка временной папки Windows': r'PowerShell.exe -Command "Get-ChildItem -Path C:\Windows\Temp -Force | Remove-Item -Force -Recurse"'
            }

            for i, (operation, command) in enumerate(commands.items()):
                try:
                    subprocess.call(command, shell=True)
                    progress_bar['value'] = (i + 1) * 10
                    fix_label.configure(text=operation + '...')
                    fixpc_window.update()
                except subprocess.CalledProcessError as e:
                    messagebox.showinfo('Ошибка', f'Ошибка при выполнении команды "{command}": {e}', parent=fixpc_window)

            progress_bar.stop()
            progress_bar.grid_remove()
            fix_label.configure(text='...Выберите действие...', font=font_2)

            messagebox.showinfo('Успех!', 'Очистка пк завершена', parent=fixpc_window)

            fixpc_window.wm_attributes('-disabled', False)

            button1.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
            button2.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
            button3.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
        except RuntimeError:
            pass

    thread = threading.Thread(target=task)
    thread.start()

def check_files():
    font_2 = ctk.CTkFont(family='Arial', size=18)
    progress_bar = ttk.Progressbar(fixpc_window, orient=HORIZONTAL, length=200, mode='indeterminate')
    progress_bar.grid(column=0, row=4, pady=10)

    def task():
        try:
            fixpc_window.wm_attributes('-disabled', True)

            button1.configure(state='disabled', corner_radius=8, hover=True, hover_color='green')
            button2.configure(state='disabled', corner_radius=8, hover=True, hover_color='green')
            button3.configure(state='disabled', corner_radius=8, hover=True, hover_color='green')

            progress_bar.start(10)

            # Выполнение команды sfc
            fix_label.configure(text="Проверка целостности файлов...", font=font_2)
            subprocess.call("sfc /scannow", shell=True)
            progress_bar.step(1)

            # Выполнение команды DISM для проверки здоровья образа
            fix_label.configure(text="Проверка целостности образа Windows...", font=font_2)
            subprocess.call("DISM /Online /Cleanup-Image /CheckHealth", shell=True)
            progress_bar.step(1)

            # Выполнение команды DISM для сканирования здоровья образа
            fix_label.configure(text="Вторичная проверка целостности образа Windows...", font=font_2)
            subprocess.call("DISM /Online /Cleanup-Image /ScanHealth", shell=True)
            progress_bar.step(1)

            # Выполнение команды DISM для восстановления здоровья образа
            fix_label.configure(text="Восстановление файлов Windows...", font=font_2)
            subprocess.call("DISM /Online /Cleanup-Image /RestoreHealth", shell=True)
            progress_bar.step(1)

            progress_bar.stop()
            progress_bar.grid_remove()
            fix_label.configure(text="")

            messagebox.showinfo('Успех!', 'Проверка и восстановление поврежденных файлов завершена.', parent=fixpc_window)

            fixpc_window.wm_attributes('-disabled', False)

            button1.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
            button2.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
            button3.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
            fix_label.configure(text="...Выберите действие...", font=font_2)
        except RuntimeError:
            pass

    thread = threading.Thread(target=task)
    thread.start()

def fix_sound():
    font_2 = ctk.CTkFont(family='Arial', size=18)
    def fix_sound_threading():
        try:
            fixpc_window.wm_attributes('-disabled', True)

            button1.configure(state='disabled', corner_radius=8, hover=True, hover_color='green')
            button2.configure(state='disabled', corner_radius=8, hover=True, hover_color='green')
            button3.configure(state='disabled', corner_radius=8, hover=True, hover_color='green')

            fix_label.configure(text="Перезапуск службы звука...", font=font_2)
            os.system('net stop audiosrv')
            os.system('net start audiosrv')
            answer = messagebox.askyesno("Починка звука №1", "Помогло данное решение?", parent=fixpc_window)
            if answer == True:
                fixpc_window.wm_attributes('-disabled', False)

                fix_label.configure(text='Рад был помочь!')
                button1.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
                button2.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
                button3.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
            elif answer == False:
                fixpc_window.wm_attributes('-disabled', True)

                fix_label.configure(text="Перезапуск службы звука №2...", font=font_2)
                os.system('net stop "Windows Audio"')
                os.system('net start "Windows Audio"')
                answer_2 = messagebox.askyesno("Починка звука №2", "Помогло данное решение?", parent=fixpc_window)
                if answer_2 == True:
                    fixpc_window.wm_attributes('-disabled', False)

                    fix_label.configure(text='Рад был помочь!')
                    button1.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
                    button2.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
                    button3.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
                else:
                    fixpc_window.wm_attributes('-disabled', True)

                    fix_label.configure(text="Меняем тип запуска звука...", font=font_2)
                    os.system('sc config Audiosrv start= auto')
                    answer_3 = messagebox.askyesno("Починка звука №3", "Помогло данное решение?", parent=fixpc_window)
                    if answer_3 == True:
                        fixpc_window.wm_attributes('-disabled', False)

                        fix_label.configure(text='Рад был помочь!')
                        button1.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
                        button2.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
                        button3.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
                    else:
                        fixpc_window.wm_attributes('-disabled', False)

                        messagebox.showinfo('Другие способы', 'Попробуйте запустить пункт "Проверка файлов"', parent=fixpc_window)
                        button1.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
                        button2.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
                        button3.configure(state='enabled', corner_radius=8, hover=True, hover_color='green')
                        fix_label.configure(text="...Выберите действие...", font=font_2)
        except RuntimeError:
            pass

    thread = threading.Thread(target=fix_sound_threading)
    thread.start()

def start_window_FixPC(window):
    global fixpc_window, fix_label, button1, button2, button3

    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)

    def exit_back_fixpc():
        try:
            window.deiconify()
            fixpc_window.destroy()
        except NameError:
            window.deiconify()
            fixpc_window.destroy()
        except TclError:
            window.deiconify()
            fixpc_window.destroy()
        except AttributeError:
            window.deiconify()
            fixpc_window.destroy()

    try:
        window.withdraw()
    except NameError:
        window.deiconify()
    except TclError:
        window.deiconify()
    except AttributeError:
        window.deiconify()

    fixpc_window = ctk.CTkToplevel(window)
    fixpc_window.title('Ремонт пк')
    fixpc_window.resizable(width=False, height=False)
    fixpc_window.columnconfigure([0], weight=1, minsize=250)
    fixpc_window.rowconfigure([0, 1, 2], weight=1, minsize=0)
    fixpc_window.protocol('WM_DELETE_WINDOW', exit_back_fixpc)

    # Задаем размеры окна
    fixpc_window.geometry(f"{center_x - int(window_width / 1.8)}+{center_y - int(window_height / 5)}")

    button1 = ctk.CTkButton(fixpc_window, text='Очистка', width=15, command=clear_pc, font=font)
    button2 = ctk.CTkButton(fixpc_window, text='Проверка файлов', width=15, command=check_files, font=font)
    button3 = ctk.CTkButton(fixpc_window, text='Ремонт звука', width=15, command=fix_sound, font=font)

    button1.grid(column=0, row=0, sticky='we', padx=5, pady=2)
    button2.grid(column=0, row=1, sticky='we', padx=5, pady=2)
    button3.grid(column=0, row=2, sticky='we', padx=5, pady=2)

    button1.configure(corner_radius=8, hover=True, hover_color='green')
    button2.configure(corner_radius=8, hover=True, hover_color='green')
    button3.configure(corner_radius=8, hover=True, hover_color='green')

    fix_label = ctk.CTkLabel(fixpc_window, text="...Выберите действие...", font=font_2)
    fix_label.grid(column=0, row=3, columnspan=4, sticky='we')

    fixpc_window.mainloop()