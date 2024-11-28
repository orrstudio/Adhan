from datetime import datetime as dt
import requests
import json
import tkinter as tk
from tkinter import font as tkfont
import subprocess
import os
import time
import locale
import tkinter

def get_prayer_times():
    url = "http://api.aladhan.com/v1/timingsByCity?city=baku&country=AZ&method=13"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        timings = data["data"]["timings"]
        selected_timings = {key: timings[key] for key in ["Midnight", "Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]}
        hijri_date = data["data"]["date"]["hijri"]
        formatted_hijri_date = f"{hijri_date['day']} {hijri_date['month']['en']} {hijri_date['year']}"
        return selected_timings, formatted_hijri_date
    else:
        return None, None

def get_next_prayer_time(timings):
    now_time = dt.now().time()
    timings_next_day = timings.copy()
    first_prayer = list(timings.values())[0]
    timings_next_day['next_day_first_prayer'] = first_prayer
    for prayer, time in timings_next_day.items():
        prayer_time = dt.strptime(time, "%H:%M").time()
        now_time = dt.now().time()
        if now_time < prayer_time:
            return prayer, prayer_time
    next_day_first_prayer_time = dt.strptime(timings_next_day['next_day_first_prayer'], "%H:%M").time()
    return 'next_day_first_prayer', next_day_first_prayer_time

def play_audio_file(file_path, use_gui):
    FNULL = open(os.devnull, 'w')
    if use_gui:
        subprocess.Popen(['mpv', '--force-window', file_path], stdout=FNULL, stderr=subprocess.STDOUT, shell=False)
    else:
        subprocess.Popen(['mpv', file_path], stdout=FNULL, stderr=subprocess.STDOUT, shell=False)

def create_window(timings, hijri_date):
    window = tk.Tk()
    window.title("Namaz Vaxtları")
    window.configure(bg='#222222')
    
    # Установка размера и положения окна
    window.geometry(f'+0+0')
    
    bold_font = tkfont.Font(family="DSEG7Classic", size=30, weight="bold")
    regular_font = tkfont.Font(family="MartianMono", size=30)
    clock_font = tkfont.Font(family="DSEG7Classic", size=100, weight="bold")
    date_font = tkfont.Font(family="Comfortaa", size=20, weight="bold")
    line_font = tkfont.Font(family="Arial", size=10, weight="bold")

    az_names = {
        "Midnight": " Təhəccüd --",
            "Fajr": " İmsak -----",
         "Sunrise": " Günəş -----",
           "Dhuhr": " Günorta ---",
             "Asr": " İkindi ----",
         "Maghrib": " Axşam -----",
            "Isha": " Gecə ------"
    }

    now_time = dt.now().time()

    gregorian_date_label = tk.Label(window, font=date_font, bg='#222222', fg='Olive')
    gregorian_date_label.grid(row=2, column=0, columnspan=2)

    hijri_date_label = tk.Label(window, font=date_font, bg='#222222', fg='Olive')
    hijri_date_label.grid(row=3, column=0, columnspan=2)

    def update_date():
        hijri_date_label.config(text=f"{hijri_date}")
        locale.setlocale(locale.LC_TIME, "ru_RU.utf8")
        current_date = dt.now().strftime("%A, %d %B %Y")
        gregorian_date_label.config(text=f"{current_date} {'года'}")

    update_date()

    clock_label = tk.Label(window, font=clock_font, bg='#222222', fg='lime', pady=20)
    clock_label.grid(row=0, column=0, columnspan=2)

    def update_clock():
        current_time = dt.now().strftime("%H:%M")
        clock_label.config(text=current_time)
        window.after(1000, update_clock)

    update_clock()

    label_xett1 = tk.Label(window, text=f"――――――――――――――――――――――――――――――――――――――――", font=line_font, bg='#222222', fg='Olive')
    label_xett1.grid(row=4, columnspan=2)
    label_qaliq = tk.Label(window, text=f" Növbəti >>>", font=regular_font, bg='#222222', fg='Gold', anchor='w')
    label_qaliq_time = tk.Label(window, text="", font=bold_font, bg='#222222', fg='Red', anchor='w')
    label_qaliq.grid(row=5, column=0, sticky='w', pady=(0,0))
    label_qaliq_time.grid(row=5, column=1, sticky='w', pady=(0,0))
    label_xett2 = tk.Label(window, text=f"――――――――――――――――――――――――――――――――――――――――", font=line_font, bg='#222222', fg='Olive')
    label_xett2.grid(row=6, columnspan=2)

    label_names = []
    label_times = []
    for i, (name, time) in enumerate(timings.items()):
        label_name = tk.Label(window, text=f"{az_names[name]}", font=regular_font, bg='#222222', fg='Olive', anchor='e')
        label_time = tk.Label(window, text=f"{time}", font=bold_font, bg='#222222', fg='Teal', anchor='w')
        label_name.grid(row=i+7, column=0, sticky='w', pady=(0,4))
        label_time.grid(row=i+7, column=1, sticky='w', pady=(0,4))
        label_names.append(label_name)
        label_times.append(label_time)

    def update_next_prayer_time():
        next_prayer, next_prayer_time = get_next_prayer_time(timings)
        if next_prayer_time is not None:
            now_time = dt.now().time()
            time_difference = dt.combine(dt.today().date(), next_prayer_time) - dt.combine(dt.today().date(), now_time)
            minutes, seconds = divmod(time_difference.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            label_qaliq_time.config(text=f"{hours:02d}:{minutes:02d}")
            if (hours == 1 and minutes == 0) or (hours == 0 and minutes == 45) or (hours == 0 and minutes == 30):
                play_audio_file('audio/AllahuAkbar.mp3', use_gui=False)
            if hours == 0 and minutes == 0:
                # Проверяем, какая молитва следующая, и воспроизводим соответствующий аудиофайл
                if next_prayer in ['Midnight', 'Sunrise']:
                    play_audio_file('audio/BismillahFatihSefaragic.mp3', use_gui=False)
                else:
                    play_audio_file('audio/adhan/AdhanAhmedAlNufais.mp3', use_gui=True)

        for i, (name, time) in enumerate(timings.items()):
            prayer_time = dt.strptime(time, "%H:%M").time()
            now_time = dt.now().time()
            if now_time < prayer_time:
                if i > 0:
                    label_names[i-1].config(fg='Gold')
                    label_times[i-1].config(fg='Aqua')
                break
            else:
                label_names[i].config(fg='Olive')
                label_times[i].config(fg='Teal')
        if next_prayer == 'next_day_first_prayer':
            label_names[-1].config(fg='Gold')
            label_times[-1].config(fg='Aqua')
        window.after(60000, update_next_prayer_time)


    update_next_prayer_time()

    window.mainloop()

def run():
    timings, hijri_date = get_prayer_times()
    if timings is not None and hijri_date is not None:
        create_window(timings, hijri_date)
    
if __name__ == "__main__":
    # subprocess.run(["powermate", "-d"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # Запуск команды powermate -d
    play_audio_file('audio/BismillahFatihSefaragic.mp3', use_gui=False) # Запуск аудио "Бисмиллах"
    time.sleep(5)  # ждем 5 секунд перед завершением программы
    run()

