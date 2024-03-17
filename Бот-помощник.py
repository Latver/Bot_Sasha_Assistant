# -*- coding: utf-8 -*-

#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬#
# Author: LATVER #
# Bot_v2.0       #
#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬#

#      1. Внедрение функции, позволяющей пользователям определять задачи для ассистента самостоятельно и давать ему инструкции по выполнению конкретных действий. (Ожидание)
#      2. В разделе "Настройки" → "Ассистент" планируется внести расширение, позволяющее пользователю выбирать предпочитаемый режим активации микрофона. (Ожидание)
#      3.1. Добавить выбор назначения клавиши для режима радио. (Ожидание)
#      4. Добавить конвертацию звуковых файлов. (ожидание)
#      5. Добавить возможность пользователю создавать собственные ключевые слова для вызова и прекращения работы ассистента. (ожидание)

#Библотеки
from tkinter import *
from tkinter import Entry, END, messagebox, Tk, Button, filedialog, Label, BooleanVar
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox, Scrollbar
import tkinter.simpledialog
import customtkinter as ctk
from PIL import Image
import os, time, keyboard, requests, pyautogui, threading, re, subprocess, random, webbrowser, datetime, psutil, logging
import getpass, speedtest, sys, win32api, pickle, tempfile, pygame, shutil, ctypes, roman, aiohttp

#from Main_Create_Button import create_button, load_button_settings
from Sasha_Keyboard_Ethernet import chat_on_Sasha
from HotKeys import create_enter_widget, handle_hotkeys
from Power import menu_pc, Power_off, templates, Calc_sec, Reboot, Calc_sec, stop
from Speak import va_speak, unpause_audio, pause_audio, stop_audio
from Browser import menu_browser
from Repair import start_window_FixPC
from System_Windows import cmds, autoloading, regedit, services, appdata, device_manager, finish_process, menu_windows_system
from Setting_Bot import menu_setting_bot, load_config, window_upper, recognize_google, select_model, set_extra_wait_time, selected_recognizer, load_selected_recognizer, check_autorun_assistant_model, on_button_start_click, on_button_stop_click, on_buttons_Sasha, start_ChatGPT, off_ChatGPT, remove_old_wav_files
from State_Panel_Word import save_panel_state, read_panel_state, toggle_panel_state, check_word_panel
from Other_Main import parent_menu
from Voice_and_Key_Help import what

# Функция на запрос прав администратора
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

