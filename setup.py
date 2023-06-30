import sys
from cx_Freeze import setup, Executable

# Путь к вашему скрипту Python
script = 'bedolaga.py'

# Создание объекта Executable
executables = [Executable(script)]

# Настройки компиляции
build_options = {
    'packages': ['os', 'subprocess', 'webbrowser', 'vosk', 'sys', 'sounddevice', 'queue', 'cv2', 'numpy', 'pyautogui', 'time', 'pyowm', 'pyttsx3', 'openai', 'string'],
    'excludes': [],
    'include_files': [
        'config.py',
        'web/main.html',
        'web/style/style.css',
        'web/jquery-3.6.0.min.js',
        'web/img/setting.png',
        'web/img/info.png',
        'web/img/микро-removebg-preview.png'

    ],
}

# Настройки сборки
build_exe_options = {
    'build_exe': 'dist',  # Папка, куда будет помещен .exe файл
}

# Создание экземпляра setup
setup(
    name='MyApp',
    version='1.0',
    description='My Application',
    options={'build_exe': build_exe_options},
    executables=executables
)
