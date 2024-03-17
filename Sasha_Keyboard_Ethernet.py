# -*- coding: utf-8 -*-

import customtkinter as ctk
from PIL import Image as PILImage
from tkinter import *
from langdetect import detect
from googletrans import Translator
from freeGPT import Client
import g4f, threading, random, re, os, time, requests, logging, aiohttp
from websearch import WebSearch as web
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MAX_MESSAGE_LENGTH = 3000
current_message = ""
lock = threading.Lock()

current_directory = os.path.dirname(os.path.abspath(__file__))
path_to_icons = f'{current_directory}\\icons'

photo_image_Exit_Ai = ctk.CTkImage(dark_image=PILImage.open(f"{path_to_icons}\\exit_ai.png"), size=(30, 30))

# Добавьте переменную для отслеживания состояния тумблера
internet_search_enabled = None

def exit_ai_chat(label_line_symbols, exit_ai, text_messages, entry_message, send_button, typing_label, internet_search_toggle):
    try:
        label_line_symbols.destroy()
        exit_ai.destroy()
        text_messages.destroy()
        entry_message.destroy()
        send_button.destroy()
        typing_label.destroy()
        internet_search_toggle.destroy()
    except (AttributeError, TclError, NameError):
        label_line_symbols.destroy()
        exit_ai.destroy()
        text_messages.destroy()
        entry_message.destroy()
        send_button.destroy()
        typing_label.destroy()
        internet_search_toggle.destroy()

def save_settings():
    # Сохраните состояние тумблера в файл
    settings_path = os.path.join(os.path.expanduser('~'), 'Documents', 'BotHelper', 'settings.txt')
    with open(settings_path, 'w') as settings_file:
        settings_file.write(f"internet_search_enabled: {str(internet_search_enabled)}")

def load_settings():
    # Загрузите состояние тумблера из файла
    settings_path = os.path.join(os.path.expanduser('~'), 'Documents', 'BotHelper', 'settings.txt')
    try:
        with open(settings_path, 'r') as settings_file:
            settings = settings_file.read()
            settings_dict = dict(item.split(": ") for item in settings.strip().split("\n"))
            return settings_dict.get('internet_search_enabled', 'False').lower() == 'true'
    except FileNotFoundError:
        return True
    except Exception as e:
        logging.error(f"Error loading settings: {e}")
        return True

# Инициализация переменной
internet_search_enabled = load_settings()

def search_in_google(query):
    typing_label.configure(text='Саша ищет информацию в интернете...')
    excluded_domains = ['youtube.com', 'rutube.ru', 'instagram.com', 'facebook.com', 'twitter.com', 'linkedin.com', 'twitch.tv']
    try:
        search_results = [page for page in web(query).pages[:1000] if not any(domain in page for domain in excluded_domains)]
        return search_results
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTPError in search_in_google: {e}")
    except ValueError:
        pass
    except Exception as e:
        logging.error(f"Exception in search_in_google: {e}")

def extract_cleaned_text_from_website(url, user_agent, result_list):
    typing_label.configure(text='Саша ищет информацию в интернете...')
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

        paragraphs = soup.find_all('p')
        text = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
        cleaned_text = clean_text(text)

        with lock:
            result_list.append(cleaned_text)
            
    except requests.exceptions.RequestException as e:
        pass
    except UnicodeDecodeError as e:
        pass
    except Exception as e:
        logging.error(f"Exception in extract_cleaned_text_from_website: {e}")

def clean_text(text):
    typing_label.configure(text='Саша ищет информацию в интернете...')
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = re.sub(r'\[[^\]]+\]', '', cleaned_text)
    cleaned_text = re.sub(r'Сомнительна связь.*', '', cleaned_text)
    cleaned_text = re.sub(r'Использованы данные словаря.*', '', cleaned_text)
    cleaned_text = re.sub(r'\([^)]*\)', '', cleaned_text)
    return cleaned_text.strip()

def format_text(text):
    typing_label.configure(text='Саша ищет информацию в интернете...')
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    formatted_text = ' '.join(sentences)
    return formatted_text

