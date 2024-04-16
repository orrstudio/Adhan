import requests
import json
import tkinter as tk
from tkinter import font as tkfont
import datetime
import locale

def get_prayer_times():
    url = "http://api.aladhan.com/v1/timingsByCity?city=Baku&country=Azerbaijan&method=13"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        timings = data["data"]["timings"]
        selected_timings = {key: timings[key] for key in ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha", "Midnight"]}
        hijri_date = data["data"]["date"]["hijri"]
        formatted_hijri_date = f"{hijri_date['day']} {hijri_date['month']['en']} {hijri_date['year']}"
        return selected_timings, formatted_hijri_date
    else:
        return None, None

def create_window(timings, hijri_date):
    window = tk.Tk()
    window.title("Namaz Vaxtları")
    window.configure(bg='#222222')
    bold_font = tkfont.Font(family="DSEG7Classic", size=30, weight="bold")
    regular_font = tkfont.Font(family="FreeSans", size=30)
    clock_font = tkfont.Font(family="DSEG7Classic", size=100, weight="bold")
    date_font = tkfont.Font(family="FreeSans", size=20)

    az_names = {
        "Fajr": "İmsak",
        "Sunrise": "Günəş",
        "Dhuhr": "Günorta",
        "Asr": "İkindi",
        "Maghrib": "Axşam",
        "Isha": "Gecə",
        "Midnight": "Təhəccüd"
    }

    now = datetime.datetime.now().time()

    hijri_date_label = tk.Label(window, font=date_font, bg='#222222', fg='gold')
    hijri_date_label.grid(row=0, column=0, columnspan=2)

    gregorian_date_label = tk.Label(window, font=date_font, bg='#222222', fg='gold')
    gregorian_date_label.grid(row=1, column=0, columnspan=2)

    def update_date():
        hijri_date_label.config(text=f"{hijri_date}")
        locale.setlocale(locale.LC_TIME, "ru_RU.utf8")
        current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
        gregorian_date_label.config(text=f"{current_date} {'года'}")

    update_date()

    clock_label = tk.Label(window, font=clock_font, bg='#222222', fg='lime', pady=20)
    clock_label.grid(row=2, column=0, columnspan=2)

    def update_clock():
        current_time = datetime.datetime.now().strftime("%H:%M")
        clock_label.config(text=current_time)
        window.after(1000, update_clock)

    update_clock()

    for i, (name, time) in enumerate(timings.items()):
        prayer_time = datetime.datetime.strptime(time, "%H:%M").time()

        label_name = tk.Label(window, text=f"{az_names[name]} -", font=regular_font, bg='#222222', fg='Olive', anchor='e')
        label_time = tk.Label(window, text=f"{time}", font=bold_font, bg='#222222', fg='Teal', anchor='w')
        label_name.grid(row=i+3, column=0, sticky='e', pady=(0,10))
        label_time.grid(row=i+3, column=1, sticky='w', pady=(0,10))

    window.mainloop()

def run():
    timings, hijri_date = get_prayer_times()
    if timings is not None and hijri_date is not None:
        create_window(timings, hijri_date)

if __name__ == "__main__":
    run()

