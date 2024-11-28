#!/bin/bash

################ Как использовать ##################
# Запуск скрипта:                                  #
# ```bash                                          #
# ./adhan-install.sh                               #
# ```                                              #
# Скрипт выполнит - установку шрифтов, пакетов,    #
# настройку окружения, локалей, часового пояса,    #
# виртуального окружения, автозапуска и иконок.    #
####################################################

# Путь к исходной директории с шрифтами
SOURCE_DIR=~/GitHub/Adhan/fonts/
TARGET_DIR=~/fonts/

# Путь к файлу adhan.sh.desktop
DESKTOP_FILE=~/GitHub/Adhan/adhan.sh.desktop

# Путь к иконкам
ICON_DIR=~/GitHub/Adhan/icon/

# Массив с названиями файлов шрифтов
FILES=(
    "arialmt.ttf"
    "Comfortaa-Bold.ttf"
    "DSEG7Classic-Bold.ttf"
    "MartianMono-Bold.ttf"
    "Oswald-Bold.ttf"
)

# Проверка и создание директории
if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
fi
    echo "Проверка и создание директории $TARGET_DIR ЗАВЕРШЕНО"

# Копирование файлов шрифтов
echo "Копирование файлов шрифтов..."
for FILE in "${FILES[@]}"; do
    cp "$SOURCE_DIR$FILE" "$TARGET_DIR"
    echo "Копирование ${FILES[@]} ЗАВЕРШЕНО"
done

# Обновляем кеш шрифтов
echo "Обновление кеша шрифтов..."
fc-cache -f -v
echo "Обновление кеша шрифтов ЗАВЕРШЕНО"

# Обновление системы перед установкой пакетов
echo "Обновление базы данных пакетов и системы..."
sudo pacman -Syu --noconfirm
echo "Обновление системы завершено"

# Установка необходимых пакетов
echo "Установка необходимых пакетов..."
sudo pacman -S --noconfirm mpv python python-pip tk
echo "Установка необходимых пакетов ЗАВЕРШЕНО"

# Добавление переменных окружения
echo "Добавление переменных окружения..."
export PATH="/usr/local/opt/tcl-tk/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/tcl-tk/lib"
export CPPFLAGS="-I/usr/local/opt/tcl-tk/include"
echo "Добавление переменных окружения ЗАВЕРШЕНО"

# Настройка локали
echo "Настройка локали..."
sudo sed -i '/az_AZ UTF-8/s/^#//' /etc/locale.gen
sudo sed -i '/en_US.UTF-8 UTF-8/s/^#//' /etc/locale.gen
sudo sed -i '/ru_RU.UTF-8 UTF-8/s/^#//' /etc/locale.gen
sudo locale-gen
echo "Настройка локали ЗАВЕРШЕНО"

# Установка часового пояса
echo "Установка часового пояса..."
sudo ln -sf /usr/share/zoneinfo/Asia/Baku /etc/localtime
echo "Установка часового пояса ЗАВЕРШЕНО"

# Создание виртуального окружения
echo "Создание виртуального окружения Python..."
python3 -m venv venv
echo "Создание виртуального окружения Python ЗАВЕРШЕНО"

# Активация виртуального окружения и установка библиотек
echo "Активация виртуального окружения и установка библиотек..."
source venv/bin/activate
pip install requests prettytable rich
echo "Активация виртуального окружения и установка библиотек ЗАВЕРШЕНО"

# Копирование файла adhan.sh.desktop в нужные папки для 
# автозапуска и создании иконки приложения в меню программ
echo "Копирование adhan.sh.desktop в /usr/share/applications и ~/.config/autostart..."

sudo cp "$DESKTOP_FILE" /usr/share/applications/

if [ ! -d ~/.config/autostart ]; then
    mkdir -p ~/.config/autostart
fi

cp "$DESKTOP_FILE" ~/.config/autostart/
echo "Копирование adhan.sh.desktop в /usr/share/applications и ~/.config/autostart ЗАВЕРШЕНО"

# Копирование иконок в системные папки
echo "Копирование иконок adhan.svg в системные папки..."
sudo cp "$ICON_DIR/adhan.svg" /usr/share/icons/
sudo cp "$ICON_DIR/adhan.svg" /usr/share/icons/hicolor/scalable/apps/
sudo cp "$ICON_DIR/adhan.svg" /usr/share/icons/hicolor/symbolic/apps/
echo "Копирование иконок adhan.svg в системные папки  ЗАВЕРШЕНО"

# Копирование PNG иконок разных размеров с переименованием
declare -A ICON_SIZES=(
    [48]="adhan48x48.png"
    [64]="adhan64x64.png"
    [96]="adhan96x96.png"
    [128]="adhan128x128.png"
    [192]="adhan192x192.png"
    [256]="adhan256x256.png"
    [512]="adhan512x512.png"
)

for SIZE in "${!ICON_SIZES[@]}"; do
    ICON_FILE="${ICON_SIZES[$SIZE]}"
    TARGET_DIR="/usr/share/icons/hicolor/${SIZE}x${SIZE}/apps"
    
    # Проверка и создание директории
    if [ ! -d "$TARGET_DIR" ]; then
        sudo mkdir -p "$TARGET_DIR"
    fi
    
    # Копирование и переименование файла
    sudo cp "$ICON_DIR/$ICON_FILE" "$TARGET_DIR/adhan.png"
    echo "Иконка $ICON_FILE скопирована в $TARGET_DIR как adhan.png"
done

echo "Установка завершена! Чтобы запустить программу Adhan введите в терминале: '~/GitHub/Adhan/adhan.sh' или воспользуйтесь кнопкой программы в меню запуска программ."

