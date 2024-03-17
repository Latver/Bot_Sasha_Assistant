import os, re, random, threading, logging, datetime, requests, aiohttp, io, win32com.client, concurrent.futures, subprocess, g4f, configparser
from urllib.parse import quote
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from fuzzywuzzy import process, fuzz
from langdetect import detect
from googletrans import Translator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
from PIL import Image, ImageTk
from io import BytesIO
from websearch import WebSearch as web
from freeGPT import Client
import pygetwindow as gw

from Speak import va_speak

documents_path = os.path.expanduser("~")
bot_helper_path = os.path.join(documents_path, "Documents", "BotHelper")
bot_helper_dir = os.path.expanduser("~\\Documents\\BotHelper")
bot_helper_path_app = os.path.join(bot_helper_dir, "saved_app_path.txt")
lock = threading.Lock()
MAX_MESSAGE_LENGTH = 3000
current_message = ''
app_paths = {}

CONFIG_FILE = os.path.join(bot_helper_path, "config.ini")
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

if not config.has_section('WebSearch'):
    config.add_section('WebSearch')
    config.set('WebSearch', 'web_search', 'True')
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

web_search = config.getboolean('WebSearch', 'web_search')

def limit_text_length(text, max_length=46):
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    else:
        return text

def replace_language_names(text):
    language_mappings = {
        "лат.": "латинского",
        "англ.": "английского",
        "др.-греч.": "древне-греческого"
    }
    for key, value in language_mappings.items():
        text = text.replace(key, value)
    return text

def generate_picture(user_input, user_va_speak):
    global prompt_picture
    user_va_speak.configure(text='Генерация изображения...')
    try:
        keywords = ["нарисуй", "сделай", "сгенерируй", "генерируй", 'сгенерировать', 'сгенерируйте',
        "нарисуй мне", "сделай мне", "сгенерируй мне", "генерируй мне", 'сгенерировать мне', 'сгенерируйте мне',
        "мне нарисуй", "мне сделай", "мне сгенерируй", "мне генерируй", 'мне сгенерировать', 'мне сгенерируйте',
        'но рисуем', 'но рисуем мне', 'мне', 'рисуй', 'рисуем']

        for phrase in keywords:
            user_input = user_input.replace(phrase, "").strip()

        user_input_translated = translate_sentences(user_input, src_lang='ru', dest_lang='en')

        prompt_picture = user_input_translated

        try:
            va_speak("Генерирую изображение")
            user_va_speak.configure(text='Генерация изображения...')
            resp = Client.create_generation("prodia", prompt_picture)
            va_speak("Изображение готово")
            Image.open(BytesIO(resp)).show()
            user_va_speak.configure(text='Говорите...')
        except Exception as e:
            user_va_speak.configure(text='Переключение на другую модель...')
            va_speak("Переключаюсь на другую модель")
            try:
                user_va_speak.configure(text='Генерация изображения...')
                va_speak("Генерирую изображение")
                resp = Client.create_generation("prodia", prompt_picture)
                va_speak("Изображение готово")
                Image.open(BytesIO(resp)).show()
                user_va_speak.configure(text='Говорите...')
            except Exception as e:
                va_speak("Произошла непредвиденная ошибка")
    except RuntimeError:
        prompt_picture = ''
        va_speak('Не удалось перевести запрос')

def read_path_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                parts = line.split(": ")
                if len(parts) == 2:
                    app_name, app_path = parts
                    app_paths[app_name] = app_path
    except FileNotFoundError:
        pass

def write_path_to_file(app_name, path):
    bot_helper_path = os.path.join(bot_helper_dir, "saved_app_path.txt")
    with open(bot_helper_path, 'a') as file:
        if app_name not in app_paths:
            file.write(f"{app_name}: {path}\n")
            app_paths[app_name] = path

def find_executable_recursive(root_dir, target_name):
    best_match = None
    best_score = 0

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_name, file_extension = os.path.splitext(file.lower())
            if file_extension in ['.exe', '.url']:
                score = fuzz.ratio(target_name.lower(), file_name)
                if score > best_score:
                    best_score = score
                    best_match = os.path.join(root, file)

    if best_score > 70:
        return best_match

    return None

