import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QMessageBox

class WexQS(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WexQS")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.welcome_label = QLabel("Добро пожаловать в WexQS!")
        self.layout.addWidget(self.welcome_label)

        self.tweaker_button = QPushButton("Запустить WexTweaks")
        self.tweaker_button.clicked.connect(self.run_tweaker)
        self.layout.addWidget(self.tweaker_button)

        self.install_button = QPushButton("Запустить установку системы")
        self.install_button.clicked.connect(self.run_installer)
        self.layout.addWidget(self.install_button)

    def run_tweaker(self):
        try:
            subprocess.run(['pkexec', 'python3', '/usr/share/Wex/WexTweaks.py'], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить WexTweaks: {e}")

    def run_installer(self):
        try:
            subprocess.run(['pkexec', 'python3', '/usr/share/Wex/Install.py'], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить установку системы: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WexQS()
    window.show()
    sys.exit(app.exec())