# Импортируем модуль requests для отправки HTTP-запросов
import requests
# Импортируем модуль json для работы с данными в формате JSON
import json
from prettytable import PrettyTable
from rich import print

# Определяем функцию run
def run():
    # Задаем URL для запроса к API Aladhan
    url = "http://api.aladhan.com/v1/timingsByCity?city=Baku&country=Azerbaijan&method=13"
    # Отправляем GET-запрос к указанному URL
    response = requests.get(url)
    # Проверяем статус ответа
    if response.status_code == 200:
        # Если статус ответа 200 (успешно), то преобразуем текст ответа в JSON
        data = json.loads(response.text)
        # Извлекаем времена молитвы из данных ответа
        fajr = data["data"]["timings"]["Fajr"]
        sunrise = data["data"]["timings"]["Sunrise"]
        dhuhr = data["data"]["timings"]["Dhuhr"]
        asr = data["data"]["timings"]["Asr"]
        maghrib = data["data"]["timings"]["Maghrib"]
        isha = data["data"]["timings"]["Isha"]
        midnight = data["data"]["timings"]["Midnight"]

        # Создаем объект PrettyTable
        table = PrettyTable()
        # Устанавливаем названия столбцов
        table.field_names = ["Namaz", "Vaxtı"]
        # Добавляем строки с данными
        table.add_row(["İmsak", fajr])
        table.add_row(["Şəfəq", sunrise])
        table.add_row(["Günorta", dhuhr])
        table.add_row(["İkindi", asr])
        table.add_row(["Axşam", maghrib])
        table.add_row(["Gecə", isha])
        table.add_row(["Gecəyarı", midnight])

        # Выводим таблицу с увеличенным шрифтом
        print(f"[size=26]{table}[/size]")

    else:
        # Если статус ответа не 200, то выводим сообщение об ошибке
        print(f"Error: {response.status_code}")

# Если этот скрипт запущен как основной, то вызываем функцию run
if __name__ == "__main__":
    run()

