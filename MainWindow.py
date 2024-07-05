from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QHBoxLayout, QVBoxLayout, QMainWindow, QPushButton, \
    QComboBox, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QTimer
import cv2
import numpy as np


class MainWindow(QMainWindow):
    """
    Класс MainWindow представляет главное окно приложения для редактирования изображений.

    Атрибуты:
        image_label (QLabel): Виджет метки для отображения изображения.
        button1 (QPushButton): Кнопка для выбора изображения с компьютера.
        button2 (QPushButton): Кнопка для включения веб-камеры.
        capture_button (QPushButton): Кнопка для захвата изображения с веб-камеры.
        combobox (QComboBox): Комбобокс для выбора цветового канала.
        height_input (QLineEdit): Поле ввода для указания высоты изображения.
        width_input (QLineEdit): Поле ввода для указания ширины изображения.
        brightness_input (QLineEdit): Поле ввода для уменьшения яркости.
        center_x_input (QLineEdit): Поле ввода для указания X координаты центра круга.
        center_y_input (QLineEdit): Поле ввода для указания Y координаты центра круга.
        radius_input (QLineEdit): Поле ввода для указания радиуса круга.
        apply_button (QPushButton): Кнопка для применения изменений.
        reset_button (QPushButton): Кнопка для отмены изменений.
        cap (cv2.VideoCapture): Объект захвата видео для веб-камеры.
        timer (QTimer): Таймер для обновления видеопотока.
        current_image (numpy.ndarray): Текущее изображение.
        original_image (numpy.ndarray): Оригинальное изображение.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setFixedSize(1000, 600)
        self.image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()

        self.button1 = QPushButton("Выбрать изображение на компьютере")
        button_layout.addWidget(self.button1)
        self.button1.setFixedHeight(40)
        self.button1.clicked.connect(self.open_image)

        self.button2 = QPushButton("Включить веб-камеру")
        button_layout.addWidget(self.button2)
        self.button2.setFixedHeight(40)
        self.button2.clicked.connect(self.start_camera)

        self.capture_button = QPushButton("Сделать фото")
        button_layout.addWidget(self.capture_button)
        self.capture_button.setFixedHeight(40)
        self.capture_button.clicked.connect(self.capture_image)
        self.capture_button.setEnabled(False)

        main_layout.addLayout(button_layout)

        self.combobox = QComboBox()
        self.combobox.addItems(["Все каналы", "Красный канал", "Зеленый канал", "Синий канал"])
        self.combobox.currentIndexChanged.connect(self.update_image_channel)
        main_layout.addWidget(self.combobox)

        input_layout = QHBoxLayout()

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Высота изображения")
        input_layout.addWidget(self.height_input)

        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Ширина изображения")
        input_layout.addWidget(self.width_input)

        self.brightness_input = QLineEdit()
        self.brightness_input.setPlaceholderText("Понизить яркость")
        input_layout.addWidget(self.brightness_input)

        main_layout.addLayout(input_layout)

        circle_layout = QHBoxLayout()

        self.center_x_input = QLineEdit()
        self.center_x_input.setPlaceholderText("X координата центра круга")
        circle_layout.addWidget(self.center_x_input)

        self.center_y_input = QLineEdit()
        self.center_y_input.setPlaceholderText("Y координата центра круга")
        circle_layout.addWidget(self.center_y_input)

        self.radius_input = QLineEdit()
        self.radius_input.setPlaceholderText("Радиус круга")
        circle_layout.addWidget(self.radius_input)

        main_layout.addLayout(circle_layout)

        action_button_layout = QHBoxLayout()

        self.apply_button = QPushButton("Применить изменения")
        action_button_layout.addWidget(self.apply_button)
        self.apply_button.setFixedHeight(40)
        self.apply_button.clicked.connect(self.apply_changes)

        self.reset_button = QPushButton("Отменить изменения")
        action_button_layout.addWidget(self.reset_button)
        self.reset_button.setFixedHeight(40)
        self.reset_button.clicked.connect(self.reset_image)

        main_layout.addLayout(action_button_layout)

        central_widget.setLayout(main_layout)

        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_video_stream)

        self.current_image = None
        self.original_image = None

    def center(self):
        """
        Центрирует окно приложения на экране.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_image(self):
        """
        Открывает диалоговое окно для выбора изображения с компьютера и отображает выбранное изображение.
        """
        file_dialog = QFileDialog(self)
        filename, _ = file_dialog.getOpenFileName(self, "Выбрать изображение", "", "Изображения (*.png *.jpg)")
        if filename:
            self.current_image = cv2.imread(filename)
            self.original_image = self.current_image.copy()
            self.display_image(self.current_image)

    def start_camera(self):
        """
        Включает веб-камеру и начинает потоковое отображение видео.
        """
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)
        self.capture_button.setEnabled(True)

    def display_video_stream(self):
        """
        Отображает видеопоток с веб-камеры в реальном времени.
        """
        ret, frame = self.cap.read()
        if ret:
            self.current_image = frame
            self.display_image(frame)

    def capture_image(self):
        """
        Захватывает изображение с веб-камеры и отображает его.
        """
        ret, frame = self.cap.read()
        if ret:
            self.current_image = frame
            self.original_image = self.current_image.copy()
            self.display_image(frame)
            self.timer.stop()
            self.cap.release()
            self.capture_button.setEnabled(False)

    def display_image(self, image):
        """
        Отображает изображение в виджете метки с учетом выбранного цветового канала.

        Args:
            image (numpy.ndarray): Изображение для отображения.
        """
        if image is not None:
            channel = self.combobox.currentText()
            if channel == "Красный канал":
                image = self.extract_channel(image, 2)
            elif channel == "Зеленый канал":
                image = self.extract_channel(image, 1)
            elif channel == "Синий канал":
                image = self.extract_channel(image, 0)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def update_image_channel(self):
        """
        Обновляет отображение изображения при изменении выбранного цветового канала.
        """
        if self.current_image is not None:
            self.display_image(self.current_image)

    @staticmethod
    def extract_channel(image, channel_idx):
        """
        Извлекает указанный цветовой канал из изображения.

        Args:
            image (numpy.ndarray): Входное изображение.
            channel_idx (int): Индекс цветового канала (0 - синий, 1 - зеленый, 2 - красный).

        Returns:
            numpy.ndarray: Изображение с выделенным цветовым каналом.
        """
        channel_image = np.zeros_like(image)
        channel_image[:, :, channel_idx] = image[:, :, channel_idx]
        return channel_image

    def apply_changes(self):
        """
        Применяет изменения к изображению на основе введенных значений (размер, яркость, круг).
        """
        global resized_image
        if self.current_image is None:
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите изображение.")
            return

        try:
            # Применяем изменения только для тех полей, которые были заполнены
            new_width = int(self.width_input.text()) if self.width_input.text() else None
            new_height = int(self.height_input.text()) if self.height_input.text() else None
            brightness_value = int(self.brightness_input.text()) if self.brightness_input.text() else 0
            center_x = int(self.center_x_input.text()) if self.center_x_input.text() else None
            center_y = int(self.center_y_input.text()) if self.center_y_input.text() else None
            radius = int(self.radius_input.text()) if self.radius_input.text() else None

            if new_width and new_width <= 0:
                raise ValueError("Неверное значение ширины")
            if new_height and new_height <= 0:
                raise ValueError("Неверное значение высоты")
            if radius and radius <= 0:
                raise ValueError("Радиус должен быть положительным числом")

            # Изменяем размер изображения
            if new_width or new_height:
                if new_width and new_height:
                    resized_image = cv2.resize(self.current_image, (new_width, new_height))
                elif new_width:
                    h, w, _ = self.current_image.shape
                    ratio = new_width / w
                    resized_image = cv2.resize(self.current_image, (new_width, int(h * ratio)))
                elif new_height:
                    h, w, _ = self.current_image.shape
                    ratio = new_height / h
                    resized_image = cv2.resize(self.current_image, (int(w * ratio), new_height))
            else:
                resized_image = self.current_image

            adjusted_image = self.adjust_brightness(resized_image, brightness_value)

            if center_x is not None and center_y is not None and radius is not None:
                circled_image = self.draw_circle(adjusted_image, center_x, center_y, radius)
            else:
                circled_image = adjusted_image

            self.current_image = circled_image
            self.display_image(self.current_image)

            self.clear_inputs()

        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректные значения: {e}")

    def reset_image(self):
        """
        Сбрасывает изображение к исходному состоянию.
        """
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)

    def clear_inputs(self):
        """
        Очищает все поля ввода.
        """
        self.width_input.clear()
        self.height_input.clear()
        self.brightness_input.clear()
        self.center_x_input.clear()
        self.center_y_input.clear()
        self.radius_input.clear()

    @staticmethod
    def adjust_brightness(image, brightness):
        """
        Регулирует яркость изображения.

        Args:
            image (numpy.ndarray): Входное изображение.
            brightness (int): Значение яркости для уменьшения.

        Returns:
            numpy.ndarray: Изображение с уменьшенной яркостью.
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = np.clip(v - brightness, 0, 255)
        final_hsv = cv2.merge((h, s, v))
        image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return image

    @staticmethod
    def draw_circle(image, center_x, center_y, radius):
        """
        Рисует круг на изображении.

        Args:
            image (numpy.ndarray): Входное изображение.
            center_x (int): X координата центра круга.
            center_y (int): Y координата центра круга.
            radius (int): Радиус круга.

        Returns:
            numpy.ndarray: Изображение с нарисованным кругом.

        Raises:
            ValueError: Если координаты или радиус круга выходят за границы изображения.
        """
        height, width, _ = image.shape
        if center_x < 0 or center_x >= width or center_y < 0 or center_y >= height:
            raise ValueError("Координаты центра круга выходят за границы изображения")
        if (radius <= 0 or center_x - radius < 0 or center_x + radius >= width or center_y - radius < 0
        or center_y + radius >= height):
            raise ValueError("Радиус круга должен быть положительным числом и в пределах границ изображения")

        return cv2.circle(image, (center_x, center_y), radius, (0, 0, 255), 2)
