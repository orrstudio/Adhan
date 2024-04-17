import subprocess

def play_audio_file(file_path):
    # Запуск mpv для воспроизведения аудиофайла
    subprocess.call(['mpv', file_path])

if __name__ == "__main__":
    play_audio_file('audio/AdhanAhmedAlNufais.mp3')

