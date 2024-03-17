import customtkinter as ctk
import tkinter as tk
from tkinter import *
import win32api, threading, psutil, time, speedtest

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

is_running = True

def test_ethernet(window, window_other_menu):
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)
    def get_network_usage():
        network_io_counters = psutil.net_io_counters()
        sent_bytes = network_io_counters.bytes_sent
        recv_bytes = network_io_counters.bytes_recv
        time.sleep(1)
        network_io_counters = psutil.net_io_counters()
        sent_bytes_diff = network_io_counters.bytes_sent - sent_bytes
        recv_bytes_diff = network_io_counters.bytes_recv - recv_bytes
        total_bytes = sent_bytes_diff + recv_bytes_diff
        if total_bytes < 1024:
            return f"{total_bytes:.2f} Б/с"
        elif total_bytes < 1048576:
            return f"{total_bytes/1024:.2f} Кб/с"
        elif total_bytes < 1073741824:
            return f"{total_bytes/1048576:.2f} Мб/с"
        else:
            return f"{total_bytes/1073741824:.2f} Гб/с"

    def update_network_load():
        while True:
            network_usage = get_network_usage()
            label.configure(text=f"Скорость интернета: {network_usage}")

    def test_speed():
        try:
            test_label.configure(text="Подождите, идет тестирование...")
            window_speed_test.update()
            speed_test = speedtest.Speedtest()
            server_names = []
            speed_test.get_servers(server_names)
            test_label.configure(text="Выбор лучшего сервера...")
            speed_test.get_best_server()
            test_label.configure(text="Вычисляем скорость загрузки...")
            download_speed = speed_test.download()
            test_label.configure(text="Вычисляем скорость выгрузки...")
            upload_speed = speed_test.upload()
            if download_speed < 1024:
                download_result = f"{download_speed:.2f} Б/с"
            elif download_speed < 1048576:
                download_result = f"{download_speed/1024:.2f} Кб/с"
            elif download_speed < 1073741824:
                download_result = f"{download_speed/1048576:.2f} Мб/с"
            else:
                download_result = f"{download_speed/1073741824:.2f} Гб/с"
            if upload_speed < 1024:
                upload_result = f"{upload_speed:.2f} Б/с"
            elif upload_speed < 1048576:
                upload_result = f"{upload_speed/1024:.2f} Кб/с"
            elif upload_speed < 1073741824:
                upload_result = f"{upload_speed/1048576:.2f} Мб/с"
            else:
                upload_result = f"{upload_speed/1073741824:.2f} Гб/с"
            test_label.configure(text=f"────────────────────\nСкорость загрузки: {download_result},\nСкорость выгрузки: {upload_result}")
            test_button.configure(state=tk.ACTIVE)
        except speedtest.ConfigRetrievalError:
            test_label.configure(text="Проверьте доступ\nв интернет.")
            test_button.configure(state=tk.ACTIVE)
        except speedtest.NoMatchedServers:
            test_label.configure(text="Нет подходящих серверов\nдля тестирования скорости.")
            test_button.configure(state=tk.ACTIVE)
        except speedtest.SpeedtestException:
            test_label.configure(text="Произошла ошибка\nпри тестировании скорости.")
            test_button.configure(state=tk.ACTIVE)

    def test_speed_thread():
        global Thread
        test_button.configure(state="disabled")
        Thread = threading.Thread(target=test_speed)
        Thread.start()

    def speed_window():
        global only_speed_window
        def update_network_load_2():
            while True:
                network_usage = get_network_usage()
                label.configure(text=f"Скорость интернета: {network_usage}")
        
        def exit_in_window_other_menu():
            try:
                window_other_menu.deiconify()
                only_speed_window.destroy()
                only_speed_window.quit()
            except NameError:
                window.deiconify()
                only_speed_window.destroy()
                only_speed_window.quit()
            except AttributeError:
                window.deiconify()
                only_speed_window.destroy()
                only_speed_window.quit()

        try:
            window_speed_test.destroy()
            window_speed_test.quit()
        except NameError:
            window_speed_test.destroy()
            window_speed_test.quit()
            window.deiconify()
        except AttributeError:
            window_speed_test.destroy()
            window_speed_test.quit()
            window.deiconify()

        only_speed_window = ctk.CTk()
        only_speed_window.resizable(width=False, height=False)
        only_speed_window.title('Нагрузка')
        only_speed_window.columnconfigure([0], weight=1, minsize=150)
        only_speed_window.rowconfigure([0, 1, 2, 3], weight=1, minsize=0)
        only_speed_window.protocol("WM_DELETE_WINDOW", exit_in_window_other_menu)
        only_speed_window.attributes("-topmost", True)

        only_speed_window.geometry(f"{center_x - int(window_width / 1.3)}+{center_y - int(window_height / 4)}")

        label = ctk.CTkLabel(only_speed_window, text="Загрузка...", font=font_2)
        label.pack()

        thread = threading.Thread(target=update_network_load_2)
        thread.start()
        
        only_speed_window.mainloop()

    def on_top_test_speed():
        button_on_top.configure(state=DISABLED)
        button_off_top.configure(state=ACTIVE)
        window_speed_test.attributes("-topmost", True)
    def off_top_test_speed():
        button_on_top.configure(state=ACTIVE)
        button_off_top.configure(state=DISABLED)
        window_speed_test.attributes("-topmost", False)

    def on_closing():
        try:
            window_other_menu.deiconify()
            window_speed_test.destroy()
            window_speed_test.quit()
        except:
            window.deiconify()
            window_speed_test.destroy()
            window_speed_test.quit()

    try:
        window_other_menu.withdraw()
    except NameError:
        window.withdraw()
    except AttributeError:
        window.withdraw()

    window_speed_test = ctk.CTk()
    window_speed_test.resizable(width=False, height=False)
    window_speed_test.title('Нагрузка')
    window_speed_test.columnconfigure([0], weight=1, minsize=150)
    window_speed_test.rowconfigure([0,1,2,3,4], weight=1, minsize=0)
    window_speed_test.protocol("WM_DELETE_WINDOW", on_closing)
    window_speed_test.geometry(f"{center_x - int(window_width / 1.5)}+{center_y - int(window_height / 4)}")

    label = ctk.CTkLabel(window_speed_test, text="Загрузка...", font=font_2)
    test_label = ctk.CTkLabel(window_speed_test, text="", font=font_2)
    test_button = ctk.CTkButton(window_speed_test, text="Тест скорости интернета", width = 25, command=test_speed_thread, font=font)
    button_on_top = ctk.CTkButton(window_speed_test, text='Поверх всех окон', width = 25, command=on_top_test_speed, font=font)
    button_off_top = ctk.CTkButton(window_speed_test, text='Не поверх всех окон', width = 25, command=off_top_test_speed, font=font)
    button_speed_window = ctk.CTkButton(window_speed_test, text='Только скорость интернета', width = 25, command=speed_window, font=font)

    label.grid(column=0, row=0, sticky='we')
    test_label.grid(column=0, row=1, sticky='we')
    test_button.grid(column=0, row=2, sticky='we', pady=2, padx=2)
    button_on_top.grid(column=0, row=3, sticky='we', pady=2, padx=2)
    button_off_top.grid(column=0, row=4, sticky='we', pady=2, padx=2)
    button_speed_window.grid(column=0, row=5, sticky='we', pady=2, padx=2)

    button_off_top.configure(state=DISABLED)

    thread = threading.Thread(target=update_network_load)
    thread.start()
    
    window_speed_test.mainloop()