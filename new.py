import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt, Slot
from func import main, output_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Пример интерфейса PySide")

        # Создаем виджеты QLabel для заголовка и текста
        title_label = QLabel("БЕДОЛАГА", self)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))

        main_content_label = QLabel("", self)
        main_content_label.setWordWrap(True)
        main_content_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_content_label.setStyleSheet("background-color: #EBECF0;")
        main_content_label.setFixedHeight(300)

        # Создаем виджеты QPushButton для кнопок

        # Создаем виджеты QLabel для иконок
        settings_icon_label = QLabel(self)
        settings_icon_label.setPixmap(QPixmap("img/setting.png").scaled(55, 55))
        settings_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_icon_label.setStyleSheet("background-color: #EBECF0;")

        microphone_icon_label = QLabel(self)
        microphone_icon_label.setPixmap(QPixmap("img/микро-removebg-preview.png").scaled(65, 65))
        microphone_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        microphone_icon_label.setStyleSheet("background-color: #5E17EB; border-radius: 100%; padding: 10px;")

        info_icon_label = QLabel(self)
        info_icon_label.setPixmap(QPixmap("img/info.png").scaled(55, 55))
        info_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_icon_label.setStyleSheet("background-color: #EBECF0;")

        # Создаем компоновщики QVBoxLayout и QHBoxLayout для компоновки виджетов
        main_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        info_layout = QHBoxLayout()

        # Добавляем виджеты в компоновщики
        buttons_layout.addWidget(settings_icon_label)
        buttons_layout.addWidget(microphone_icon_label)
        buttons_layout.addWidget(info_icon_label)

        info_layout.addStretch()
        info_layout.addWidget(title_label)
        info_layout.addStretch()

        main_layout.addLayout(info_layout)
        main_layout.addWidget(main_content_label)
        main_layout.addLayout(buttons_layout)

        # Создаем виджет QWidget и устанавливаем наш компоновщик в качестве его компоновки
        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

        # Подключаем слот к сигналу нажатия кнопки "микрофон"
        microphone_icon_label.mousePressEvent = self.on_microphone_clicked

        self.resize(800, 600)

    @Slot()
    def on_microphone_clicked(self, event):
        # Вызываем функцию main из func.py при нажатии на иконку "микрофон"
        gpt_request = False;
        gpt_code = False
        google_request = False
        dialog = False
        is_active_command = False
        weather = False
        main(gpt_request, gpt_code, google_request, dialog, is_active_command, weather)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())






import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt, Slot, QTimer
from func import main

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Пример интерфейса PySide")

        # Создаем виджеты QLabel для заголовка и текста
        title_label = QLabel("БЕДОЛАГА", self)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))

        self.main_content_label = QLabel("", self)
        self.main_content_label.setWordWrap(True)
        self.main_content_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_content_label.setStyleSheet("background-color: #EBECF0;")
        self.main_content_label.setFixedHeight(300)

        # Создаем виджеты QPushButton для кнопок
        update_button = QPushButton("Update", self)
        update_button.setStyleSheet("background-color: #EBECF0;")

        # Создаем виджеты QLabel для иконок
        settings_icon_label = QLabel(self)
        settings_icon_label.setPixmap(QPixmap("img/setting.png").scaled(55, 55))
        settings_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_icon_label.setStyleSheet("background-color: #EBECF0;")

        microphone_icon_label = QLabel(self)
        microphone_icon_label.setPixmap(QPixmap("img/микро-removebg-preview.png").scaled(65, 65))
        microphone_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        microphone_icon_label.setStyleSheet("background-color: #5E17EB; border-radius: 100%; padding: 10px;")

        info_icon_label = QLabel(self)
        info_icon_label.setPixmap(QPixmap("img/info.png").scaled(55, 55))
        info_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_icon_label.setStyleSheet("background-color: #EBECF0;")

        # Создаем компоновщики QVBoxLayout и QHBoxLayout для компоновки виджетов
        main_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        info_layout = QHBoxLayout()

        # Добавляем виджеты в компоновщики
        buttons_layout.addWidget(settings_icon_label)
        buttons_layout.addWidget(microphone_icon_label)
        buttons_layout.addWidget(info_icon_label)

        info_layout.addStretch()
        info_layout.addWidget(title_label)
        info_layout.addStretch()

        main_layout.addLayout(info_layout)
        main_layout.addWidget(self.main_content_label)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(update_button)

        # Создаем виджет QWidget и устанавливаем наш компоновщик в качестве его компоновки
        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

        # Подключаем слот к сигналу нажатия кнопки "микрофон"
        microphone_icon_label.mousePressEvent = self.on_microphone_clicked

        # Задаем размеры окна
        self.resize(800, 600)  # Здесь можно установить желаемые ширину и высоту

        # Создаем таймер для обновления содержимого массива
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_array)
        self.timer.start(1000)  # Обновление каждую секунду

        # Инициализируем массив
        self.array = []

    @Slot()
    def on_microphone_clicked(self, event):
        gpt_request = False;
        gpt_code = False
        google_request = False
        dialog = False
        is_active_command = False
        weather = False
        main(gpt_request, gpt_code, google_request, dialog, is_active_command, weather)

    @Slot()
    def update_array(self):
        # Обновляем содержимое массива
        self.array.append("Новая запись")

        # Обновляем текст на экране
        self.update_main_content_label()

    def update_main_content_label(self):
        # Обновляем текст в QLabel с содержимым массива
        text = "<br>".join(self.array)
        self.main_content_label.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