def find_best_matching_application(target_name):
    available_drives = [chr(drive) for drive in range(65, 91)]
    if target_name in app_paths:
        return app_paths[target_name]

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    desktop_files = [os.path.splitext(file)[0] for file in os.listdir(desktop_path) if file.endswith(".lnk")]
    desktop_matches = process.extractOne(target_name, desktop_files, scorer=fuzz.ratio)
    
    if desktop_matches[1] > 70:
        desktop_result = os.path.join(desktop_path, desktop_matches[0] + ".lnk")
        write_path_to_file(target_name, desktop_result)
        return desktop_result

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(find_executable_on_drive, available_drives, [target_name] * len(available_drives)))

    for result in results:
        if result:
            write_path_to_file(target_name, result)
            return result
    
    return None

def find_and_execute_shortcut(target_name):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    for root, dirs, files in os.walk(desktop_path):
        for file in files:
            # Проверяем, является ли файл ярлыком
            if file.endswith(".lnk"):
                lnk_file_path = os.path.join(root, file)
                try:
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(lnk_file_path)
                    # Проверяем, совпадает ли цель ярлыка с искомым именем
                    if target_name.lower() in shortcut.TargetPath.lower():
                        os.startfile(shortcut.TargetPath)
                        return True
                except Exception as e:
                    print(f"Error: {str(e)}")

            # Если файл не имеет расширения, то пытаемся запустить его напрямую
            elif target_name.lower() in file.lower():
                file_path = os.path.join(root, file)
                try:
                    os.startfile(file_path)
                    return True
                except Exception as e:
                    print(f"Error: {str(e)}")

    return False

def find_executable_on_drive(drive, target_name):
    drive_letter = drive + ":\\"
    if os.access(drive_letter, os.R_OK):
        executable_path = find_executable_recursive(drive_letter, target_name)
        if executable_path:
            write_path_to_file(target_name, executable_path)
            return executable_path
    return None

def remove_last_line_from_file(file_path):
    try:
        with open(file_path, 'r+') as file:
            lines = file.readlines()
            if lines:
                lines = lines[:-1]
                file.seek(0)
                file.writelines(lines)
                file.truncate()
    except FileNotFoundError:
        pass

def open_application(application_path):
    bot_helper_dir = os.path.expanduser("~\Documents\BotHelper")
    bot_helper_path_app = os.path.join(bot_helper_dir, "saved_app_path.txt")
    
    try:
        if application_path:
            os.startfile(application_path)
            va_speak(f"Приложение успешно запущено.")
        else:
            va_speak(f"Приложение не найдено.")

    except UnboundLocalError:
        va_speak(f'Произошла ошибка при запуске программы')
    except OSError:
        remove_last_line_from_file(bot_helper_path_app)
        va_speak(f'Произошла ошибка при запуске программы')
        
def close_application(application_name, user_input=None):
    # Закрыть окно
    window = gw.getWindowsWithTitle(application_name)
    if window:
        try:
            window[0].close()
            va_speak(f"Закрыто приложение '{application_name}'.")
        except Exception as e:
            va_speak(f"Произошла ошибка при закрытии окна {application_name}: {str(e)}")
    
    # Попытка завершения процесса с использованием команды taskkill
    try:
        subprocess.run(["taskkill", "/F", "/IM", application_name + ".exe"], check=True)
    except subprocess.CalledProcessError:
        va_speak(f"Приложение '{application_name}' не было найдено.")
    except Exception as e:
        print(f"Произошла ошибка при закрытии приложения '{application_name}': {str(e)}")