def generate_response(user_question, texts):
    typing_label.configure(text='Саша ищет информацию в интернете...')
    try:
        if not texts:
            return ''

        vectorizer = TfidfVectorizer().fit(texts)
        user_vector = vectorizer.transform([user_question])

        similarities = cosine_similarity(user_vector, vectorizer.transform(texts)).flatten()
        most_similar_index = similarities.argmax()

        most_similar_text = texts[most_similar_index]
        cleaned_most_similar_text = clean_text(most_similar_text)

        user_keywords = re.findall(r'\b\w+\b', user_question)
        relevant_sentences = [sentence for sentence in re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', cleaned_most_similar_text) if any(keyword in sentence for keyword in user_keywords)]

        selected_sentences = ' '.join(relevant_sentences[:100000])

        return selected_sentences
    except ValueError:
        logging.error("ValueError in generate_response")
        pass

def get_random_user_agent():
    typing_label.configure(text='Саша ищет информацию в интернете...')
    user_agent_file_path = "user-agents.txt"
    try:
        with open(user_agent_file_path, 'r') as file:
            user_agents = file.read().splitlines()
        return random.choice(user_agents)
    except Exception as e:
        logging.error(f"Exception in get_random_user_agent: {e}")
        return None

def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return "unknown"

def translate_to_russian(text):
    translator = Translator()
    translation = translator.translate(text, dest='ru')
    return translation.text
def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, dest='en')
    return translation.text

def generate_gpt_message(prompt, output_widget):
    global internet_search_enabled

    typing_label.configure(text='Саша печатает...')
    
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)

    send_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=DISABLED)

    user_question = prompt.strip().lower()

    if internet_search_enabled:
        search_results = search_in_google(user_question)

        if search_results:
            extracted_texts = []
            threads = []

            for i, result in enumerate(search_results):
                user_agent = get_random_user_agent()
                if user_agent is None:
                    logging.error("Failed to get a random user agent")
                    return

                try:
                    # Создаем новый поток для каждого веб-запроса
                    thread = threading.Thread(target=extract_cleaned_text_from_website, args=(result, user_agent, extracted_texts))
                    threads.append(thread)
                    thread.start()

                except Exception as e:
                    logging.error(f"Exception in thread creation: {e}")

            for thread in threads:
                thread.join()

            response = generate_response(user_question, extracted_texts)

            if response and response.strip():
                global current_message
                sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', response)
                current_message = ''
                for sentence in sentences:
                    if len(current_message) + len(sentence) <= MAX_MESSAGE_LENGTH:
                        current_message += sentence + ' '
                    else:
                        current_message = sentence + ' '
    else:
        pass

    input_text = f'Запрос: {prompt}\nИнформация из интернета: {current_message.strip()}\nПиши по русски.'
    input_text_2 = prompt

    lang = ''

    try:
        from g4f.client import Client
        client_2 = Client()
        try:
            if internet_search_enabled:
                typing_label.configure(text='Саша печатает...')
                response = client_2.chat.completions.create(model='gemini-pro', messages=[{"role": "user", "content": input_text}])
                response_text = response.choices[0].message.content
                lang = detect_language(response_text)
                output_widget.configure(state="normal")
                output_widget.insert(ctk.END, f"\nСаша: {response_text}\n")
                typing_label.configure(text='')
                send_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
            elif not internet_search_enabled:
                typing_label.configure(text='Саша печатает...')
                response = client_2.chat.completions.create(model='gemini-pro', messages=[{"role": "user", "content": input_text_2}])
                response_text = response.choices[0].message.content
                lang = detect_language(response_text)
                output_widget.configure(state="normal")
                output_widget.insert(ctk.END, f"\nСаша: {response_text}\n")
                typing_label.configure(text='')
                send_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
        except:
            if internet_search_enabled:
                typing_label.configure(text='Саша печатает...')
                response = client_2.chat.completions.create(model='airoboros-70b', messages=[{"role": "user", "content": input_text}])
                response_text = response.choices[0].message.content
                lang = detect_language(response_text)
                output_widget.configure(state="normal")
                output_widget.insert(ctk.END, f"\nСаша: {response_text}\n")
                typing_label.configure(text='')
                send_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
            elif not internet_search_enabled:
                typing_label.configure(text='Саша печатает...')
                response = client_2.chat.completions.create(model='airoboros-70b', messages=[{"role": "user", "content": input_text_2}])
                response_text = response.choices[0].message.content
                lang = detect_language(response_text)
                output_widget.configure(state="normal")
                output_widget.insert(ctk.END, f"\nСаша: {response_text}\n")
                typing_label.configure(text='')
                send_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)

    except (g4f.errors.RetryProviderError, aiohttp.client_exceptions.ClientResponseError):
        typing_label.configure(text='Переключаюсь на другую модель...')
        if lang != 'en':
            message = translate_to_english(input_text)
        typing_label.configure(text='Саша печатает...')
        #response = client_2.chat.completions.create("gpt3", input_text, typing_label, internet_search_enabled)
        response = client_2.chat.completions.create(model='airoboros-70b', messages=[{"role": "user", "content": input_text}])
        response_text = response.choices[0].message.content
        try:
            try:
                utf8_response = response_text.encode('ISO-8859-1').decode('UTF-8')
                lang = detect_language(utf8_response)
                if lang != 'ru':
                    message = translate_to_russian(utf8_response)
            except (UnicodeDecodeError, UnicodeEncodeError):
                lang = detect_language(response)
                if lang != 'ru':
                    message = translate_to_russian(response)
        except AttributeError:
            if internet_search_enabled:
                typing_label.configure(text='Я не могу сгенерировать сообщение.\nОтправляю информацию с интернета...')
                output_widget.configure(state="normal")
                output_widget.insert(ctk.END, f"\nСаша: {current_message.strip()}\n")
                typing_label.configure(text='Отправлена информация из интернета')
                send_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
                return

            if not internet_search_enabled:
                typing_label.configure(text='Включите поиск в интернете...')
                output_widget.configure(state="normal")
                output_widget.insert(ctk.END, f"\nСаша: Я не могу сгенерировать сообщение. Включите поиск в интернете... {current_message.strip()}\n")
                send_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)
                return
        output_widget.configure(state="normal")
        output_widget.insert(ctk.END, f"\nСаша: {message}\n")
        typing_label.configure(text='')
        send_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)

    except Exception as e:
        if internet_search_enabled:
            typing_label.configure(text='Я не могу сгенерировать сообщение.\nОтправляю информацию с интернета...')
            output_widget.configure(state="normal")
            output_widget.insert(ctk.END, f"\nСаша: {current_message.strip()}\n")
            typing_label.configure(text='Отправлена информация из интернета')
            print('3')
            send_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)

        if not internet_search_enabled:
            typing_label.configure(text='Включите поиск в интернете...')
            output_widget.configure(state="normal")
            output_widget.insert(ctk.END, f"\nСаша: Я не могу сгенерировать сообщение. Включите поиск в интернете... {current_message.strip()}\n")
            print('4')
            send_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)

    typing_label.configure(text='')

    send_button.configure(corner_radius=8, hover=True, hover_color='green', font=font, anchor="n", state=NORMAL)

