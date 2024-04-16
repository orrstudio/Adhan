# Импорт модуля requests для выполнения HTTP-запросов
import requests
# Импорт модуля json для работы с данными в формате JSON
import json
# Импорт модуля tkinter для создания графического пользовательского интерфейса
import tkinter as tk
# Импорт модуля font из tkinter для работы со шрифтами
from tkinter import font as tkfont
# Импорт модуля datetime для работы с датами и временем
import datetime
# Импорт модуля locale для работы с локализацией
import locale

# Функция для получения времени молитвы
def get_prayer_times():
    # URL API для получения времени молитвы
    url = "http://api.aladhan.com/v1/timingsByCity?city=Baku&country=Azerbaijan&method=13"
    # Выполнение GET-запроса к API
    response = requests.get(url)
    # Проверка статуса ответа
    if response.status_code == 200:
        # Преобразование ответа из формата JSON в словарь Python
        data = json.loads(response.text)
        # Извлечение времени молитвы из данных
        timings = data["data"]["timings"]
        # Выбор нужных времен молитвы
        selected_timings = {key: timings[key] for key in ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha", "Midnight"]}
        # Извлечение даты по хиджре из данных
        hijri_date = data["data"]["date"]["hijri"]
        # Форматирование даты по хиджре
        formatted_hijri_date = f"{hijri_date['day']} {hijri_date['month']['en']} {hijri_date['year']}"
        # Возврат выбранных времен молитвы и отформатированной даты по хиджре
        return selected_timings, formatted_hijri_date
    else:
        # Возврат None, если статус ответа не равен 200
        return None, None

# Функция для создания окна
def create_window(timings, hijri_date):
    # Создание нового окна
    window = tk.Tk()
    # Установка заголовка окна
    window.title("Namaz Vaxtları")
    # Установка цвета фона окна
    window.configure(bg='#222222')
    # Создание шрифтов для использования в метках
    bold_font = tkfont.Font(family="DSEG7Classic", size=40, weight="bold")
    regular_font = tkfont.Font(family="FreeSans", size=30)
    clock_font = tkfont.Font(family="DSEG7Classic", size=120, weight="bold")
    date_font = tkfont.Font(family="FreeSans", size=20)

    # Словарь для перевода названий молитв на азербайджанский язык
    az_names = {
        "Fajr": "İmsak",
        "Sunrise": "Günəş",
        "Dhuhr": "Günorta",
        "Asr": "İkindi",
        "Maghrib": "Axşam",
        "Isha": "Gecə",
        "Midnight": "Təhəccüd"
    }

    # Получение текущего времени
    now = datetime.datetime.now().time()

    # Добавление метки с текущей датой в верхнюю часть окна
    hijri_date_label = tk.Label(window, font=date_font, bg='#222222', fg='gold')
    hijri_date_label.grid(row=0, column=0, columnspan=2)

    gregorian_date_label = tk.Label(window, font=date_font, bg='#222222', fg='gold')
    gregorian_date_label.grid(row=1, column=0, columnspan=2)

    # Функция для обновления даты
    def update_date():
        # Установка текста метки с датой по хиджре
        hijri_date_label.config(text=f"{hijri_date}")
        # Установка локали на русский язык
        locale.setlocale(locale.LC_TIME, "ru_RU.utf8")
        # Получение текущей даты
        current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
        # Установка текста метки с григорианской датой
        gregorian_date_label.config(text=f"{current_date} {'года'}")

    # Вызов функции обновления даты
    update_date()

    # Добавление метки с текущим временем под датами
    clock_label = tk.Label(window, font=clock_font, bg='#222222', fg='lime', pady=20)
    clock_label.grid(row=2, column=0, columnspan=2)

    # Функция для обновления времени
    def update_clock():
        # Получение текущего времени
        current_time = datetime.datetime.now().strftime("%H:%M")
        # Установка текста метки с временем
        clock_label.config(text=current_time)
        # Установка таймера для обновления времени каждую секунду
        window.after(1000, update_clock)

    # Вызов функции обновления времени
    update_clock()

    # Создание меток для каждого времени молитвы
    for i, (name, time) in enumerate(timings.items()):
        # Преобразование времени молитвы из строки в объект datetime.time
        prayer_time = datetime.datetime.strptime(time, "%H:%M").time()

        # Установка цветов меток в зависимости от текущего времени и времени молитвы
        if now < prayer_time:
            colorNum = 'Teal'
            colorTxt = 'Olive'
        else:
            colorNum = 'Aqua'
            colorTxt = 'Yellow'

        # Создание меток с названием молитвы и временем
        label_name = tk.Label(window, text=f"{az_names[name]} -", font=regular_font, bg='#222222', fg=colorTxt, anchor='e')
        label_time = tk.Label(window, text=f"{time}", font=bold_font, bg='#222222', fg=colorNum, anchor='w')
        # Размещение меток в окне
        label_name.grid(row=i+3, column=0, sticky='e', pady=(0,10))
        label_time.grid(row=i+3, column=1, sticky='w', pady=(0,10))

    # Запуск главного цикла обработки событий tkinter
    window.mainloop()

# Функция для запуска приложения
def run():
    # Получение времени молитвы
    timings, hijri_date = get_prayer_times()
    # Проверка, что время молитвы получено успешно
    if timings is not None and hijri_date is not None:
        # Создание окна с временем молитвы
        create_window(timings, hijri_date)

# Запуск приложения, если этот файл является главным
if __name__ == "__main__":
    run()