def more_generate_picture(user_input):
    keywords = ["нарисуй", "сделай", "сгенерируй", "генерируй", 'сгенерировать', 'сгенерируйте',
        "нарисуй мне", "сделай мне", "сгенерируй мне", "генерируй мне", 'сгенерировать мне', 'сгенерируйте мне',
        "мне нарисуй", "мне сделай", "мне сгенерируй", "мне генерируй", 'мне сгенерировать', 'мне сгенерируйте',
        'но рисуем', 'но рисуем мне', 'мне', 'рисуй', 'рисуем']

    for phrase in keywords:
        user_input = user_input.replace(phrase, "").strip()

    if prompt_picture != '':
        try:
            va_speak("Генерирую изображение")
            resp = Client.create_generation("prodia", prompt_picture)
            va_speak("Изображение готово")
            Image.open(BytesIO(resp)).show()
        except Exception as e:
            va_speak("Переключаюсь на другую модель")
            try:
                va_speak("Генерирую изображение")
                resp = Client.create_generation("prodia", prompt_picture)
                va_speak("Изображение готово")
                Image.open(BytesIO(resp)).show()
            except Exception as e:
                va_speak("Произошла непредвиденная ошибка")
    else:
        va_speak("Задайте запрос для генерации еще одного изображения")

def search_wikipedia(query):
    encoded_query = quote(query)
    url = f"https://ru.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={encoded_query}&utf8=&converttitles="
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        page_id = next(iter(data['query']['pages']))

        if page_id != '-1':
            extract = data['query']['pages'][page_id]['extract']
            extract = re.sub(r"\(.*?\)", "", extract)
            extract = re.sub(r"\[.*?\]", "", extract)
            extract = replace_language_names(extract)

            if extract:
                paragraphs = extract.split('\n\n')[:2]
                return paragraphs
            else:
                think = random.choice(thinking)
                va_speak(think)
                get_gpt_response(query, user_va_speak)
        else:
            return None
    else:
        return ["Проверьте доступ в интернет и повторите свой запрос."]

def log_error(log_file_path, file_name, error):
    current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open(log_file_path, "a") as log_file:
        log_file.write(f"[{current_time}] Error deleting {file_name}: {error}\n")

def translate_text(text, source_lang, target_lang):
    try:
        translator = Translator()
        translated_text = translator.translate(text, src=source_lang, dest=target_lang)
        return translated_text.text
    except Exception as e:
        va_speak("Произошла ошибка в переводе текста")
        return text            

def detect_language(text):
    try:
        detected_lang = detect(text)
        return detected_lang
    except Exception as e:
        va_speak("Произошла ошибка в распознавании речи")
        return None

def convert_roman_numerals(text):
    words = text.split()
    for i in range(len(words)):
        try:
            arabic_numeral = roman.fromRoman(words[i].upper())
            words[i] = str(arabic_numeral)
        except roman.InvalidRomanNumeralError:
            pass
    return ' '.join(words)

def translate_sentences(input_text, src_lang, dest_lang):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', input_text)
        
    translated_sentences = []
    translator = Translator()
    
    for sentence in sentences:
        if sentence.strip():
            translated_sentence = translator.translate(sentence, src=src_lang, dest=dest_lang).text
            translated_sentences.append(translated_sentence)
    
    translated_text = ' '.join(translated_sentences)
    
    return translated_text

def save_response_to_file(response):
    if response is not None and isinstance(response, str):
        bot_helper_path = os.path.join(os.path.expanduser("~"), "Documents", "BotHelper")
        current_time = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
        file_name = os.path.join(bot_helper_path, f"Code_ChatGPT-{current_time}.txt")
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response)
        
        os.startfile(file_name)

def save_response_to_file_text(response):
    if response is not None and isinstance(response, str):
        bot_helper_path = os.path.join(os.path.expanduser("~"), "Documents", "BotHelper")
        current_time = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
        file_name = os.path.join(bot_helper_path, f"Text_ChatGPT-{current_time}.txt")
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response)
        
        os.startfile(file_name)

def load_chat_history():
    history_file = os.path.join(bot_helper_path, f"chat_history.txt")
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as file:
            chat_history = file.read()
        return chat_history
    else:
        return ""
        
def save_chat_history(chat_history):
    history_file = os.path.join(bot_helper_path, f"chat_history.txt")
    with open(history_file, "a", encoding="utf-8") as file:
        file.write(chat_history + "\n")

