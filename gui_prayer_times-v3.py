import requests
import json
import tkinter as tk
from tkinter import font as tkfont
import datetime
import locale

def get_prayer_times():
    print("Получение времени молитвы...")  # Добавлено для отладки
    url = "http://api.aladhan.com/v1/timingsByCity?city=Baku&country=Azerbaijan&method=13"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        timings = data["data"]["timings"]
        selected_timings = {key: timings[key] for key in ["Midnight", "Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]}
        hijri_date = data["data"]["date"]["hijri"]
        formatted_hijri_date = f"{hijri_date['day']} {hijri_date['month']['en']} {hijri_date['year']}"
        print("Время молитвы получено.")  # Добавлено для отладки
        return selected_timings, formatted_hijri_date
    else:
        print("Не удалось получить время молитвы.")  # Добавлено для отладки
        return None, None

def get_next_prayer_time(timings):
    print("Получение времени следующей молитвы...")  # Добавлено для отладки
    now = datetime.datetime.now().time()
    for prayer, time in timings.items():
        prayer_time = datetime.datetime.strptime(time, "%H:%M").time()
        if now < prayer_time:
            print(f"Время следующей молитвы: {prayer_time}")  # Добавлено для отладки
            return prayer_time
    print("Все молитвы на сегодня уже прошли.")  # Добавлено для отладки
    return None

def create_window(timings, hijri_date):
    window = tk.Tk()
    window.title("Namaz Vaxtları")
    window.configure(bg='#222222')
    
    bold_font = tkfont.Font(family="DSEG14Modern", size=30, weight="bold")
    regular_font = tkfont.Font(family="DSEG14Modern", size=30)
    clock_font = tkfont.Font(family="DSEG14Modern", size=100, weight="bold")
    date_font = tkfont.Font(family="DSEG14Modern", size=20)
    line_font = tkfont.Font(family="DSEG14Modern", size=10, weight="bold")

    az_names = {
        "Midnight": "  Təhəccüd -----------",
        "Fajr": "  İmsak ----------------",
        "Sunrise": "  Günəş ---------------",
        "Dhuhr": "  Günorta -------------",
        "Asr": "  İkindi ----------------",
        "Maghrib": "  Axşam --------------",
        "Isha": "  Gecə ----------------"
    }

    now = datetime.datetime.now().time()

    gregorian_date_label = tk.Label(window, font=date_font, bg='#222222', fg='Olive')
    gregorian_date_label.grid(row=2, column=0, columnspan=2)

    hijri_date_label = tk.Label(window, font=date_font, bg='#222222', fg='Olive')
    hijri_date_label.grid(row=3, column=0, columnspan=2)

    def update_date():
        hijri_date_label.config(text=f"{hijri_date}")
        locale.setlocale(locale.LC_TIME, "ru_RU.utf8")
        current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
        gregorian_date_label.config(text=f"{current_date} {'года'}")

    update_date()

    clock_label = tk.Label(window, font=clock_font, bg='#222222', fg='lime', pady=20)
    clock_label.grid(row=0, column=0, columnspan=2)

    def update_clock():
        current_time = datetime.datetime.now().strftime("%H:%M")
        clock_label.config(text=current_time)
        window.after(1000, update_clock)

    update_clock()

    label_xett1 = tk.Label(window, text=f"――――――――――――――――――――――――――――――――――――――――――", font=line_font, bg='#222222', fg='Olive')
    label_xett1.grid(row=4, columnspan=2)
    label_qaliq = tk.Label(window, text=f"Növbəti namaza qalan vaxt - ", font=date_font, bg='#222222', fg='Gold', anchor='e')
    label_qaliq_time = tk.Label(window, text="", font=bold_font, bg='#222222', fg='Red', anchor='w')  # Изменили здесь
    label_qaliq.grid(row=5, column=0, sticky='e', pady=(0,0))
    label_qaliq_time.grid(row=5, column=1, sticky='w', pady=(0,0))
    label_xett2 = tk.Label(window, text=f"――――――――――――――――――――――――――――――――――――――――――", font=line_font, bg='#222222', fg='Olive')
    label_xett2.grid(row=6, columnspan=2)

    for i, (name, time) in enumerate(timings.items()):
        prayer_time = datetime.datetime.strptime(time, "%H:%M").time()

        label_name = tk.Label(window, text=f"{az_names[name]} -", font=regular_font, bg='#222222', fg='Olive', anchor='e')
        label_time = tk.Label(window, text=f"{time}", font=bold_font, bg='#222222', fg='Teal', anchor='w')
        label_name.grid(row=i+7, column=0, sticky='e', pady=(0,10))
        label_time.grid(row=i+7, column=1, sticky='w', pady=(0,10))

    def update_next_prayer_time():
        print("Обновление времени до следующей молитвы...")  # Добавлено для отладки
        next_prayer_time = get_next_prayer_time(timings)
        if next_prayer_time is not None:
            now = datetime.datetime.now().time()
            time_difference = datetime.datetime.combine(datetime.date.today(), next_prayer_time) - datetime.datetime.combine(datetime.date.today(), now)
            minutes, seconds = divmod(time_difference.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            label_qaliq_time.config(text=f"{hours:02d}:{minutes:02d}")  # Изменили здесь
            print(f"Оставшееся время до следующей молитвы: {hours:02d}:{minutes:02d}")  # Добавлено для отладки
        window.after(60000, update_next_prayer_time)  # обновляем каждую минуту

    update_next_prayer_time()  # Вызываем сразу после создания метки

    window.mainloop()

def run():
    timings, hijri_date = get_prayer_times()
    if timings is not None and hijri_date is not None:
        create_window(timings, hijri_date)

if __name__ == "__main__":
    run()

