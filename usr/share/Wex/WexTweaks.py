import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
    QLabel, QComboBox, QCheckBox, QMessageBox, QInputDialog, QListWidget, QListWidgetItem,
    QTabWidget, QLineEdit
)
from PyQt5.QtCore import QSettings, QTranslator, QLocale


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.translator = QTranslator()
        self.current_language = "en"

        self.setWindowTitle("Wex Tweaks")
        self.setGeometry(100, 100, 800, 600)

        # Language selector
        self.language_selector = QComboBox(self)
        self.language_selector.addItem("English", "en")
        self.language_selector.addItem("Русский", "ru")
        self.language_selector.currentIndexChanged.connect(self.switch_language)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.language_selector)

        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # General tab
        self.general_tab = QWidget()
        self.general_layout = QVBoxLayout()
        self.general_tab.setLayout(self.general_layout)

        self.welcome_label = QLabel(self.tr("Welcome to Wex Tweaks"), self)
        self.general_layout.addWidget(self.welcome_label)

        self.repo_label = QLabel(self.tr("Select Repository:"), self)
        self.general_layout.addWidget(self.repo_label)

        self.repo_combobox = QComboBox(self)
        self.repo_combobox.addItems(["core", "extra", "community", "multilib", "chaotic-aur"])
        self.general_layout.addWidget(self.repo_combobox)

        self.chaotic_aur_checkbox = QCheckBox(self.tr("Enable Chaotic AUR"), self)
        self.general_layout.addWidget(self.chaotic_aur_checkbox)

        self.update_mirrorlist_button = QPushButton(self.tr("Update Mirrorlist"), self)
        self.update_mirrorlist_button.clicked.connect(self.update_mirrorlist)
        self.general_layout.addWidget(self.update_mirrorlist_button)

        self.update_system_button = QPushButton(self.tr("Update System"), self)
        self.update_system_button.clicked.connect(self.update_system)
        self.general_layout.addWidget(self.update_system_button)

        self.install_package_button = QPushButton(self.tr("Install Package"), self)
        self.install_package_button.clicked.connect(self.install_package)
        self.general_layout.addWidget(self.install_package_button)

        self.clean_system_button = QPushButton(self.tr("Clean System"), self)
        self.clean_system_button.clicked.connect(self.clean_system)
        self.general_layout.addWidget(self.clean_system_button)

        self.clean_cache_button = QPushButton(self.tr("Clean Package Cache"), self)
        self.clean_cache_button.clicked.connect(self.clean_cache)
        self.general_layout.addWidget(self.clean_cache_button)

        self.check_system_button = QPushButton(self.tr("Check System Status"), self)
        self.check_system_button.clicked.connect(self.check_system_status)
        self.general_layout.addWidget(self.check_system_button)

        self.manage_autostart_button = QPushButton(self.tr("Manage Autostart Applications"), self)
        self.manage_autostart_button.clicked.connect(self.manage_autostart)
        self.general_layout.addWidget(self.manage_autostart_button)

        self.tabs.addTab(self.general_tab, self.tr("General"))

        # AUR Helpers tab
        self.aur_helpers_tab = QWidget()
        self.aur_helpers_layout = QVBoxLayout()
        self.aur_helpers_tab.setLayout(self.aur_helpers_layout)

        self.aur_helpers_label = QLabel(self.tr("Install AUR Helpers:"), self)
        self.aur_helpers_layout.addWidget(self.aur_helpers_label)

        self.aur_helpers_list = QListWidget(self)
        self.aur_helpers_list.addItems(["yay", "paru", "bauh", "pamac-aur"])
        self.aur_helpers_list.setSelectionMode(QListWidget.MultiSelection)
        self.aur_helpers_layout.addWidget(self.aur_helpers_list)

        self.install_aur_helper_button = QPushButton(self.tr("Install Selected AUR Helpers"), self)
        self.install_aur_helper_button.clicked.connect(self.install_aur_helpers)
        self.aur_helpers_layout.addWidget(self.install_aur_helper_button)

        self.tabs.addTab(self.aur_helpers_tab, self.tr("AUR Helpers"))

        # Popular Programs tab
        self.popular_programs_tab = QWidget()
        self.popular_programs_layout = QVBoxLayout()
        self.popular_programs_tab.setLayout(self.popular_programs_layout)

        self.popular_programs_label = QLabel(self.tr("Install Popular Programs:"), self)
        self.popular_programs_layout.addWidget(self.popular_programs_label)

        self.popular_programs_list = QListWidget(self)
        self.popular_programs_list.addItems([
            "Steam", "portProton", "Discord", "Visual Studio Code", "GIMP", "Blender",
            "OBS Studio", "Krita",
            "Wine", "Vulkan-tools",
            "PlayOnLinux", "wine",
            "telegram-desktop", "VLC", "Audacity", "mpv",
            "qBittorrent", "Deluge",
            "FileZilla", "GParted", "BleachBit", "VirtualBox", "virt-manager", "qemu",
            "gnome-boxes", "Remmina", "ethtool", "iperf",
            "nmap", "Inkscape",
            "LibreOffice",
            "Eclipse", "Android Studio"
        ])
        self.popular_programs_list.setSelectionMode(QListWidget.MultiSelection)
        self.popular_programs_layout.addWidget(self.popular_programs_list)

        self.install_selected_program_button = QPushButton(self.tr("Install Selected Programs"), self)
        self.install_selected_program_button.clicked.connect(self.install_selected_programs)
        self.popular_programs_layout.addWidget(self.install_selected_program_button)

        self.tabs.addTab(self.popular_programs_tab, self.tr("Popular Programs"))

        # Systemd Services tab
        self.systemd_services_tab = QWidget()
        self.systemd_services_layout = QVBoxLayout()
        self.systemd_services_tab.setLayout(self.systemd_services_layout)

        self.services_label = QLabel(self.tr("Manage Systemd Services:"), self)
        self.systemd_services_layout.addWidget(self.services_label)

        self.services_list = QListWidget(self)
        self.systemd_services_layout.addWidget(self.services_list)
        self.refresh_services_list()

        systemd_buttons_layout = QHBoxLayout()

        self.start_service_button = QPushButton(self.tr("Start"))
        self.start_service_button.clicked.connect(self.start_service)
        systemd_buttons_layout.addWidget(self.start_service_button)

        self.stop_service_button = QPushButton(self.tr("Stop"))
        self.stop_service_button.clicked.connect(self.stop_service)
        systemd_buttons_layout.addWidget(self.stop_service_button)

        self.restart_service_button = QPushButton(self.tr("Restart"))
        self.restart_service_button.clicked.connect(self.restart_service)
        systemd_buttons_layout.addWidget(self.restart_service_button)

        self.enable_service_button = QPushButton(self.tr("Enable"))
        self.enable_service_button.clicked.connect(self.enable_service)
        systemd_buttons_layout.addWidget(self.enable_service_button)

        self.disable_service_button = QPushButton(self.tr("Disable"))
        self.disable_service_button.clicked.connect(self.disable_service)
        systemd_buttons_layout.addWidget(self.disable_service_button)

        self.create_service_button = QPushButton(self.tr("Create"))
        self.create_service_button.clicked.connect(self.create_service)
        systemd_buttons_layout.addWidget(self.create_service_button)

        self.delete_service_button = QPushButton(self.tr("Delete"))
        self.delete_service_button.clicked.connect(self.delete_service)
        systemd_buttons_layout.addWidget(self.delete_service_button)

        self.systemd_services_layout.addLayout(systemd_buttons_layout)
        self.tabs.addTab(self.systemd_services_tab, self.tr("Systemd Services"))

        # Layout setup
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Load settings
        self.settings = QSettings("WexTweaks", "AppSettings")
        self.load_settings()

    def switch_language(self, index):
        language = self.language_selector.itemData(index)
        if language == self.current_language:
            return

        if language == "ru":
            self.translator.load("wex_tweaks_ru.qm")
            self.current_language = "ru"
        else:
            self.translator.load("wex_tweaks_en.qm")
            self.current_language = "en"

        QApplication.instance().installTranslator(self.translator)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("Wex Tweaks"))
        self.welcome_label.setText(self.tr("Welcome to Wex Tweaks"))
        self.repo_label.setText(self.tr("Select Repository:"))
        self.chaotic_aur_checkbox.setText(self.tr("Enable Chaotic AUR"))
        self.update_mirrorlist_button.setText(self.tr("Update Mirrorlist"))
        self.update_system_button.setText(self.tr("Update System"))
        self.install_package_button.setText(self.tr("Install Package"))
        self.clean_system_button.setText(self.tr("Clean System"))
        self.clean_cache_button.setText(self.tr("Clean Package Cache"))
        self.check_system_button.setText(self.tr("Check System Status"))
        self.manage_autostart_button.setText(self.tr("Manage Autostart Applications"))
        self.aur_helpers_label.setText(self.tr("Install AUR Helpers:"))
        self.install_aur_helper_button.setText(self.tr("Install Selected AUR Helpers"))
        self.popular_programs_label.setText(self.tr("Install Popular Programs:"))
        self.install_selected_program_button.setText(self.tr("Install Selected Programs"))
        self.services_label.setText(self.tr("Manage Systemd Services:"))
        self.start_service_button.setText(self.tr("Start"))
        self.stop_service_button.setText(self.tr("Stop"))
        self.restart_service_button.setText(self.tr("Restart"))
        self.enable_service_button.setText(self.tr("Enable"))
        self.disable_service_button.setText(self.tr("Disable"))
        self.create_service_button.setText(self.tr("Create"))
        self.delete_service_button.setText(self.tr("Delete"))

    def load_settings(self):
        self.settings.beginGroup("MainWindow")
        self.resize(self.settings.value("size", self.size()))
        self.move(self.settings.value("pos", self.pos()))
        self.settings.endGroup()

    def closeEvent(self, event):
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.endGroup()

    def update_mirrorlist(self):
        try:
            subprocess.run(["sudo", "reflector", "--verbose", "--latest", "5", "--sort", "rate", "--save", "/etc/pacman.d/mirrorlist"], check=True)
            QMessageBox.information(self, "Success", "Mirrorlist updated successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to update mirrorlist")

    def update_system(self):
        try:
            subprocess.run(["sudo", "pacman", "-Syu"], check=True)
            QMessageBox.information(self, "Success", "System updated successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to update system")

    def install_package(self):
        package, ok = QInputDialog.getText(self, "Install Package", "Enter package name:")
        if ok and package:
            try:
                subprocess.run(["yay", "-S", package], check=True)
                QMessageBox.information(self, "Success", f"Package '{package}' installed successfully")
            except subprocess.CalledProcessError:
                QMessageBox.critical(self, "Error", f"Failed to install package '{package}'")

    def clean_system(self):
        try:
            subprocess.run(["sudo", "pacman", "-Rns", "$(pacman -Qdtq)"], shell=True, check=True)
            subprocess.run(["sudo", "pacman", "-Sc"], shell=True, check=True)
            QMessageBox.information(self, "Success", "System cleaned successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to clean system")

    def clean_cache(self):
        try:
            subprocess.run(["sudo", "paccache", "-r"], check=True)
            QMessageBox.information(self, "Success", "Package cache cleaned successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to clean package cache")

    def check_system_status(self):
        try:
            result = subprocess.run(["systemctl", "status"], capture_output=True, text=True, check=True)
            QMessageBox.information(self, "System Status", result.stdout)
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to check system status")

    def manage_autostart(self):
        try:
            subprocess.run(["xdg-autostart"], check=True)
            QMessageBox.information(self, "Success", "Autostart applications managed successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to manage autostart applications")

    def install_aur_helpers(self):
        selected_helpers = [item.text() for item in self.aur_helpers_list.selectedItems()]
        for helper in selected_helpers:
            try:
                subprocess.run(["git", "clone", f"https://aur.archlinux.org/{helper}.git"], check=True)
                subprocess.run(["makepkg", "-si", "--noconfirm"], cwd=f"./{helper}", check=True)
                QMessageBox.information(self, "Success", f"AUR helper '{helper}' installed successfully")
            except subprocess.CalledProcessError:
                QMessageBox.critical(self, "Error", f"Failed to install AUR helper '{helper}'")

    def install_selected_programs(self):
        selected_programs = [item.text() for item in self.popular_programs_list.selectedItems()]
        for program in selected_programs:
            try:
                subprocess.run(["sudo", "pacman", "-S", program.lower().replace(" ", "-")], check=True)
                QMessageBox.information(self, "Success", f"Program '{program}' installed successfully")
            except subprocess.CalledProcessError:
                QMessageBox.critical(self, "Error", f"Failed to install program '{program}'")

    def refresh_services_list(self):
        self.services_list.clear()
        try:
            result = subprocess.run(["systemctl", "list-unit-files", "--type=service", "--state=enabled,disabled"], capture_output=True, text=True, check=True)
            for line in result.stdout.split("\n")[1:]:
                if line:
                    service_name = line.split()[0]
                    item = QListWidgetItem(service_name)
                    self.services_list.addItem(item)
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to retrieve services list")

    def start_service(self):
        service = self.services_list.currentItem().text()
        try:
            subprocess.run(["sudo", "systemctl", "start", service], check=True)
            QMessageBox.information(self, "Success", f"Service '{service}' started successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"Failed to start service '{service}'")

    def stop_service(self):
        service = self.services_list.currentItem().text()
        try:
            subprocess.run(["sudo", "systemctl", "stop", service], check=True)
            QMessageBox.information(self, "Success", f"Service '{service}' stopped successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"Failed to stop service '{service}'")

    def restart_service(self):
        service = self.services_list.currentItem().text()
        try:
            subprocess.run(["sudo", "systemctl", "restart", service], check=True)
            QMessageBox.information(self, "Success", f"Service '{service}' restarted successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"Failed to restart service '{service}'")

    def enable_service(self):
        service = self.services_list.currentItem().text()
        try:
            subprocess.run(["sudo", "systemctl", "enable", service], check=True)
            QMessageBox.information(self, "Success", f"Service '{service}' enabled successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"Failed to enable service '{service}'")

    def disable_service(self):
        service = self.services_list.currentItem().text()
        try:
            subprocess.run(["sudo", "systemctl", "disable", service], check=True)
            QMessageBox.information(self, "Success", f"Service '{service}' disabled successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"Failed to disable service '{service}'")

    def create_service(self):
        service_name, ok = QInputDialog.getText(self, "Create New Service", "Enter service name (e.g., my_service):")
        if ok and service_name:
            service_content, ok = QInputDialog.getMultiLineText(self, "Create New Service", "Enter service file content:", 
            "[Unit]\nDescription=My custom service\n\n[Service]\nExecStart=/path/to/executable\n\n[Install]\nWantedBy=multi-user.target")
            if ok and service_content:
                service_path = f"/etc/systemd/system/{service_name}.service"
                try:
                    with open(service_path, "w") as service_file:
                        service_file.write(service_content)
                    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
                    self.refresh_services_list()
                    QMessageBox.information(self, "Success", f"Service '{service_name}' created successfully")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create service '{service_name}': {e}")

    def delete_service(self):
        service = self.services_list.currentItem().text()
        confirm = QMessageBox.question(self, "Delete Service", f"Are you sure you want to delete the service '{service}'?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                subprocess.run(["sudo", "systemctl", "disable", service], check=True)
                subprocess.run(["sudo", "rm", f"/etc/systemd/system/{service}"], check=True)
                QMessageBox.information(self, "Success", f"Service '{service}' deleted successfully")
                self.refresh_services_list()
            except subprocess.CalledProcessError:
                QMessageBox.critical(self, "Error", f"Failed to delete service '{service}'")

    def add_user(self):
        username, ok = QInputDialog.getText(self, "Add User", "Enter new username:")
        if ok and username:
            try:
                subprocess.run(["sudo", "useradd", "-m", "-s", "/bin/bash", username], check=True)
                subprocess.run(["sudo", "passwd", username], check=True)
                QMessageBox.information(self, "Success", f"User '{username}' added successfully")
            except subprocess.CalledProcessError:
                QMessageBox.critical(self, "Error", f"Failed to add user '{username}'")

    def delete_user(self):
        username, ok = QInputDialog.getText(self, "Delete User", "Enter username to delete:")
        if ok and username:
            confirm = QMessageBox.question(self, "Delete User", f"Are you sure you want to delete the user '{username}'?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                try:
                    subprocess.run(["sudo", "userdel", "-r", username], check=True)
                    QMessageBox.information(self, "Success", f"User '{username}' deleted successfully")
                except subprocess.CalledProcessError:
                    QMessageBox.critical(self, "Error", f"Failed to delete user '{username}'")

    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())