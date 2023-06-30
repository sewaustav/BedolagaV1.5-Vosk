import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor, QPen, QBrush, QPainterPath
from PySide6.QtCore import Qt, Slot, QTimer
from func import main

class RoundedRectLabel(QLabel):
    def __init__(self, text, radius, is_even):
        super().__init__(text)
        self.radius = radius
        self.is_even = is_even

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Задаем цвет и стиль пера для контура
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)

        # Задаем цвет заливки в зависимости от четности строки
        if self.is_even:
            brush = QBrush(QColor("#F4CA16"))
        else:
            brush = QBrush(QColor("#318CE7"))
        painter.setBrush(brush)

        # Получаем ширину и высоту текста
        text_width = self.fontMetrics().width(self.text())
        text_height = self.fontMetrics().height()

        # Рассчитываем координаты и размеры прямоугольника
        rect_x = (self.width() - text_width) / 2 - self.radius
        rect_y = (self.height() - text_height) / 2
        rect_width = text_width + self.radius * 2
        rect_height = text_height

        # Создаем путь с закругленными углами
        path = QPainterPath()
        path.addRoundedRect(rect_x, rect_y, rect_width, rect_height, self.radius, self.radius)

        # Рисуем закругленный прямоугольник
        painter.drawPath(path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Пример интерфейса PySide")

        # Создаем виджеты QLabel для заголовка и текста
        title_label = QLabel("БЕДОЛАГА", self)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))

        self.main_content_layout = QVBoxLayout()
        self.main_content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_content_layout.setSpacing(10)

        self.main_content_scroll_area = QScrollArea()
        self.main_content_scroll_area.setWidgetResizable(True)
        self.main_content_widget = QWidget()
        self.main_content_widget.setLayout(self.main_content_layout)
        self.main_content_scroll_area.setWidget(self.main_content_widget)

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
        main_layout.addWidget(self.main_content_scroll_area)
        main_layout.addLayout(buttons_layout)

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
        gpt_request = False
        gpt_code = False
        google_request = False
        dialog = False
        is_active_command = False
        weather = False
        main(gpt_request, gpt_code, google_request, dialog, is_active_command, weather)

    @Slot()
    def update_array(self):
        from func import output_data
        # Обновляем содержимое массива
        for i in range(len(self.array), len(output_data)):
            self.array.append(output_data[i])

        # Обновляем текст на экране
        self.update_main_content_label()

    def update_main_content_label(self):
        # Очищаем содержимое виджета с сообщениями
        while self.main_content_layout.count():
            item = self.main_content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Добавляем новые сообщения в виджет с сообщениями
        for i, message in enumerate(self.array):
            is_even = i % 2 == 0
            label = RoundedRectLabel(message, 10, is_even)
            label.setFont(QFont("Arial", 16))
            label.setFixedHeight(label.fontMetrics().height() + 10)  # Высота = высота текста + отступы
            self.main_content_layout.addWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
