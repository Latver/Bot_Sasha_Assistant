import re, webbrowser, os, random, datetime, threading, difflib, requests

from Speak import va_speak, unpause_audio, stop_audio, pause_audio
from Main_GPT import get_gpt_response, generate_picture, more_generate_picture, clear_chat_history, close_application, open_application, read_path_from_file, find_and_execute_shortcut, find_best_matching_application, search_wikipedia, save_response_to_file, save_response_to_file_text
from System_Windows import cmds, autoloading, regedit, services, appdata, device_manager, finish_process
from Browser import sites_open
from Guess_the_Word import create_widgets
from Snake import gameLoop
from Tic_Tac_Toe import tic_tac_toe
from Arcanoid import arcanoid

bot_helper_dir = os.path.expanduser("~\\Documents\\BotHelper")
bot_helper_path_app = os.path.join(bot_helper_dir, "saved_app_path.txt")
app_paths = {}

thinking = ["Дайте подумать.", "Ищу ответ.", "Размышляю над этим.", "Ищу правильный ответ.", "Обработка информации.", "Пытаюсь найти наилучший ответ.", "В поиске нужной информации.",
"Провожу анализ.", "Ищу подходящую информацию.", "Рассматриваю варианты.", "Пытаюсь сформулировать ответ.", "Дайте пару секунд. Я думаю.", "Думаю.", "Дайте пару секунд.",
"Произвожу поиск в базе данных.", "Разбираюсь в вопросе.", "Раздумываю над ответом.", "Анализирую ваш вопрос.", "Фокусируюсь на вопросе."]

Thanks = ["Пожалуйста, рада была помочь.", "Не стоит благодарности, я всегда готова прийти на помощь.", "Рада, что смогла быть полезной.",
"Не за что, я сделала все возможное.", "Рада, что моя помощь была ценной.", "Всегда готова оказать помощь.", "Не нужно благодарности, это моя работа.",
"Очень приятно было помочь вам.", "Без проблем, рада была помочь.", "Спасибо вам за доверие.", "Рада была быть полезной.", "Не за что, это было для меня легким делом.",
"Очень приятно, что я смогла помочь.", "Не стоит благодарности.", "Без проблем, это было для меня приятным опытом.", "Рада была быть полезной, спасибо за приятные слова.",
"Рада была принести пользу, это моя цель.", "Не за что, это моя работа - помогать.", "Очень приятно услышать слова благодарности, спасибо вам.",
"Не нужно благодарности, я всегда готова поддержать.", "Без проблем, это было для меня интересным заданием.", "Рада была быть полезной, спасибо за возможность помочь вам."]