def chat_on_Sasha(button11_main_menu_bot, window):
    global send_button, typing_label, internet_search_toggle, text_messages

    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)

    def send_message(event=None):
        user_message = entry_message.get()
        if user_message.strip():
            lang = detect_language(user_message)
            if lang != 'ru':
                user_message = translate_to_russian(user_message)

            text_messages.configure(state="normal")
            text_messages.insert(ctk.END, f"\nВы: {user_message}\n")
            text_messages.configure(state="disabled")
            entry_message.delete(0, ctk.END)

            # Запускаем генерацию ответа в отдельном потоке
            threading.Thread(target=generate_gpt_message, args=(user_message, text_messages)).start()

    def toggle_internet_search():
        global internet_search_enabled
        internet_search_enabled = not internet_search_enabled
        save_settings()

        if not internet_search_enabled:
            global current_message
            current_message = ""

        # Обновите состояние чекбокса в соответствии с файлом
        internet_search_toggle.deselect() if not internet_search_enabled else internet_search_toggle.select()

    label_line_symbols = ctk.CTkLabel(window, text = '═══════════════')
    label_line_symbols.grid(column = 0, row = 8, columnspan = 10, stick = 'we', pady = 2, padx = 2)

    exit_ai = ctk.CTkButton(window, text = '', command = lambda: exit_ai_chat(label_line_symbols, exit_ai, text_messages, entry_message, send_button, typing_label, internet_search_toggle))
    exit_ai.grid(row=9, column=0, columnspan=2)
    exit_ai.configure(image=photo_image_Exit_Ai, compound=TOP, width=1, corner_radius=8, hover=True, hover_color='green', font=font, anchor="w")

    text_messages = ctk.CTkTextbox(window, wrap="word", height=135, state="disabled", font=font_2)
    text_messages.grid(row=10, column=0, padx=10, pady=10, sticky="nsew", columnspan=10)

    entry_message = ctk.CTkEntry(window, placeholder_text='Напишите сообщение...')
    entry_message.grid(row=11, column=0, columnspan=1, padx=10, pady=10, sticky="we")

    send_button = ctk.CTkButton(window, text="Отправить", command=send_message, font=font)
    send_button.grid(row=11, column=1, padx=10, pady=10, sticky='we')
    send_button.configure(corner_radius=8, hover=True, hover_color='green', anchor="n", state=NORMAL)

    typing_label = ctk.CTkLabel(window, text="", font=("Arial", 14))
    typing_label.grid(row=12, column=1, padx=10, pady=10, sticky='e')

    internet_search_toggle = ctk.CTkCheckBox(window, text="Поиск в интернете", command=toggle_internet_search)
    internet_search_toggle.grid(row=12, column=0, padx=10, pady=10, sticky='w')

    # Обновите состояние чекбокса при запуске программы
    if internet_search_toggle is not None:
        if internet_search_enabled:
            internet_search_toggle.select()
        else:
            internet_search_toggle.deselect()

    window.bind("<Return>", send_message)