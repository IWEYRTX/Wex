import sys
import webbrowser
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QProcess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WexQS")
        layout = QVBoxLayout()

        # Приветственное сообщение
        self.welcome_label = QLabel("Добро пожаловать в WexQS!\nЗдесь вы можете найти полезные ссылки:")
        layout.addWidget(self.welcome_label)

        # Кнопки для открытия ссылок
        self.open_issues_button = QPushButton("Баг трекер")
        self.open_issues_button.clicked.connect(lambda: webbrowser.open("https://github.com/IWEYRTX/Wex/issues"))
        layout.addWidget(self.open_issues_button)

        self.open_distribution_button = QPushButton("Wex на GitHub")
        self.open_distribution_button.clicked.connect(lambda: webbrowser.open("https://github.com/Wexium/"))
        layout.addWidget(self.open_distribution_button)

        self.launch_app_button = QPushButton("Запустить WexTweak")
        self.launch_app_button.clicked.connect(self.launch_app)
        layout.addWidget(self.launch_app_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def launch_app(self):
        app_name = "WexTweak.py"
        process = QProcess()
        process.start(f"pkexec python /usr/share/wex/{app_name}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())