cities = ['Абакан', 'Азов', 'Александров', 'Алексин', 'Альметьевск', 'Анапа', 'Ангарск', 'Анжеро-Судженск', 'Апатиты', 'Арзамас', 'Армавир', 'Арсеньев', 'Артем', 'Архангельск', 'Асбест', 'Астрахань', 'Ачинск',
'Балаково', 'Балахна', 'Балашиха', 'Балашов', 'Барнаул', 'Батайск', 'Белгород', 'Белебей', 'Белово', 'Белогорск', 'Белорецк', 'Белореченск', 'Бердск', 'Березники', 'Березовский', 'Бийск', 'Биробиджан', 'Благовещенск', 'Бор', 'Борисоглебск', 'Боровичи', 'Братск', 'Брянск', 'Бугульма', 'Буденновск', 'Бузулук', 'Буйнакск', 
'Великие Луки', 'Великий Новгород', 'Верхняя Пышма', 'Видное', 'Владивосток', 'Владикавказ', 'Владимир', 'Волгоград', 'Волгодонск', 'Волжск', 'Волжский', 'Вологда', 'Вольск', 'Воркута', 'Воронеж', 'Воскресенск', 'Воткинск', 'Всеволожск', 'Выборг', 'Выкса', 'Вязьма,' 
'Гатчина', 'Геленджик', 'Георгиевск', 'Глазов', 'Горно-Алтайск', 'Грозный', 'Губкин', 'Гудермес', 'Гуково', 'Гусь-Хрустальный', 
'Дербент', 'Дзержинск', 'Димитровград', 'Дмитров', 'Долгопрудный', 'Домодедово', 'Донской', 'Дубна', 
'Евпатория', 'Егорьевск', 'Ейск', 'Екатеринбург', 'Елабуга', 'Елец', 'Ессентуки', 
'Железногорск', 'Жигулевск', 'Жуковский',
'Заречный', 'Зеленогорск', 'Зеленодольск', 'Златоуст', 
'Иваново', 'Ивантеевка', 'Ижевск, Избербаш', 'Иркутск', 'Искитим', 'Ишим', 'Ишимбай', 
'Йошкар-Ола',
'Казань', 'Калининград', 'Калуга', 'Каменск-Уральский', 'Каменск-Шахтинский', 'Камышин', 'Канск', 'Каспийск', 'Кемерово', 'Керчь', 'Кинешма', 'Кириши', 'Киров', 'Кирово-Чепецк', 'Киселевск', 'Кисловодск', 'Клин', 'Клинцы', 'Ковров', 'Когалым', 'Коломна', 'Комсомольск-на-Амуре', 'Копейск', 'Королев', 'Кострома', 'Котлас', 'Красногорск', 'Краснодар', 'Краснокаменск', 'Краснокамск', 'Краснотурьинск', 'Красноярск', 'Кропоткин', 'Крымск', 'Кстово', 'Кузнецк', 'Кумертау', 'Кунгур', 'Курган', 'Курск', 'Кызыл', 'Лабинск', 
'Лениногорск', 'Ленинск-Кузнецкий', 'Лесосибирск', 'Липецк', 'Лиски', 'Лобня', 'Лысьва', 'Лыткарино', 'Люберцы', 
'Магадан', 'Магнитогорск', 'Майкоп', 'Махачкала', 'Междуреченск', 'Мелеуз', 'Миасс', 'Минеральные Воды', 'Минусинск', 'Михайловка', 'Михайловск', 'Мичуринск', 'Москва', 'Мурманск', 'Муром', 'Мытищи', 'Малышева',
'Набережные Челны', 'Назарово', 'Назрань', 'Нальчик', 'Наро-Фоминск', 'Находка', 'Невинномысск', 'Нерюнгри', 'Нефтекамск', 'Нефтеюганск', 'Нижневартовск', 'Нижнекамск', 'Нижний Новгород', 'Нижний Тагил', 'Новоалтайск', 'Новокузнецк', 'Новокуйбышевск', 'Новомосковск', 'Новороссийск', 'Новосибирск', 'Новотроицк', 'Новоуральск', 'Новочебоксарск', 'Новочеркасск', 'Новошахтинск', 'Новый Уренгой', 'Ногинск', 'Норильск', 'Ноябрьск', 'Нягань', 
'Обнинск', 'Одинцово', 'Озерск', 'Октябрьский', 'Омск', 'Орел', 'Оренбург', 'Орехово-Зуево', 'Орск', 
'Павлово', 'Павловский Посад', 'Пенза', 'Первоуральск', 'Пермь', 'Петрозаводск', 'Петропавловск-Камчатский', 'Подольск', 'Полевской', 'Прокопьевск', 'Прохладный', 'Псков', 'Пушкино', 'Пятигорск', 
'Раменское', 'Ревда', 'Реутов', 'Ржев', 'Рославль', 'Россошь', 'Ростов-на-Дону', 'Рубцовск', 'Рыбинск', 'Рязань', 
'Салават', 'Сальск', 'Самара', 'Санкт-Петербург', 'Саранск', 'Сарапул', 'Саратов', 'Саров', 'Свободный', 'Севастополь', 'Северодвинск', 'Северск', 'Сергиев Посад', 'Серов', 'Серпухов', 'Сертолово', 'Сибай', 'Симферополь', 'Славянск-на-Кубани', 'Смоленск', 'Соликамск', 'Солнечногорск', 'Сосновый Бор', 'Сочи', 'Ставрополь', 'Старый Оскол', 'Стерлитамак', 'Ступино', 'Сургут', 'Сызрань', 'Сыктывкар', 
'Таганрог', 'Тамбов', 'Тверь', 'Тимашевск', 'Тихвин', 'Тихорецк', 'Тобольск', 'Тольятти', 'Томск', 'Троицк', 'Туапсе', 'Туймазы', 'Тула', 'Тюмень', 
'Узловая', 'Улан-Удэ', 'Ульяновск', 'Урус-Мартан', 'Усолье-Сибирское', 'Уссурийск', 'Усть-Илимск', 'Уфа', 'Ухта', 
'Феодосия', 'Фрязино', 
'Хабаровск', 'Ханты-Мансийск', 'Хасавюрт', 'Химки', 
'Чайковский', 'Чапаевск', 'Чебоксары', 'Челябинск', 'Черемхово', 'Череповец', 'Черкесск', 'Черногорск', 'Чехов', 'Чистополь', 'Чита', 
'Шадринск', 'Шали', 'Шахты', 'Шуя', 
'Щекино', 'Щелково',
'Электросталь', 'Элиста', 'Энгельс', 
'Южно-Сахалинск', 'Юрга, Якутск',
'Ялта', 'Ярославль']

