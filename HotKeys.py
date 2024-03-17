import customtkinter as ctk
import tkinter as tk
import webbrowser, os
from tkinter import Entry, END, messagebox, Tk, Button, filedialog, Label, BooleanVar

from Power import menu_pc, Power_off, templates, Calc_sec, Reboot, templates_reboot, Calc_sec
from Browser import vk_and_youtube, youtube, google_disk, google_translate, gmail, sites_open, window_vk
from AutoClicker import one_click_win, reference
from Repair import start_window_FixPC
from System_Windows import cmds, autoloading, regedit, services, appdata, device_manager, finish_process
from Randomizer import menu_random, withdraw_random_number, withdraw_generator_number, heads_or_tails
from Setting_Bot import new_win, ChatGPT_setting, menu_path

enter = None
window_power_pc = None
window_other_menu = None

def create_enter_widget(window):
    global enter
    enter = ctk.CTkEntry(window, font=('Arial', 20, 'bold'), width=250, justify='center', placeholder_text='Введите запрос...')
    enter.focus()
    enter.grid(row=0, column=0, columnspan=2, sticky='wns', pady=2)

    enter.bind('<Return>', lambda event: handle_hotkeys(window, enter))

    return enter

def handle_hotkeys(window, enter):
    value = enter.get()

    # список горячих клавиш
    hotkeys = ['11', '111', '112', '113', '114', '1121', '1122', '1123', '1124',
               '12', '121', '122', '123', '124', '1221', '1222', '1223', '1224', '13', '14', '15', 
               '21', '22', '221', '222', '223', '23', '24', '25', '26', '27', 
               '31', '32', '33', '34', '35', '36', '37',
               '41', '42', '43',
               '51', '52', '53',
               '61', '62', '63', '64', '641', '642', '643', '644', '65', '66', '67', '674','68', '6811', '6812', '682',
               '0 ']

    if value in hotkeys:
        # Питание пк
        if value == '11':
            window.withdraw()
            enter.delete(0, tk.END)
            Power_off(window_power_pc, window)
        elif value == '111':
            window.withdraw()
            enter.delete(0, tk.END)
            os.system('shutdown /s /t 1 /f')
        elif value == '112':
            window.withdraw()
            enter.delete(0, tk.END)
            templates(window_power_pc, window)
        elif value == '113':
            window.withdraw()
            enter.delete(0, tk.END)
            os.system('shutdown -a')
        elif value == '114':
            window.withdraw()
            enter.delete(0, tk.END)
            Calc_sec(window_power_pc, window)
        elif value == '1121':
            enter.delete(0, tk.END)
            os.system('shutdown /s /t 1800 /f')
        elif value == '1122':
            enter.delete(0, tk.END)
            os.system('shutdown /s /t 3600 /f')
        elif value == '1123':
            enter.delete(0, tk.END)
            os.system('shutdown /s /t 5400 /f')
        elif value == '1124':
            enter.delete(0, tk.END)
            os.system('shutdown /s /t 7200 /f')
        elif value == '12':
            window.withdraw()
            enter.delete(0, tk.END)
            Reboot(window_power_pc, window)
        elif value == '121':
            window.withdraw()
            enter.delete(0, tk.END)
            os.system('shutdown /r /t 1 /f')
        elif value == '122':
            window.withdraw()
            enter.delete(0, tk.END)
            templates_reboot(window_power_pc, window)
        elif value == '123':
            enter.delete(0, tk.END)
            os.system('shutdown -a')
        elif value == '124':
            window.withdraw()
            enter.delete(0, tk.END)
            Calc_sec(window_power_pc, window)
        elif value == '1221':
            enter.delete(0, tk.END)
            os.system('shutdown /r /t 1800 /f')
        elif value == '1222':
            enter.delete(0, tk.END)
            os.system('shutdown /r /t 3600 /f')
        elif value == '1223':
            enter.delete(0, tk.END)
            os.system('shutdown /r /t 5400 /f')
        elif value == '1224':
            enter.delete(0, tk.END)
            os.system('shutdown /r /t 7200 /f')
        elif value == '13':
            enter.delete(0, tk.END)
            Hybernation_question = messagebox.askyesno('Уверены?', 'Вы точно хотите включить гибернацию?')
            if Hybernation_question == 'Да':
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            elif Hybernation_question == 'Нет':
                pass
        elif value == '14':
            enter.delete(0, tk.END)
            Exit_question = messagebox.askyesno('Уверены?', 'Вы точно хотите выйти из системы?')
            if Exit_question == 'Да':
                os.system('shutdown /l')
            elif Exit_question == 'Нет':
                pass
        elif value == '15':
            window.withdraw()
            enter.delete(0, tk.END)
            Calc_sec()

        #браузер
        elif value == '21':
            enter.delete(0, tk.END)
            vk_and_youtube()
            enter.delete(0, tk.END)
        elif value == '22':
            enter.delete(0, tk.END)
            window_vk(window)
        elif value == '221':
            webbrowser.open('https://vk.com/feed')
            enter.delete(0, tk.END)
        elif value == '222':
            webbrowser.open('https://vk.com/im')
            enter.delete(0, tk.END)
        elif value == '223':
            webbrowser.open('https://vk.com/id0')
            enter.delete(0, tk.END)
        elif value == '23':
            enter.delete(0, tk.END)
            youtube()
        elif value == '24':
            enter.delete(0, tk.END)
            google_translate()
        elif value == '25':
            enter.delete(0, tk.END)
            google_disk()
        elif value == '26':
            enter.delete(0, tk.END)
            gmail()
        elif value == '27':
            enter.delete(0, tk.END)
            window.withdraw()
            sites_open(window)

        # Система
        elif value == '31':
            enter.delete(0, tk.END)
            cmds()
        elif value == '32':
            enter.delete(0, tk.END)
            autoloading()
        elif value == '33':
            enter.delete(0, tk.END)
            regedit()
        elif value == '34':
            enter.delete(0, tk.END)
            services()
        elif value == '35':
            enter.delete(0, tk.END)
            appdata()
        elif value == '36':
            enter.delete(0, tk.END)
            device_manager()
        elif value == '37':
            enter.delete(0, tk.END)
            window.withdraw()
            finish_process(window)

        # Починка пк
        elif value == '41':
            enter.delete(0, tk.END)
            window.withdraw()
            messagebox.showinfo('Предупреждение', 'Данная функция имеет всего одно окно', parent=None)
            start_window_FixPC(window)
        elif value == '42':
            enter.delete(0, tk.END)
            window.withdraw()
            messagebox.showinfo('Предупреждение', 'Данная функция имеет всего одно окно', parent=None)
            start_window_FixPC(window)
        elif value == '43':
            enter.delete(0, tk.END)
            window.withdraw()
            messagebox.showinfo('Предупреждение', 'Данная функция имеет всего одно окно', parent=None)
            start_window_FixPC(window)

        # Настройки бота
        elif value == '51':
            enter.delete(0, tk.END)
            window.withdraw()
            new_win(window)
        elif value == '52':
            enter.delete(0, tk.END)
            window.withdraw()
            ChatGPT_setting(window)
        elif value == '53':
            enter.delete(0, tk.END)
            window.withdraw()
            menu_path(window)

        # Прочее
        elif value == '61':
            enter.delete(0, tk.END)
            window.withdraw()
            Weather()
        elif value == '62':
            enter.delete(0, tk.END)
            window.withdraw()
            News()
        elif value == '63':
            enter.delete(0, tk.END)
            window.withdraw()
            converter_files()
        elif value == '64':
            enter.delete(0, tk.END)
            window.withdraw()
            main_menu_other()
        elif value == '641':
            enter.delete(0, tk.END)
            window.withdraw()
            create_widgets()
        elif value == '642':
            enter.delete(0, tk.END)
            window.withdraw()
            snake.gameLoop()
        elif value == '643':
            enter.delete(0, tk.END)
            window.withdraw()
            tic_tac_toe()
        elif value == '644':
            enter.delete(0, tk.END)
            window.withdraw()
            arcanoid()
        elif value == '65':
            enter.delete(0, tk.END)
            window.withdraw()
            test_ethernet()
        elif value == '66':
            enter.delete(0, tk.END)
            window.withdraw()
            find_game()
        # Автокликер
        elif value == '67':
            enter.delete(0, tk.END)
            window.withdraw()
            one_click_win(window, window_other_menu)
        elif value == '674':
            enter.delete(0, tk.END)
            try:
                reference(window)
            except Exception:
                window.deiconify()
        # Рандомайзер
        elif value == '68':
            enter.delete(0, tk.END)
            window.withdraw()
            menu_random(window, window_other_menu)
        elif value == '6811':
            enter.delete(0, tk.END)
            window.withdraw()
            withdraw_random_number(window)
        elif value == '6812':
            enter.delete(0, tk.END)
            window.withdraw()
            withdraw_generator_number(window)
        elif value == '682':
            enter.delete(0, tk.END)
            try:
                heads_or_tails(window)
            except Exception:
                window.deiconify()

    elif value.startswith('0 '):
        cmd_command = value[2:].strip()
        subprocess.call(cmd_command, shell=True)
        enter.delete(0, tk.END)
        return

    # elif value not in hotkeys:
    #     if '.' in value:  # если вводится имя сайта, а не запрос
    #         url = 'https://' + value
    #         webbrowser.open_new(url)
    #         enter.delete(0, tk.END)
    #     else:
    #         url = 'https://www.google.com/search?q=' + value
    #         webbrowser.open_new(url)
    #         enter.delete(0, tk.END)