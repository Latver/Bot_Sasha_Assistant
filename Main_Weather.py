from tkinter import StringVar, ttk
import customtkinter as ctk
import win32api, requests, datetime

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

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

def Weather(window, window_other_menu):
    global window_weather

    font = ctk.CTkFont(family='Arial', size=20)
    
    def update_combobox(*args):
        # Обновляем значения в комбобоксе и получаем значение из поля ввода
        current_text = edit_city.get().lower()

        # Фильтруем список городов по значению в поле ввода
        filtered_cities = [city for city in cities if current_text in city.lower()]

        # Обновляем значения в выпадающем списке
        combobox_city['values'] = filtered_cities

    def get_weather(*args):
        global treeview

        try:
            treeview.destroy()
        except (NameError, AttributeError):
            pass

        label_weather.place(x=130, y=100)
        window_weather.geometry(f"418x130+{center_x - int(window_width / 1.2)}+{center_y - int(window_height / 3)}")

        # Одна точка
        label_weather.configure(text="Загрузка погоды.")
        window_weather.update()

        city = edit_city.get()
        api_key = "26aecdf5b56cf2b82e37bdac6985cff6"
        geocode_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
        response = requests.get(geocode_url)
        if city == "":
            label_weather.configure(text="Вы не ввели город")
        elif response.status_code == 200:
            location_data = response.json()
            if location_data:
                
                # Две точки
                label_weather.configure(text="Загрузка погоды..")
                window_weather.update()

                lat = location_data[0]["lat"]
                lon = location_data[0]["lon"]
                url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={api_key}&lang=ru"
                response = requests.get(url)
                if response.status_code == 200:

                    window_weather.geometry(f"893x300+{center_x - int(window_width / 0.55)}+{center_y - int(window_height / 3)}")
                    
                    # Три точки
                    label_weather.configure(text="Загрузка погоды...")
                    window_weather.update()

                    weather_data = response.json()
                    forecast = ''

                    # Создаем фрейм с Treeview и заголовками столбцов
                    treeview = ttk.Treeview(window_weather)
                    treeview['columns'] = ['weather', 'temp_min', 'temp_max', 'feels_like', 'pressure', 'humidity', 'wind_speed']
                    treeview.heading('#0', text='День')
                    treeview.heading('weather', text='Погода')
                    treeview.heading('temp_min', text='Мин. темп., °C')
                    treeview.heading('temp_max', text='Макс. темп., °C')
                    treeview.heading('feels_like', text='Ощущается, °C')
                    treeview.heading('pressure', text='Давление, мм рт. ст.')
                    treeview.heading('humidity', text='Влажность, %')
                    treeview.heading('wind_speed', text='Скорость ветра, м/с')

                    treeview.column('#0', width=100)
                    treeview.column('weather', width=150)
                    treeview.column('temp_min', width=100)
                    treeview.column('temp_max', width=100)
                    treeview.column('feels_like', width=100)
                    treeview.column('pressure', width=120)
                    treeview.column('humidity', width=100)
                    treeview.column('wind_speed', width=120)

                    treeview.grid(column=0, row=3)

                    label_weather.configure(text="")

                    # Добавляем строки с данными
                    for day in weather_data["daily"]:
                        timestamp = day["dt"]
                        date = datetime.datetime.fromtimestamp(timestamp)
                        day_of_week = date.strftime("%A").replace("Monday", "Понедельник").replace("Tuesday", "Вторник").replace("Wednesday", "Среда").replace("Thursday", "Четверг").replace("Friday", "Пятница").replace("Saturday", "Суббота").replace("Sunday", "Воскресенье")
                        weather = day["weather"][0]["description"]
                        temp_min = round(day["temp"]["min"] - 273.15, 1)
                        temp_max = round(day["temp"]["max"] - 273.15, 1)
                        feels_like = round(day["feels_like"]["day"] - 273.15, 1)
                        pressure = round(day["pressure"] * 0.750062, 1)
                        humidity = day["humidity"]
                        wind_speed = round(day["wind_speed"], 1)
                        treeview.insert('', 'end', text=day_of_week, values=(weather, f"{temp_min:.1f}", f"{temp_max:.1f}", f"{feels_like:.1f}", f"{pressure:.1f}", f"{humidity} %", f"{wind_speed} м/с"))
                    treeview.grid(column=0, row=3)
                else:
                    label_weather.configure(text="Не удалось получить прогноз погоды\n")
                    label_weather.configure(text=label_weather.cget("text") + "Проверьте доступ в интернет")
                    window_weather.geometry(f"418x200+{center_x - int(window_width / 1.2)}+{center_y - int(window_height / 3)}")
                    label_weather.place(x=10, y=120)
            else:
                label_weather.configure(text="Не удалось найти координаты города\n")
                label_weather.configure(text=label_weather.cget("text") + "Проверьте правильность написания города")
                window_weather.geometry(f"418x200+{center_x - int(window_width / 1.2)}+{center_y - int(window_height / 3)}")
                label_weather.place(x=10, y=120)
        else:
            label_weather.configure(text="Не удалось найти город\n")
            label_weather.configure(text=label_weather.cget("text") + "Попробуйте снова нажать кнопку или проверьте правильность написания города")
            window_weather.geometry(f"418x200+{center_x - int(window_width / 1.2)}+{center_y - int(window_height / 3)}")
            label_weather.place(x=10, y=120)

    def exit_window_weather():
        try:
            window_other_menu.deiconify()
            window_weather.destroy()
            window_weather.quit()
        except (NameError, AttributeError):
            window.deiconify()
            window_weather.destroy()
            window_weather.quit()

    def select_city(event):
        value = event.widget.get()
        var_city.set(value)

    def on_mousewheel(event):
        try:
            combobox_city.yview_scroll(int(-1*(event.delta/120)), "units")
        except AttributeError:
            pass

    try:
        window_other_menu.withdraw()
    except NameError:
        window.withdraw()
    except AttributeError:
        window.withdraw()
    except TclError:
        window.deiconify()

    window_weather = ctk.CTk()
    window_weather.title("Погода")
    window_weather.resizable(width=False, height=False)
    window_weather.protocol('WM_DELETE_WINDOW', exit_window_weather)
    window_weather.geometry(f"418x100+{center_x - int(window_width / 1.2)}+{center_y - int(window_height / 3)}")

    # Создаем виджеты
    label_city = ctk.CTkLabel(window_weather, text="Введите город")
    label_weather = ctk.CTkLabel(window_weather, text="")
    combobox_label = ctk.CTkLabel(window_weather, text="Выберите город")

    # Создаем выпадающий список
    var_city = StringVar()

    # Задаем первый элемент списка как значение по умолчанию
    var_city.set(cities[0])
    combobox_city = ttk.Combobox(window_weather)
    var_city.set(combobox_city.get())

    # Список вариантов для комбобокса
    combobox_city['values'] = cities

    # Кнопка получения погоды
    button_weather = ctk.CTkButton(window_weather, text="Получить погоду", command=get_weather)

    # Поле для ввода города
    edit_city = ctk.CTkEntry(window_weather, justify='center')

    # Надпись "Введите город"
    label_city.grid(column=0, row=0, padx=5, pady=2, sticky='we')
    # Поле для ввода города
    edit_city.grid(column=0, row=0, padx=165, pady=2, sticky='w')
    # Надпись "Выберите город"
    combobox_label.grid(column=0, row=1, padx=5, pady=2, sticky='we')
    # Комбобокс
    combobox_city.grid(column=0, row=1, padx=165, pady=2, sticky='w')
    # Кнопка получения погоды
    button_weather.grid(column=0, row=2, padx=5, pady=2, sticky='w')
    # Пустое поле для очистки ошибок
    label_weather.grid(column=1, row=3, padx=5, pady=2, sticky='we')

    label_city.configure(font=font, anchor="w")
    label_weather.configure(font=font)
    combobox_label.configure(font=font, anchor="w")
    combobox_city.configure(font=('Arial 14 bold'), textvariable=var_city, width=21)
    button_weather.configure(font=font, width=408)
    edit_city.configure(font=font, width=250, textvariable=var_city)

    edit_city.bind("<Return>", get_weather)
    edit_city.bind('<KeyRelease>', update_combobox)
    combobox_city.bind("<Return>", get_weather)
    combobox_city.bind('<KeyRelease>', update_combobox)
    combobox_city.bind("<MouseWheel>", on_mousewheel)
    combobox_city.bind("<<ComboboxSelected>>", select_city)

    # Запускаем главный цикл приложения
    window_weather.mainloop()