window = None
window_game_menu = None

def get_weather(city):
    api_key = '26aecdf5b56cf2b82e37bdac6985cff6'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data

def get_similar_city(city):
    matches = difflib.get_close_matches(city, cities)
    if matches:
        return matches[0]
    return None

def translate_weekday(weekday):
    russian_weekdays = {
        'Monday': 'понедельник',
        'Tuesday': 'вторник',
        'Wednesday': 'среда',
        'Thursday': 'четверг',
        'Friday': 'пятница',
        'Saturday': 'суббота',
        'Sunday': 'воскресенье'
    }
    return russian_weekdays.get(weekday, '')

def handle_user_message(user_input, user_va_speak):
    global context

    if any(phrase in user_input.lower() for phrase in ["погода", "погоду", "погодe"]):
        keywords = ['город', 'городе', "города", "городу"]
        for keyword in keywords:
            user_input = user_input.replace(keyword, '')
        city = user_input.split()[-1].strip()
        similar_city = get_similar_city(city)
        if similar_city:
            weather_data = get_weather(similar_city)
            if 'weather' in weather_data:
                description = weather_data['weather'][0]['description']
                temperature = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                wind_speed = weather_data['wind']['speed']
                clouds_percent = weather_data['clouds']['all']
                temperature = weather_data['main']['temp']
                temperature_parts = str(temperature).split('.')
                temperature_text = ' и '.join(temperature_parts) + " градусов по цельсию"
                humidity_text = f"{humidity}процентов"
                wind_speed_text = f"{wind_speed} метров в секунду"
                clouds_text = f"{clouds_percent}процентов"

                weather_phrases = {
                    "clear sky": "ясное небо",
                    "few clouds": "небольшая облачность",
                    "scattered clouds": "рассеянная облачность",
                    "broken clouds": "облачно с прояснениями",
                    "overcast clouds": "затянутое небо",
                    "shower rain": "легкий дождь",
                    "light rain": "небольшой дождь",
                    "rain": "дождь",
                    "thunderstorm": "гроза",
                    "snow": "снег",
                    "mist": "туман"}
                if description in weather_phrases:
                    description_ru = weather_phrases[description]
                else:
                    description_ru = description

                va_speak(f"Погода в городе {similar_city} {description_ru}. Температура {temperature_text}. "
                      f"Влажность {humidity_text}. Ветер {wind_speed_text}. Облачность {clouds_text}.")
            else:
                va_speak("Не удалось получить информацию о погоде.")

    elif re.search(r'\bдат[ау]\b', user_input):
        current_date = datetime.datetime.now().strftime("%d.%m.%Y")
        va_speak(f"Сегодня {current_date}.")
    elif re.search(r'\bвремя\b', user_input):
        current_time = datetime.datetime.now().strftime("%H:%M")
        va_speak(f"Сейчас {current_time}.")
    elif re.search(r'\bдень\s+недели\b', user_input):
        current_day = datetime.datetime.now().strftime("%A")
        russian_day = translate_weekday(current_day)
        va_speak(f"Сегодня {russian_day}.")

    elif any(phrase in user_input.lower() for phrase in ["коде", "кода", "код", "коду", "напиши коде", "напиши кода", "напиши код", "напиши коду"]):
        think = random.choice(thinking)
        va_speak(think)
        gpt_response = get_gpt_response(user_input, user_va_speak)
        save_response_to_file(gpt_response)
    elif any(phrase in user_input.lower() for phrase in ["напиши", "пиши", "перепиши", "запиши", "напишу", "пишу", "перепишу", "запишу", "написать", "писать", "переписать", "записать",
                                                         "на пиши", "пиши", "пере пиши", "за пиши", "на пишу", "пишу", "пере пишу", "за пишу", "на писать", "писать", "пере писать", "за писать"]):
        think = random.choice(thinking)
        va_speak(think)
        gpt_response = get_gpt_response(user_input, user_va_speak)
        save_response_to_file_text(gpt_response)

    elif any(phrase in user_input.lower() for phrase in ["спасибо", "спасиба", "спасиб", "благодарю", "благодарствую", 
        "саша спасибо", "саша спасиба", "саша спасиб", "саша благодарю", "саша благодарствую",
        "спасибо саша", "спасиба саша", "спасиб саша", "благодарю саша", "благодарствую саша",
        "саш спасибо", "саш спасиба", "саш спасиб", "саш благодарю", "саш благодарствую",
        "спасибо саш", "спасиба саш", "спасиб саш", "благодарю саш", "благодарствую саш"]):
        thank = random.choice(Thanks)
        va_speak(thank)

    elif any(word == user_input.lower() for word in ["стоп", "стой", "постой", "по стой", "хватит", "остановись", "замолчи", "не говори", "помолчи", "заткнись"]):
        stop_audio()
    elif any(word == user_input.lower() for word in ["подожди", "пауза", "тихо", "жди", "погоди"]):
        pause_audio()
    elif any(word == user_input.lower() for word in ["говори", "продолжай", "дальше", "рассказывай", "продолжим"]):
        unpause_audio()

    elif any(word == user_input.lower() for word in ["очисти", "очисти историю", "почисти", "почисти историю", "забудь о чем говорили", "забудь", "новый диалог", "новую диалог", "новым диалог", "новые диалог", "забудь разговор", "забудь наш разговор",
        "саша забудь", "саша очисти", "саша почисти", "саша очисти историю", "саша почисти историю", "саша забудь о чем говорили", "саша новый диалог", "саша забудь разговор", "саша забудь наш разговор",
        "давай начнем новый диалог", "саша давай начнем новый диалог", "давай начнем новым диалог", "саша давай начнем новым диалог", "давай начнем новую диалог", "саша давай начнем новую диалог", "давай начнем новые диалог", "саша давай начнем новые диалог"]):
        va_speak('Хорошо, давайте начнем новый диалог')
        clear_chat_history()

    elif any(word == user_input.lower() for word in ["алло", "ты здесь", "здесь", "ты тут", "тут", "прием", "але", "где ты",
        "саша алло", "саша ты здесь", "саша тут", "саша прием", "саша але", "саша где ты", "саша здесь", "саша ты тут", "саша",
        "саш алло", "саш ты здесь", "саш тут", "саш прием", "саш але", "саш где ты", "саш здесь", "саш ты тут", "саш",
        "сша алло", "сша ты здесь", "сша тут", "сша прием", "сша але", "сша где ты", "сша здесь", "сша ты тут", "сша",
        'сажать здесь', "что здесь"]):
        threading.Thread(target=va_speak("Да, я здесь")).start()

    # Выключение
    elif any(phrase in user_input.lower() for phrase in ["выключить компьютер через", "выключи компьютер через", "выключи работу через", "выключить работу через"]):
        remaining_time = None
        try:
            words = user_input.split()
            for i, word in enumerate(words):
                if word.isdigit() and i < len(words) - 1 and words[i+1] in ["секунд", "секунду", "секунды", "сек"]:
                    remaining_time = int(word)
                    if len(words) == 1:
                        threading.Thread(target=va_speak(f'Ваш компьютер выключится через {word} секунду')).start()
                    elif len(words) <= 4:
                        threading.Thread(target=va_speak(f'Ваш компьютер выключится через {word} секунды')).start()
                    else:
                        threading.Thread(target=va_speak(f'Ваш компьютер выключится через {word} секунд')).start()
                    break
                elif word.isdigit() and i < len(words) - 1 and words[i+1] in ["минут", "минуту", "минуты", "мин"]:
                    remaining_time = int(word) * 60
                    if len(words) == 1:
                        threading.Thread(target=va_speak(f'Ваш компьютер выключится через {word} минуту')).start()
                    elif len(words) <= 4:
                        threading.Thread(target=va_speak(f'Ваш компьютер выключится через {word} минуты')).start()
                    else:
                        threading.Thread(target=va_speak(f'Ваш компьютер выключится через {word} минут')).start()
                    break
                elif word.isdigit() and i < len(words) - 1 and words[i+1] in ["час", "часа","часов"]:
                    remaining_time = int(word) * 3600
                    if len(words) == 1:
                        threading.Thread(target=va_speak(f'Ваш компьютер выключится через {word} час')).start()
                    elif len(words) <= 4:
                        threading.Thread(target=va_speak(f'Ваш компьютер выключится через {word} часа')).start()
                    else:
                        threading.Thread(target=va_speak(f'Ваш компьютер выключится через {word} часов')).start()
                    break
            if remaining_time is not None:
                os.system(f"shutdown /s /t {remaining_time} /f")
            else:
                threading.Thread(target=va_speak("Не удалось распознать время")).start()
        except WindowsError:
            threading.Thread(target=va_speak("Произошла ошибка при выключении компьютера")).start()

    elif any(phrase in user_input.lower() for phrase in ["выключить компьютер", "выключи компьютер", "выключи комп", "выключить пк", "выключи пк"]):
        os.system("shutdown /s /t 1 /f")

    elif any(phrase in user_input.lower() for phrase in ["отмени выключение", 'отменить выключение', 'отменить выключения', 'отмени выключения', 'так и не выключение', 'отмена выключения']):
        threading.Thread(target=va_speak('Отменила выключение')).start()
        stop()

    # Перезагрузка
    elif any(phrase in user_input.lower() for phrase in ["перезагрузить компьютер через", "перезагрузи компьютер через", "перезагрузи работу через", "перезагрузить работу через", 'перезагрузка компьютера через', 'перезагрузка пк через']):
        remaining_time = None
        try:
            words = user_input.split()
            for i, word in enumerate(words):
                if word.isdigit() and i < len(words) - 1 and words[i+1] in ["секунд", "секунду", "секунды", "сек"]:
                    remaining_time = int(word)
                    if len(words) == 1:
                        threading.Thread(target=va_speak(f'Ваш компьютер перезагрузиться через {word} секунду')).start()
                    elif len(words) <= 4:
                        threading.Thread(target=va_speak(f'Ваш компьютер перезагрузиться через {word} секунды')).start()
                    else:
                        threading.Thread(target=va_speak(f'Ваш компьютер перезагрузиться через {word} секунд')).start()
                    break
                elif word.isdigit() and i < len(words) - 1 and words[i+1] in ["минут", "минуту", "минуты", "мин"]:
                    remaining_time = int(word) * 60
                    if len(words) == 1:
                        threading.Thread(target=va_speak(f'Ваш компьютер перезагрузиться через {word} минуту')).start()
                    elif len(words) <= 4:
                        threading.Thread(target=va_speak(f'Ваш компьютер перезагрузиться через {word} минуты')).start()
                    else:
                        threading.Thread(target=va_speak(f'Ваш компьютер перезагрузиться через {word} минут')).start()
                    break
                elif word.isdigit() and i < len(words) - 1 and words[i+1] in ["час", "часа", "часов"]:
                    remaining_time = int(word) * 3600
                    if len(words) == 1:
                        threading.Thread(target=va_speak(f'Ваш компьютер перезагрузиться через {word} час')).start()
                    elif len(words) <= 4:
                        threading.Thread(target=va_speak(f'Ваш компьютер перезагрузиться через {word} часа')).start()
                    else:
                        threading.Thread(target=va_speak(f'Ваш компьютер перезагрузиться через {word} часов')).start()
                    break
            if remaining_time is not None:
                os.system(f"shutdown /r /t {remaining_time} /f")
            else:
                threading.Thread(target=va_speak("Не удалось распознать время")).start()
        except WindowsError:
            threading.Thread(target=va_speak("Произошла ошибка при перезагрузке компьютера")).start()

    elif any(phrase in user_input.lower() for phrase in ["перезагрузить компьютер", "перезагрузи компьютер", "перезагрузить пк", "перезагрузи пк", 'перезагрузка компьютера', 'перезагрузка пк']):
        os.system("shutdown /r /t 1 /f")

    elif any(phrase in user_input.lower() for phrase in ["отмени перезагрузку", 'отменить перезагрузку', 'отменить перезагрузка', 'отмени перезагрузку', 'так и не перезагрузку', 'отмена перезагрузки']):
        threading.Thread(target=va_speak('Отменила перезагрузку')).start()
        stop()

    # Гибернация
    elif any(phrase in user_input.lower() for phrase in ["гибернация", "гибернацию", "гибернация компьютера"]):
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

    # Выход из системы
    elif any(phrase in user_input.lower() for phrase in ["выйди из системы", "выход из системы", "выход из система", "выход системы", "выход и системы", "выход и система", "выйди система", "выйди и системы"]):
        os.system('shutdown /l')

    # Браузер
    # Вк
    elif any(phrase in user_input.lower() for phrase in ["vk", 'и вк', ' и vk', 'в контакте', 'в контакт', 'vkontakte', 'v kontakte', 'v kontakt']):
        va_speak("Включаю вконтакте")
        webbrowser.open_new('https://vk.com/id0')

    # YouTube
    elif any(phrase in user_input.lower() for phrase in ["ю т у б", 'youtube', 'ютуб', 'you tube', 'и youtube', ' и ютуб', 'тут']):
        va_speak("Включаю ютуб")
        webbrowser.open_new('https://www.youtube.com/')

    # Gmail
    elif any(phrase in user_input.lower() for phrase in ["gmail", 'д мэйл', 'г мэйл', 'g mail', 'и gmail', 'почту', 'почте', 'почта', 'почты']):
        va_speak("Включаю джимайл")
        webbrowser.open('https://gmail.com')

    # Переводчик
    elif any(phrase in user_input.lower() for phrase in ["переводчик", 'яндекс переводчик', "гугл переводчик"]):
        va_speak("Включаю переводчик")
        webbrowser.open('https://translate.yandex.ru')

    # Гугл диск
    elif any(phrase in user_input.lower() for phrase in ["google disk", 'google диск', 'гугл диск', 'гугл disk']):
        va_speak("Включаю гугл диск")
        webbrowser.open('https://drive.google.com/drive')

    # Менеджер сайтов
    elif any(phrase in user_input.lower() for phrase in ["менеджер сайт", 'менеджер сайтов', 'manager сайтов', 'manager сайт']):
        va_speak("Включаю менеджер сайтов")
        sites_open(window)

    # CMD
    elif any(phrase in user_input.lower() for phrase in ['терминал', 'терминалу', 'терминала', 'терминалы', 'командная строка', 'командную строку', 'командная строку', 'командную строка']):
        va_speak("Открываю терминал")
        cmds()

    # Папка автозагрузки
    elif any(phrase in user_input.lower() for phrase in ["автозагрузка", 'автозагрузки', 'папка автозагрузки', 'папки автозагрузки', 'папку автозагрузки']):
        va_speak("Открываю папку автозагрузки")
        autoloading()

    # Реестр
    elif any(phrase in user_input.lower() for phrase in ["реестр", 'реестра', 'реестре']):
        va_speak("Открываю реестр")
        regedit()

    # Службы
    elif any(phrase in user_input.lower() for phrase in ["службы", 'служба', 'службу', 'службе']):
        va_speak("Открываю службы")
        services()

    # Диспетчер устройств
    elif any(phrase in user_input.lower() for phrase in ["диспетчер устройств", 'диспетчеру устройств', 'диспетчера устройств', "диспетчер устройства", 'диспетчеру устройству', 'диспетчера устройстве']):
        va_speak("Открываю диспетчер устройств")
        device_manager()

    # Завершить процесс приложения
    elif any(phrase in user_input.lower() for phrase in ["завершить процесс", 'завершение процесса', 'завершен процесс', "процесс", 'процесса', 'процессу']):
        va_speak("Открываю завершение процесса")
        finish_process(window)

    # Автозагрузка программы
    elif any(phrase in user_input.lower() for phrase in ["автозагрузка программы", 'автозагрузку программы', 'автозагрузки программы', "автозагрузка программа", 'автозагрузку программу', 'автозагрузки программе', 
        "авто загрузка программы", 'авто загрузку программы', 'авто загрузки программы', "авто загрузка программа", 'авто загрузку программу', 'авто загрузки программе',
        "загрузка программы", 'загрузку программы', 'загрузки программы', "загрузка программа", 'загрузку программу', 'загрузки программе']):
        va_speak("Включаю автозагрузку программы")
        new_win()
    
    # Настройки ассистента
    elif any(phrase in user_input.lower() for phrase in ["ассистента", 'ассистенту', 'ассистент', "настройки ассистента", 'настройки ассистенту', 'настройки ассистент']):
        va_speak("Включаю настройки ассистента")
        ChatGPT_setting()

    elif any(phrase in user_input.lower() for phrase in ["меню приложений", 'пути приложений', 'путь приложений', "приложений", 'настройки ассистенту', 'настройки ассистент']):
        va_speak("Включаю добавление путей приложений")
        menu_path()

    # Новости
    elif any(phrase in user_input.lower() for phrase in ["новостей", 'новость', 'новости']):
        va_speak("Включаю новости")
        News()

    # Конвертация файлов
    elif any(phrase in user_input.lower() for phrase in ["конверт файлов", 'конвертер файлов', 'конвертация файлов', 'конвертацию файлов','конвертор файлов'
        "конверт файла", 'конвертер файлы', 'конвертация файлов', 'конвертацию файл', 'конвертор файлов', 'конвертации файлов']):
        va_speak("Включаю конвертер файлов")
        converter_files()

    # Угадай слово
    elif any(phrase in user_input.lower() for phrase in ["угадай слово", 'угадать слово', 'отгадай слово', 'отгадать слово']):
        va_speak("Включаю игру угадай слово")
        try:
            create_widgets(window, window_game_menu)
        except (AttributeError, NameError):
            pass

    # Змейка
    elif any(phrase in user_input.lower() for phrase in ["змейку", 'змейка', 'змею', 'змея']):
        va_speak("Включаю игру змейка")
        try:
            gameLoop(window, window_game_menu)
        except (AttributeError, NameError):
            pass

    # Крестики-нолики
    elif any(phrase in user_input.lower() for phrase in ["крестики-нолики", 'крестики нолики', 'крест нолики', 'крести нолики', "крестики ноль", 'крестики нолики', 'крести ноль']):
        va_speak("Включаю игру крестики-нолики")
        try:
            tic_tac_toe(window, window_game_menu)
        except (AttributeError, NameError):
            pass

    # Арканоид
    elif any(phrase in user_input.lower() for phrase in ["арканоид", 'арка ноет']):
        va_speak("Включаю игру арканоид")
        try:
            arcanoid(window, window_game_menu)
        except (AttributeError, NameError):
            pass

    # AI изображение
    elif any(phrase in user_input.lower() for phrase in ['нарисуй еще', 'еще нарисуй', 'сделай еще', 'еще сделай', 'сгенерируй еще', 'еще сгенерируй', 'но рисуем еще', 'еще но рисуем', 'рисуй еще', 'еще рисуй', 'рисуем еще', 'еще рисуем', 'хочу еще', "еще хочу", "давай еще", "еще давай",
                                                         'нарисуй ещё', 'ещё нарисуй', 'сделай ещё', 'ещё сделай', 'сгенерируй ещё', 'ещё сгенерируй', 'но рисуем ещё', 'ещё но рисуем', 'рисуй ещё', 'ещё рисуй', 'рисуем ещё', 'ещё рисуем', 'хочу ещё', "ещё хочу" "давай ещё", "ещё давай"]):
        more_generate_picture(user_input)
    elif any(phrase in user_input.lower() for phrase in ["нарисуй", "сделай", "сгенерируй", "генерируй", 'сгенерировать', 'сгенерируйте',
        "нарисуй мне", "сделай мне", "сгенерируй мне", "генерируй мне", 'сгенерировать мне', 'сгенерируйте мне',
        "мне нарисуй", "мне сделай", "мне сгенерируй", "мне генерируй", 'мне сгенерировать', 'мне сгенерируйте',
        'но рисуем', 'но рисуем мне', 'рисуй', 'рисуем']):
        generate_picture(user_input, user_va_speak)

    # Открытие любых установленных приложений
    elif any(phrase in user_input.lower() for phrase in ['включи', 'открой', 'откройка', 'открой-ка', 'запусти']):
        # Открытие любых установленных приложений
        phrases_to_remove = ['включи', 'открой', 'откройка', 'открой-ка', 'запусти', 'мне', 'игру', 'игра', 'игры', 'игрой', 'программу', 'программы', 'программа', 'программой', 'приложения', 'приложение', 'приложений']
        user_input_lower = user_input.lower()
        for phrase in phrases_to_remove:
            user_input_lower = user_input_lower.replace(phrase, '').strip()
        if user_input_lower:
            app_name = user_input_lower
            read_path_from_file(os.path.join(bot_helper_dir, "saved_app_path.txt"))
            if app_name in app_paths:
                va_speak(f'Включаю {app_name}')
                open_application(app_paths[app_name])
            elif find_and_execute_shortcut(app_name):
                va_speak(f"Включаю '{app_name}'.")
            else:
                va_speak(f'Выполняю поиск программы {app_name}')
                best_matching_app = find_best_matching_application(app_name)
                open_application(best_matching_app)
    
    # Закрытие любых установленных приложений
    elif any(phrase in user_input.lower() for phrase in ['закрыть', 'закрой', 'заверши', 'завершить', 'выключи', 'выключить', 'отключи', 'отключить']):
        app_action = user_input.split(' ', 1)[-1]
        application_name = app_action.strip()
        close_application(application_name, user_input=user_input)

    elif any(phrase in user_input.lower() for phrase in ['что такое', 'что такой', 'что такая', 'кто такой', 'кто такое', 'кто такая',
                                                         'Что такое', 'Что такой', 'Что такая', 'Кто такой', 'Кто такое', 'Кто такая']):
        # Список ключевых фраз
        phrases_to_match = ['что такое', 'что такой', 'что такая', 'кто такой', 'кто такое', 'кто такая', 
                            'Что такое', 'Что такой', 'Что такая', 'Кто такой', 'Кто такое', 'Кто такая']

        # Приведение входного текста к нижнему регистру
        user_input_lower = user_input.lower()

        # Находим первую ключевую фразу, если она есть
        start_index = -1
        for phrase in phrases_to_match:
            index = user_input_lower.find(phrase)
            if index != -1 and (start_index == -1 or index < start_index):
                start_index = index

        # Удаление всех слов до ключевой фразы
        if start_index != -1:
            user_input_lower = user_input_lower[start_index:]

        # Теперь user_input_lower содержит только запрос после ключевой фразы
        user_input_lower = user_input_lower.strip()

        if user_input_lower:
            wikipedia_results = search_wikipedia(user_input_lower)
            if wikipedia_results is not None:
                for paragraph in wikipedia_results:
                    va_speak(paragraph)
            else:
                think = random.choice(thinking)
                user_va_speak.configure(text='Ожидайте...')
                va_speak(think)
                get_gpt_response(user_input, user_va_speak)
    else:
        think = random.choice(thinking)
        va_speak(think)
        get_gpt_response(user_input, user_va_speak)