from datetime import datetime as dt # Для работы с датами и временем
import requests # Для отправки HTTP-запросов
import json # Для работы с JSON-данными
import tkinter # Для создания графического интерфейса (окна приложения)
import tkinter as tk # Для создания графического интерфейса (окна приложения)
from tkinter import font as tkfont # Для работы со шрифтами в tkinter
import subprocess # Для запуска внешних процессов (например, аудиоплеера)
import os # Для работы с операционной системой (например, для перезапуска программы)
import sys # Импорт модуля sys для доступа к некоторым переменным и функциям, взаимодействующим с интерпретатором Python
import time # Для работы со временем (например, для ожидания)
import locale # Для работы с локализацией (например, для отображения даты на русском языке)

def get_prayer_times(): # Функция для получения времени молитвы
    url = "http://api.aladhan.com/v1/timingsByCity?city=Baku&country=Azerbaijan&method=13" # URL API для получения времени молитвы
    response = requests.get(url) # Отправляем GET-запрос к API
    if response.status_code == 200: # Если ответ успешный...
        data = json.loads(response.text) # Парсим JSON-ответ
        timings = data["data"]["timings"] # Извлекаем времена молитв
        selected_timings = {key: timings[key] for key in ["Midnight", "Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]} # Выбираем необходимые времена молитв
        hijri_date = data["data"]["date"]["hijri"]  # Извлекаем хиджрийскую дату
        formatted_hijri_date = f"{hijri_date['day']} {hijri_date['month']['en']} {hijri_date['year']}" # Форматируем хиджрийскую дату
        return selected_timings, formatted_hijri_date # Возвращаем полученные данные
    else:
        return None, None # Если ответ неуспешный, возвращаем None

def get_next_prayer_time(timings_local):  # Функция для получения следующего времени молитвы
    global timings  # теперь timings может быть глобальной переменной
    timings = timings_local  # присваиваем глобальной переменной значение локальной
    next_prayer, next_prayer_time = get_next_prayer_time(timings)  # теперь timings определена
    now_time = dt.now().time() # Получаем текущее время
    timings_next_day = timings.copy()  # Создаем копию словаря timings
    first_prayer = list(timings.values())[0] # Получаем время первой молитвы
    timings_next_day['next_day_first_prayer'] = first_prayer # Добавляем время первой молитвы следующего дня в словарь
    for prayer, time in timings_next_day.items(): # Проходим по всем временам молитвы
        prayer_time = dt.strptime(time, "%H:%M").time() # Преобразуем строку времени в объект datetime.time
        now_time = dt.now().time() # Получаем текущее время
        if now_time < prayer_time: # Если текущее время меньше времени молитвы...
            return prayer, prayer_time # Возвращаем название молитвы и время
    next_day_first_prayer_time = dt.strptime(timings_next_day['next_day_first_prayer'], "%H:%M").time()  # Преобразуем строку времени в объект datetime.time
    return 'next_day_first_prayer', next_day_first_prayer_time # Возвращаем название молитвы и время

def play_audio_file(file_path, use_gui): # Функция для воспроизведения аудиофайла
    FNULL = open(os.devnull, 'w') # Открываем null-устройство для подавления вывода в консоль
    if use_gui: # Если используется графический интерфейс...
        subprocess.Popen(['mpv', '--force-window', file_path], stdout=FNULL, stderr=subprocess.STDOUT, shell=False) # Воспроизводим аудиофайл в новом окне
    else:
        subprocess.Popen(['mpv', file_path], stdout=FNULL, stderr=subprocess.STDOUT, shell=False) # Воспроизводим аудиофайл без нового окна

def create_window(timings, hijri_date): # Функция для создания окна
    window = tk.Tk() # Создаем новое окно
    window.title("Namaz Vaxtları") # Устанавливаем заголовок окна
    window.configure(bg='#222222') # Устанавливаем цвет фона окна

    window.geometry(f'+0+0') # Установка размера и положения окна
    
    bold_font = tkfont.Font(family="DSEG7Classic", size=30, weight="bold")  # Создаем жирный шрифт
    regular_font = tkfont.Font(family="MartianMono", size=30)  # Создаем обычный шрифт
    clock_font = tkfont.Font(family="DSEG7Classic", size=100, weight="bold")  # Создаем шрифт для часов
    date_font = tkfont.Font(family="Comfortaa", size=20, weight="bold")  # Создаем шрифт для даты
    qalanvaxt_font = tkfont.Font(family="Oswald", size=22)  # Создаем шрифт для оставшегося времени
    line_font = tkfont.Font(family="Arial", size=10, weight="bold")  # Создаем шрифт для линий

    az_names = { # Создаем словарь для перевода названий молитв на азербайджанский язык
        "Midnight": " Təhəccüd --",
            "Fajr": " İmsak -----",
         "Sunrise": " Günəş -----",
           "Dhuhr": " Günorta ---",
             "Asr": " İkindi ----",
         "Maghrib": " Axşam -----",
            "Isha": " Gecə ------"
    }

    now_time = dt.now().time()  # Получаем текущее время

    gregorian_date_label = tk.Label(window, font=date_font, bg='#222222', fg='Olive')  # Создаем метку для григорианской даты
    gregorian_date_label.grid(row=2, column=0, columnspan=2)  # Размещаем метку на сетке окна

    hijri_date_label = tk.Label(window, font=date_font, bg='#222222', fg='Olive')  # Создаем метку для хиджрийской даты
    hijri_date_label.grid(row=3, column=0, columnspan=2)  # Размещаем метку на сетке окна

    def update_date():  # Функция для обновления даты
        hijri_date_label.config(text=f"{hijri_date}")  # Обновляем текст метки хиджрийской даты
        locale.setlocale(locale.LC_TIME, "ru_RU.utf8")  # Устанавливаем локализацию на русский язык
        current_date = dt.now().strftime("%A, %d %B %Y")  # Получаем текущую дату
        gregorian_date_label.config(text=f"{current_date} {'года'}")  # Обновляем текст метки григорианской даты

    update_date() # Вызываем функцию обновления даты

    clock_label = tk.Label(window, font=clock_font, bg='#222222', fg='lime', pady=20)  # Создаем метку для часов
    clock_label.grid(row=0, column=0, columnspan=2)  # Размещаем метку на сетке окна

    def update_clock():  # Функция для обновления часов
        current_time = dt.now().strftime("%H:%M")  # Получаем текущее время
        clock_label.config(text=current_time)  # Обновляем текст метки часов
    window.after(1000, update_clock)  # Обновляем часы каждую секунду

    update_clock()  # Вызываем функцию обновления часов

    label_xett1 = tk.Label(window, text=f"――――――――――――――――――――――――――――――――――――――――", font=line_font, bg='#222222', fg='Olive')  # Создаем метку для линии
    label_xett1.grid(row=4, columnspan=2)  # Размещаем метку на сетке окна
    label_qaliq = tk.Label(window, text=f"Növbəti namaza qalan vaxt     ", font=qalanvaxt_font, bg='#222222', fg='Olive', anchor='w')  # Создаем метку для оставшегося времени до следующей молитвы
    label_qaliq_time = tk.Label(window, text="", font=bold_font, bg='#222222', fg='Red', anchor='w')  # Создаем метку для отображения оставшегося времени
    label_qaliq.grid(row=5, column=0, sticky='e', pady=(0,0))  # Размещаем метку на сетке окна
    label_qaliq_time.grid(row=5, column=1, sticky='w', pady=(0,0))  # Размещаем метку на сетке окна
    label_xett2 = tk.Label(window, text=f"――――――――――――――――――――――――――――――――――――――――", font=line_font, bg='#222222', fg='Olive')  # Создаем метку для линии
    label_xett2.grid(row=6, columnspan=2)  # Размещаем метку на сетке окна

    label_names = []  # Создаем список для меток названий молитв
    label_times = []  # Создаем список для меток времен молитв
    for i, (name, time) in enumerate(timings.items()):  # Проходим по всем временам молитв
        label_name = tk.Label(window, text=f"{az_names[name]}", font=regular_font, bg='#222222', fg='Olive', anchor='e')  # Создаем метку для названия молитвы
        label_time = tk.Label(window, text=f"{time}", font=bold_font, bg='#222222', fg='Teal', anchor='w')  # Создаем метку для времени молитвы
        label_name.grid(row=i+7, column=0, sticky='w', pady=(0,5))  # Размещаем метку на сетке окна
        label_time.grid(row=i+7, column=1, sticky='w', pady=(0,5))  # Размещаем метку на сетке окна
        label_names.append(label_name)  # Добавляем метку в список меток названий молитв
        label_times.append(label_time)  # Добавляем метку в список меток времен молитв

    def update_next_prayer_time(timings):  # Функция для обновления времени до следующей молитвы
        global timings  # Делаем timings глобальной переменной
        next_prayer, next_prayer_time = get_next_prayer_time(timings)  # Получаем следующее время молитвы
        if next_prayer_time is not None:  # Если получено время следующей молитвы...
            now_time = dt.now().time()  # Получаем текущее время
            time_difference = dt.combine(dt.today().date(), next_prayer_time) - dt.combine(dt.today().date(), now_time)  # Вычисляем разницу между временем следующей молитвы и текущим временем
            minutes, seconds = divmod(time_difference.seconds, 60)  # Преобразуем разницу во времени в формат минут и секунд
            hours, minutes = divmod(minutes, 60)  # Преобразуем минуты в часы и минуты
            label_qaliq_time.config(text=f"{hours:02d}:{minutes:02d}")  # Обновляем текст метки оставшегося времени

            # Код для воспроизведения аудиофайла
            if (hours == 1 and minutes == 0) or (hours == 0 and minutes == 45) or (hours == 0 and minutes == 30): # Если остался 1 час или 45 или 30 минут до следующей молитвы...
                play_audio_file('audio/AllahuAkbar.mp3', use_gui=False) # Воспроизводим аудиофайл 'AllahuAkbar.mp3'
            if hours == 0 and minutes == 0: # Если время молитвы наступило...
                # Проверяем, какая молитва следующая, и воспроизводим соответствующий аудиофайл
                if next_prayer in ['Midnight', 'Sunrise']: # Если следующая молитва - это полночь или восход...
                    play_audio_file('audio/BismillahFatihSefaragic.mp3', use_gui=False) # Воспроизводим аудиофайл 'BismillahFatihSefaragic.mp3'
                else: # Если следующая молитва - это не полночь и не восход...
                    play_audio_file('audio/AdhanAhmedAlNufais.mp3', use_gui=True) # Воспроизводим аудиофайл 'AdhanAhmedAlNufais.mp3'

        # Код для обновления цвета меток
        for i, (name, time) in enumerate(timings.items()): # Проходим по всем временам молитвы...
            prayer_time = dt.strptime(time, "%H:%M").time() # Преобразуем строку времени в объект datetime.time
            now_time = dt.now().time() # Получаем текущее время
            if now_time < prayer_time: # Если текущее время меньше времени молитвы...
                if i > 0: # Если это не первая молитва...
                    label_names[i-1].config(fg='Gold') # Меняем цвет предыдущей метки на золотой
                    label_times[i-1].config(fg='Aqua') # Меняем цвет предыдущей метки на голубой
                break # Прерываем цикл
            else: # Если текущее время больше времени молитвы...
                label_names[i].config(fg='Olive') # Меняем цвет текущей метки на оливковый
                label_times[i].config(fg='Teal') # Меняем цвет текущей метки на бирюзовый

        if next_prayer == 'next_day_first_prayer': # Если наступил новый день...
            label_names[-1].config(fg='Gold') # Меняем цвет последней метки на золотой
            label_times[-1].config(fg='Aqua') # Меняем цвет последней метки на голубой
            
        if next_prayer == 'next_day_first_prayer': # Если наступил новый день...
            os.execl(sys.executable, sys.executable, *sys.argv) # Перезапускаем программу

        window.after(60000, update_next_prayer_time) # Обновляем время до следующей молитвы каждую минуту

    update_next_prayer_time(timings) # Вызываем функцию обновления времени до следующей молитвы

    window.mainloop() # Запускаем главный цикл окна

def run(): # Функция для запуска программы
    timings, hijri_date = get_prayer_times()  # Получаем времена молитв и хиджрийскую дату
    if timings is not None and hijri_date is not None: # Если получены времена молитв и хиджрийская дата...
        create_window(timings, hijri_date) # Создаем окно с полученными данными

if __name__ == "__main__": # Если скрипт запущен как основной...
    play_audio_file('audio/BismillahFatihSefaragic.mp3', use_gui=False) # Воспроизводим аудиофайл
    time.sleep(5)  # Ждем 5 секунд
    run() # Запускаем программу

