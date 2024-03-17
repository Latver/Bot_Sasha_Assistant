import os
import subprocess

# URL приватного репозитория с токеном доступа
repo_url = 'https://Latver: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@github.com/Latver/Bot_v2.git'

# Директория для скачивания файлов репозитория
download_directory = os.path.dirname(os.path.abspath(__file__))

# Переход в директорию для скачивания файлов
os.chdir(download_directory)

# Команда Git clone с использованием URL-адреса репозитория
command = ['git', 'clone', repo_url]
clone = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = clone.communicate()

# Проверка успешности выполнения команды Git clone
if error:
    print(f'Ошибка при клонировании репозитория: {error.decode()}')
else:
    print('Репозиторий успешно склонирован.')
