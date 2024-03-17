import os, subprocess, fitz, pdf2docx, threading, win32api
from tkinter import filedialog, messagebox
from docx2pdf import convert
import customtkinter as ctk
import tkinter as tk
from tkinter import *
from pydub import AudioSegment

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

# Ковертер файлов
def converter_files(window, window_other_menu):
    global window_converter
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)
    def exit_pdf_word_menu():
        try:
            window_other_menu.deiconify()
            window_converter.destroy()
        except NameError:
            window.deiconify()
            window_converter.destroy()
        except AttributeError:
            window.deiconify()
            window_converter.destroy()

    try:
        window_other_menu.withdraw()
    except NameError:
        window.withdraw()
    except AttributeError:
        window.withdraw()

    def convert_mp3_to_wav():
        mp3_file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])

        if not mp3_file_path:
            return

        wav_file_path = mp3_file_path.replace(".mp3", ".wav")
        audio = AudioSegment.from_mp3(mp3_file_path)
        audio.export(wav_file_path, format="wav")

        messagebox.showinfo('Success', 'MP3 to WAV conversion completed!')

        # Open the folder with the converted file
        os.system(f'explorer "{os.path.abspath(wav_file_path)}"')

    def convert_wav_to_mp3():
        wav_file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])

        if not wav_file_path:
            return

        mp3_file_path = wav_file_path.replace(".wav", ".mp3")
        audio = AudioSegment.from_wav(wav_file_path)
        audio.export(mp3_file_path, format="mp3")

        messagebox.showinfo('Success', 'WAV to MP3 conversion completed!')

        # Open the folder with the converted file
        subprocess.Popen(f'explorer /select,"{os.path.abspath(mp3_file_path)}"')

    def convert_pdf_to_images(pdf_file_path, output_folder):
        doc = fitz.open(pdf_file_path)
        for i, page in enumerate(doc):
            output_file_path = os.path.join(output_folder, f"page_{i}.png")
            pix = page.get_pixmap()
            pix.save(output_file_path, "PNG")

    def convert_word_to_png():
        # Получение пути к ворд-документу
        word_file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        
        if not word_file_path:
            # Разблокировка кнопки "png_button"
            png_button.configure(text="Выбрать файл и папку назначения", state="normal", corner_radius=8, hover=True, hover_color='green', font=font)
            return

        # Получение пути к папке назначения
        output_folder = filedialog.askdirectory()
        if not output_folder:
            # Разблокировка кнопки "png_button"
            png_button.configure(text="Выбрать файл и папку назначения", state="normal", corner_radius=8, hover=True, hover_color='green', font=font)
            return

        # Блокировка кнопки "png_button"
        png_button.configure(text="Подождите, идет конвертация...", state="disabled", corner_radius=8, hover=True, hover_color='green', font=font)

        # Конвертация ворд-документа в PDF
        pdf_file_path = os.path.join(output_folder, "output.pdf")
        convert(word_file_path, pdf_file_path)

        # Конвертация PDF в изображения PNG
        convert_pdf_to_images(pdf_file_path, output_folder)

        # Удаление временного PDF-файла
        os.remove(pdf_file_path)

        # Открытие папки с PNG файлами
        subprocess.Popen(f'explorer "{os.path.abspath(output_folder)}"')

        # Разблокировка кнопки "png_button"
        png_button.configure(text="Выбрать файл и папку назначения", state="normal", corner_radius=8, hover=True, hover_color='green', font=font)

    def button_click():
        # Блокировка кнопки "png_button"
        png_button.configure(text="Подождите, идет конвертация файла...", state="disabled", corner_radius=8, hover=True, hover_color='green', font=font)
        convert_word_to_png()

    # функция для открытия диалогового окна выбора PDF-файла
    def choose_pdf():
        pdf_button.configure(text='Выбрать PDF файл', state="disabled", width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
        convert_button.configure(text='Конвертировать', state="disabled", width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
        filename = filedialog.askopenfilename(filetypes=(("PDF files", "*.pdf"),))
        pdf_path.set(filename)

        pdf_file_3 = pdf_path.get()

        if pdf_file_3:
            pdf_button.configure(text='Выбрать PDF файл', state="normal", width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
            convert_button.configure(text='Конвертировать', state="normal", width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
        else:
            pdf_button.configure(state="normal")
            convert_button.configure(state="disabled")

    # функции для конвертации
    def convert_pdf():
        pdf_file = pdf_path.get()
        if pdf_file:
            # блокировка кнопок на время выполнения конвертации
            pdf_button.configure(text='Подождите, идет', state="disabled", width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
            convert_button.configure(text='конвертация', state="disabled", width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")

            # задаем имя для конвертированного файла
            word_file = pdf_file.split('.')[0] + '.docx'

            # вызываем функцию конвертации из библиотеки pdf2docx
            pdf2docx.parse(pdf_file, word_file)
            messagebox.showinfo('Успех', 'Конвертация завершена!', parent=window_converter)

            # разблокировка кнопок на время выполнения конвертации
            pdf_button.configure(text='Выбрать PDF файл', state="normal", width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
            convert_button.configure(text='Конвертировать', state="disabled", width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
            
            # открытие пути к сконвертированному файлу
            dir_path = os.path.dirname(pdf_file)
            os.startfile(dir_path)
        else:
            convert_button.configure(text='Конвертировать', state="disabled", width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
            messagebox.showerror('Ошибка', 'Выберите PDF файл', parent=window_converter)

    def thread_convert_pdf():
        threading.Thread(target=convert_pdf).start()

    # создаем окно приложения
    window_converter = ctk.CTkToplevel(window)
    window_converter.title('Конвертер')
    window_converter.protocol('WM_DELETE_WINDOW', exit_pdf_word_menu)
    window_converter.geometry(f"{center_x - int(window_width / 1.3)}+{center_y - int(window_height / 5)}")

    # переменная для хранения пути к PDF-файлу
    pdf_path = tk.StringVar()

    label_PDF_WORD = ctk.CTkLabel(window_converter, text='PDF → WORD', font=font)
    label_PDF_WORD.grid(column=0, columnspan=2, row=0)

    # Кнопка для выбора файла
    pdf_button = ctk.CTkButton(window_converter, text='Выбрать PDF файл', command=choose_pdf, font=font)
    pdf_button.configure(state='normal', width=5, corner_radius=8, hover=True, hover_color='green', anchor="w")
    pdf_button.grid(column=0, row=1)

    # Кнопка для конвертации
    convert_button = ctk.CTkButton(window_converter, text='Конвертировать', command=thread_convert_pdf, font=font)
    convert_button.grid(column=1, row=1)

    label_PDF_WORD = ctk.CTkLabel(window_converter, text='────────────────────────', font=font)
    label_PDF_WORD.grid(column=0, columnspan=2, row=2)

    label_PDF_WORD = ctk.CTkLabel(window_converter, text='WORD → PNG', font=font)
    label_PDF_WORD.grid(column=0, columnspan=2, row=3)

    png_button = ctk.CTkButton(window_converter, text="Выбрать файл и папку назначения", command=button_click, font=font)
    png_button.configure(state='normal', width=5, corner_radius=8, hover=True, hover_color='green')
    png_button.grid(column=0, columnspan=2, row=4, sticky='we')

    label_Audio = ctk.CTkLabel(window_converter, text='────────────────────────', font=font)
    label_Audio.grid(column=0, columnspan=2, row=5)

    label_Text_Audio = ctk.CTkLabel(window_converter, text='Аудио', font=font)
    label_Text_Audio.grid(column=0, columnspan=2, row=6)

    mp3_to_wav_button = ctk.CTkButton(window_converter, text='MP3 → WAV', command=convert_mp3_to_wav, font=font)
    mp3_to_wav_button.grid(column=0, row=7)

    wav_to_mp3_button = ctk.CTkButton(window_converter, text='WAV → MP3', command=convert_wav_to_mp3, font=font)
    wav_to_mp3_button.grid(column=1, row=7)

    pdf_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
    convert_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
    png_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
    mp3_to_wav_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
    wav_to_mp3_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)

    pdf_file_2 = pdf_path.get()

    if pdf_file_2:
        pdf_button.configure(text='Выбрать PDF файл', state="normal")
        convert_button.configure(text='Конвертировать', state="normal")
    else:
        convert_button.configure(text='Конвертировать', state="disabled")