# for install and use Adhan

 1. Copy 5 fonts to `~/.fonts` folder

 > 5 Fonts for Adhan:
 >
 > arialmt.ttf  
 > Comfortaa-Bold.ttf  
 > DSEG7Classic-Bold.ttf  
 > MartianMono-Bold.ttf  
 > Oswald-Bold.ttf
 >

and update `fontconfig`

```bash
fc-cache -f -v
```

 2. Install: Mpv Player (not Flathub), Python, Pip and Tkinter Lib:  

```bash
yay -S mpv python python-pip tk
```

 3. Install Locale:  
 
  in file `/etc/locale.gen` 

```bash
sudo nano /etc/locale.gen
```

  delet `#` for:  

 > az_AZ UTF-8
 > en_US.UTF-8 UTF-8
 > ru_RU.UTF-8 UTF-8
 
  after edit file `locale.gen` run (for generate locales):

```bash
sudo locale-gen
```

 4. Install Time Zone 

```bash
sudo ln -sf /usr/share/zoneinfo/Asia/Baku /etc/localtime
```

 5. Change location on project directory  

```bash
cd ~/GitHub/Adhan
```

 6. Install Python Env  

```bash
python3 -m venv ptnEnvAdhan
```

 7. Activation Python Env-shel  

```bash
source ptnEnvAdhan/bin/activate
```

 8. Install Libruaries  

```bash
pip install requests prettytable rich
```

 9. Run Script  

```bash
python gui_prayer_times.py
```