#  Запрос прав администратора
if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()
else:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_icons = f'{current_directory}\\icons'

    def exit_bot():
        global running_flag

        window.wm_attributes('-disabled', True)

        buttons_to_destroy = [enter, button1_main_menu_bot, button2_main_menu_bot, button3_main_menu_bot, button4_main_menu_bot, button5_main_menu_bot, button6_main_menu_bot, button7_main_menu_bot, button10_main_menu_bot, user_va_speak, enter]
        for button in buttons_to_destroy:
            button.destroy()

        label = ctk.CTkLabel(window, text='...Выключение...', justify='center', font=font)
        label.grid(column=0, row=0, pady=90, padx=80)

        remove_old_wav_files()

        subprocess.call("taskkill /F /IM Бот-помощник.exe")
        subprocess.call("taskkill /F /IM Python.exe")

    def exit_bot_thread():
        exit_question = messagebox.askyesno('Уверены?', 'Вы точно хотите выйти из программы?')
        if exit_question:
            try:
                threading.Thread(target=exit_bot).start()
            except RuntimeError:
                exit_bot()
        else:
            pass

    def limit_text_length(text, max_length=46):
        if len(text) > max_length:
            return text[:max_length - 3] + "..."
        else:
            return text

    remove_old_wav_files()

    #При нажатии клавиши enter переходит в функцию files
    def press_enter(Return):
        handle_hotkeys(window, enter)

    def main_window():
        global window, font, font_2
        global enter, button1_main_menu_bot, button2_main_menu_bot, button3_main_menu_bot, button4_main_menu_bot, button5_main_menu_bot, button6_main_menu_bot, button7_main_menu_bot, button10_main_menu_bot, user_va_speak, enter

        window = ctk.CTk()
        window.title('Бот-помощник')
        window.columnconfigure([0, 1], weight=1, minsize=0)
        window.rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1, minsize=0)
        window.protocol('WM_DELETE_WINDOW', exit_bot_thread)
        window.resizable(width=False, height=False)

        # Получаем размер экрана
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)

        # Вычисляем размеры окна
        window_width = int(screen_width * 0.13)
        window_height = int(screen_height * 0.55)

        # Вычисляем координаты центра экрана
        center_x = int(screen_width / 2)
        center_y = int(screen_height / 2)

        # Задаем размеры окна
        window.geometry(f"{center_x - int(window_width / 1.55)}+{center_y - int(window_height / 4)}")

        #load_button_settings()

        #Нажатие клавиши "enter" переходит по введенной горячей клавише в функцию "press_enter"
        window.bind('<Return>', press_enter)

        # Питание пк
        photo_image_PowerPC = ctk.CTkImage(dark_image=Image.open(f"{path_to_icons}\\Power.png"), size=(30, 30))

        # Браузер
        photo_image_browser = ctk.CTkImage(dark_image=Image.open(f"{path_to_icons}\\Browser.png"), size=(30, 30))

        # Система
        photo_image_system = ctk.CTkImage(dark_image=Image.open(f"{path_to_icons}\\Fix.png"), size=(30, 30))
        
        # Ремонт пк
        photo_image_FixPC = ctk.CTkImage(dark_image=Image.open(f"{path_to_icons}\\ToolPC.png"), size=(30, 30))

        # Настройки бота
        photo_image_setting_bot = ctk.CTkImage(dark_image=Image.open(f"{path_to_icons}\\Setting.png"), size=(30, 30))

        # Прочее
        photo_image_other = ctk.CTkImage(dark_image=Image.open(f"{path_to_icons}\\Others.png"), size=(30, 30))

        # Перейти
        photo_image_searching = ctk.CTkImage(dark_image=Image.open(f"{path_to_icons}\\Searching.png"), size=(30, 30))

        # AI
        photo_image_AI = ctk.CTkImage(dark_image=Image.open(f"{path_to_icons}\\AI.png"), size=(30, 30))

        # Справка
        photo_image_reference = ctk.CTkImage(dark_image=Image.open(f"{path_to_icons}\\Reference.png"), size=(30, 30))

        # Кнопки, поле для ввода, панель слов
        user_va_speak = ctk.CTkLabel(window, text = 'Для общения включите AI', height=1)
        enter = create_enter_widget(window)
        button1_main_menu_bot = ctk.CTkButton(window, text='', command=lambda: handle_hotkeys(window, enter)) #create_button(window, 'Searching', '', lambda: handle_hotkeys(window, enter), row=0, column=1) 
        button2_main_menu_bot = ctk.CTkButton(window, text='Питание', command=lambda: menu_pc(button2_main_menu_bot, window)) #create_button(window, "Power", "Питание", lambda: menu_pc(button2_main_menu_bot, window), row=1, column=0) 
        button3_main_menu_bot = ctk.CTkButton(window, text='Браузер', command=lambda: menu_browser(window)) #create_button(window, 'Browser', 'Браузер', lambda: menu_browser(window), row=1, column=1)
        button4_main_menu_bot = ctk.CTkButton(window, text='Система', command=lambda: menu_windows_system(window)) #create_button(window, 'Fix', 'Система', lambda: menu_windows_system(window), row=2, column=0)
        button5_main_menu_bot = ctk.CTkButton(window, text='Ремонт', command=lambda: start_window_FixPC(window)) #create_button(window, 'ToolPC', 'Ремонт', lambda: start_window_FixPC(window), row=2, column=1) 
        button6_main_menu_bot = ctk.CTkButton(window, text='Настройки', command=lambda: menu_setting_bot(window, user_va_speak)) #create_button(window, 'Setting', 'Настройки', lambda: menu_setting_bot(window, user_va_speak), row=3, column=0) 
        button7_main_menu_bot = ctk.CTkButton(window, text='Прочее', command=lambda: parent_menu(window)) #create_button(window, 'Others', 'Прочее', lambda: parent_menu(window), row=3, column=1) 
        on_buttons_Sasha(window, user_va_speak)
        button10_main_menu_bot = ctk.CTkButton(window, text='Справка', command=lambda: what(window)) #create_button(window, 'Reference', 'Справка', lambda: what(window), row=7, column=0)
        button11_main_menu_bot = ctk.CTkButton(window, text='Чат с AI', command=lambda: chat_on_Sasha(button11_main_menu_bot, window)) #create_button(window, 'AI', 'Чат с AI', lambda: chat_on_Sasha(button11_main_menu_bot, window), row=5, column=0)

        font = ctk.CTkFont(family='Arial', size=20)
        font_2 = ctk.CTkFont(family='Arial', size=18)

        user_va_speak_text = user_va_speak.cget("text")
        limited_text = limit_text_length(user_va_speak_text)

        # Позиция кнопок, поля ввода, панели слов
        button1_main_menu_bot.grid(row=0, column=1, sticky='e', pady=2)
        button2_main_menu_bot.grid(row=1, column=0, sticky='we', pady=2)
        button3_main_menu_bot.grid(row=1, column=1, padx=(5, 0), sticky='we', pady=2)
        button4_main_menu_bot.grid(row=2, column=0, sticky='we', pady=2)
        button5_main_menu_bot.grid(row=2, column=1, padx=(5, 0), sticky='we', pady=2)
        button6_main_menu_bot.grid(row=3, column=0, sticky='we', pady=2)
        button7_main_menu_bot.grid(row=3, column=1, padx=(5, 0), sticky='we', pady=2)
        button10_main_menu_bot.grid(row=7, column=0, columnspan=2, sticky='we', padx=0, pady=2)
        button11_main_menu_bot.grid(row=5, column=0, columnspan=2, sticky='we', padx=0, pady=2)
        user_va_speak.grid(row=6, column=0, columnspan=2, sticky='we', padx=0, pady=2)

        # Параметры
        button1_main_menu_bot.configure(image=photo_image_searching, compound=LEFT, width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
        button2_main_menu_bot.configure(image=photo_image_PowerPC, compound=LEFT, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")
        button3_main_menu_bot.configure(image=photo_image_browser, compound=LEFT, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")
        button4_main_menu_bot.configure(image=photo_image_system, compound=LEFT, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")
        button5_main_menu_bot.configure(image=photo_image_FixPC, compound=LEFT, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")
        button6_main_menu_bot.configure(image=photo_image_setting_bot, compound=LEFT, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")
        button7_main_menu_bot.configure(image=photo_image_other, compound=LEFT, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")
        button10_main_menu_bot.configure(image=photo_image_reference, compound=LEFT, corner_radius=8, hover=True, hover_color='green', font=font, anchor="n")
        button11_main_menu_bot.configure(image=photo_image_AI, corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)

        # Check_word_panel
        check_word_panel(user_va_speak, selected_recognizer)

        # CFG assistant
        load_config()

        # Check_checkbox
        window_upper(window)

        check_autorun_assistant_model(user_va_speak)

        # Главная иконка
        window.after(201, lambda :window.iconbitmap(f"{path_to_icons}\\Bot_Helper_Icon.ico"))

        remove_old_wav_files()

        window.mainloop()

    main_window()

is_admin()