def clear_chat_history():
    history_file = os.path.join(bot_helper_path, f"chat_history.txt")
    if os.path.exists(history_file):
        os.remove(history_file)

def search_in_google(query, user_va_speak):
    user_va_speak.configure(text='Ищу информацию в интернете...')
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
    # except Exception as e:
    #     logging.error(f"Exception in extract_cleaned_text_from_website: {e}")

def clean_text(text):
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = re.sub(r'\[[^\]]+\]', '', cleaned_text)
    cleaned_text = re.sub(r'Сомнительна связь.*', '', cleaned_text)
    cleaned_text = re.sub(r'Использованы данные словаря.*', '', cleaned_text)
    cleaned_text = re.sub(r'\([^)]*\)', '', cleaned_text)
    return cleaned_text.strip()

def format_text(text, user_va_speak):
    user_va_speak.configure(text='Ищу информацию в интернете...')
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    formatted_text = ' '.join(sentences)
    return formatted_text

def generate_response(user_question, texts, user_va_speak):
    user_va_speak.configure(text='Ищу информацию в интернете...')
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

def get_random_user_agent(user_va_speak):
    user_va_speak.configure(text='Ищу информацию в интернете...')
    user_agent_file_path = "user-agents.txt"
    try:
        with open(user_agent_file_path, 'r') as file:
            user_agents = file.read().splitlines()
        return random.choice(user_agents)
    except Exception as e:
        logging.error(f"Exception in get_random_user_agent: {e}")
        return None

def get_gpt_response(input_text, user_va_speak):
    global input_text_2
    try:
        if web_search == True:
            user_va_speak.configure(text='Ищу информацию в интернете...')
            user_question = input_text.strip().lower()
            search_results = search_in_google(user_question, user_va_speak)

            if search_results:
                extracted_texts = []
                threads = []

                for i, result in enumerate(search_results):
                    user_agent = get_random_user_agent(user_va_speak)
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

                # Ждем завершения всех потоков
                for thread in threads:
                    thread.join()

                response = generate_response(user_question, extracted_texts, user_va_speak)

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
            else:
                pass
        else:
            pass

        chat_history = load_chat_history()
        
        text_from_ethernet = f'Информация из интернета: {current_message.strip()}\nОтвечай по русски.'

        input_text_2 = f'{chat_history} {input_text}. {text_from_ethernet}'
        input_text_3 = f'{chat_history} {input_text}'

        try:
            user_va_speak.configure(text='Генерирую ответ...')
            from g4f.client import Client
            client_2 = Client()
            try:
                response = client_2.chat.completions.create(model='gemini-pro', messages=[{"role": "user", "content": input_text_2}])
                response_text = response.choices[0].message.content
            except:
                response = client_2.chat.completions.create(model='airoboros-70b', messages=[{"role": "user", "content": input_text_2}])
                response_text = response.choices[0].message.content

            user_va_speak.configure(text=limit_text_length(f'Вы сказали: {input_text}'))

            history_response = f'Я: {input_text}\nТы: {response_text}'
            save_chat_history(history_response)

            try:
                if detect(response_text) != 'ru':
                    response_text = translate_sentences(response_text, src_lang='en', dest_lang='ru')
            except:
                pass

            user_va_speak.configure(text='Ожидайте...')
            va_speak(response_text)
            user_va_speak.configure(text='Говорите...')

        except (g4f.errors.RetryProviderError, aiohttp.client_exceptions.ClientResponseError):
            clear_chat_history()
            va_speak(current_message.strip())

    except (TypeError, RuntimeError, TimeoutError):
        pass

    except g4f.errors.RetryProviderError:
        clear_chat_history()
        va_speak('Произошла ошибка при генерации ответа. Я очищу историю чата и попробуйте задать вопрос заново.')
    
    # except Exception as e:
    #    clear_chat_history()
    #    print(e)
    #    va_speak('У вас слишком большая история чата. Я очищу историю чата и попробуйте задать вопрос заново.')