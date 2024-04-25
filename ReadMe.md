# Adhan

> If you want, you can change location and other settings and rebuild

## For Develop

- INSTALL PYTHON (`yay -S python`)
- INSTALL PIP (`yay -S python-pip`)
- INSTALL TKINTER LIB (`yay -S tk`)
- INSTALL LOCALE (in file `sudo nano /etc/locale.gen` delet `#` for `az_AZ UTF-8` and `en_US.UTF-8 UTF-8` and `ru_RU.UTF-8 UTF-8`)
- GENERATE LOCALE (after edit file run `sudo locale-gen`)
- EDIT TIME ZONE (`sudo ln -sf /usr/share/zoneinfo/Asia/Baku /etc/localtime`)
- CHANGE LOCATION ON PROJECT DIRECTORY (`cd ~/GITHUB/Adhan`)
- INSTALL PYTHON ENV (`python3 -m venv ptnEnvAdhan`)
- ACTIVATION PYTHON ENV-SHEL (`source ptnEnvAdhan/bin/activate`)
- INSTALL LIBRUARY (`pip install requests prettytable rich`)
- EDIT FOR CHANGE SCRIPT (`python gui_prayer_times-v6.py`)

## For Build

- INSTALL PYTHON (`yay -S python`)
- INSTALL PIP (`yay -S python-pip`)
- INSTALL PYINSTALL (`pip install pyinstaller`)
- INSTALL LOCALE (in file `sudo nano /etc/locale.gen` delet `#` for `az_AZ UTF-8` and `en_US.UTF-8 UTF-8` and `ru_RU.UTF-8 UTF-8`)
- GENERATE LOCALE (after edit file run `sudo locale-gen`)
- EDIT TIME ZONE (`sudo ln -sf /usr/share/zoneinfo/Asia/Baku /etc/localtime`)
- CHANGE LOCATION ON PROJECT DIRECTORY (`cd ~/GITHUB/Adhan`)
- INSTALL PYTHON ENV (`python3 -m venv ptnEnvAdhan`)
- ACTIVATION PYTHON ENV-SHEL (`source ptnEnvAdhan/bin/activate`)
- INSTALL LIBRUARY (`pip install requests prettytable rich`)
- RUN FOR BUILD (`pyinstaller --onefile gui_prayer_times-v6.py`)

## For RUN

- INSTALL FONTS (copy 5 fonts to `~/.local/share/fonts`)
- INSTALL MPV (`sudo pacman -S mpv`)
- INSTALL LOCALE (in file `sudo nano /etc/locale.gen` delet `#` for `az_AZ UTF-8` and `en_US.UTF-8 UTF-8` and `ru_RU.UTF-8 UTF-8`)
- GENERATE LOCALE (after edit file run `sudo locale-gen`)
- EDIT TIME ZONE (`sudo ln -sf /usr/share/zoneinfo/Asia/Baku /etc/localtime`)
- RUN `gui_prayer_times-v6` for use.
