import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QLineEdit, QMessageBox, QFormLayout, QHBoxLayout, QStackedWidget, QWizard, QWizardPage)
from PyQt6.QtGui import QIcon, QPixmap

class Installer(QWizard):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wexium Installer")
        self.setGeometry(100, 100, 600, 400)

        self.addPage(self.createDiskPage())
        self.addPage(self.createWmPage())
        self.addPage(self.createUserPage())
        self.addPage(self.createTimezonePage())
        self.addPage(self.createSummaryPage())

        self.setWindowIcon(QIcon.fromTheme("preferences-desktop"))

    def createDiskPage(self):
        page = QWizardPage()
        page.setTitle("Выбор диска и разметки")

        layout = QFormLayout()

        self.disk_combo = QComboBox()
        self.disk_combo.addItems(self.get_disks())
        disk_label = QLabel("Выберите диск для установки:")
        disk_label.setPixmap(QIcon.fromTheme("drive-harddisk").pixmap(16, 16))
        layout.addRow(disk_label, self.disk_combo)

        self.partition_combo = QComboBox()
        self.partition_combo.addItems(["Автоматическая разметка (весь диск)", "Ручная разметка", "Установить рядом с Windows"])
        partition_label = QLabel("Выберите схему разметки диска:")
        partition_label.setPixmap(QIcon.fromTheme("drive-harddisk").pixmap(16, 16))
        layout.addRow(partition_label, self.partition_combo)

        page.setLayout(layout)
        return page

    def createWmPage(self):
        page = QWizardPage()
        page.setTitle("Выбор графической среды")

        layout = QFormLayout()

        self.wm_combo = QComboBox()
        self.wm_combo.addItems(["KDE Plasma", "BSPWM", "Hyprland"])
        wm_label = QLabel("Выберите графическую среду:")
        wm_label.setPixmap(QIcon.fromTheme("preferences-desktop").pixmap(16, 16))
        layout.addRow(wm_label, self.wm_combo)

        page.setLayout(layout)
        return page

    def createUserPage(self):
        page = QWizardPage()
        page.setTitle("Настройка пользователя")

        layout = QFormLayout()

        self.user_input = QLineEdit()
        user_label = QLabel("Имя пользователя:")
        user_label.setPixmap(QIcon.fromTheme("user").pixmap(16, 16))
        layout.addRow(user_label, self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_label = QLabel("Пароль:")
        password_label.setPixmap(QIcon.fromTheme("password").pixmap(16, 16))
        layout.addRow(password_label, self.password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_password_label = QLabel("Подтвердите пароль:")
        confirm_password_label.setPixmap(QIcon.fromTheme("password").pixmap(16, 16))
        layout.addRow(confirm_password_label, self.confirm_password_input)

        page.setLayout(layout)
        return page

    def createTimezonePage(self):
        page = QWizardPage()
        page.setTitle("Выбор часового пояса и языка")

        layout = QFormLayout()

        self.timezone_combo = QComboBox()
        self.timezone_combo.addItems(self.get_timezones())
        timezone_label = QLabel("Выберите часовой пояс:")
        timezone_label.setPixmap(QIcon.fromTheme("preferences-system-time").pixmap(16, 16))
        layout.addRow(timezone_label, self.timezone_combo)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["Русский", "English"])
        language_label = QLabel("Выберите язык:")
        language_label.setPixmap(QIcon.fromTheme("preferences-desktop-locale").pixmap(16, 16))
        layout.addRow(language_label, self.language_combo)

        page.setLayout(layout)
        return page

    def createSummaryPage(self):
        page = QWizardPage()
        page.setTitle("Подтверждение и установка")

        layout = QVBoxLayout()

        self.summary_label = QLabel("Пожалуйста, проверьте все настройки перед установкой.")
        layout.addWidget(self.summary_label)

        self.install_button = QPushButton("Установить")
        self.install_button.clicked.connect(self.install)
        layout.addWidget(self.install_button)

        page.setLayout(layout)
        return page

    def run_command(self, command):
        subprocess.run(command, shell=True, check=True)

    def get_disks(self):
        result = subprocess.run(['lsblk', '-d', '-n', '-o', 'NAME,SIZE'], stdout=subprocess.PIPE)
        disks = result.stdout.decode().splitlines()
        disk_info = []
        for disk in disks:
            name, size = disk.split()
            if 'G' in size:
                size_numeric = float(size.rstrip('G').replace(',', '.'))
                size_gb = size_numeric
                disk_info.append(f"{name} - {size_gb:.2f} ГБ")
            else:
                disk_info.append(f"{name} - {size} (Неизвестный формат)")
        return disk_info

    def get_timezones(self):
        result = subprocess.run(['timedatectl', 'list-timezones'], stdout=subprocess.PIPE)
        timezones = result.stdout.decode().splitlines()
        return timezones

    def partition_disk(self, disk, scheme):
        disk = disk.split()[0]
        if scheme == 'Автоматическая разметка (весь диск)':
            self.run_command(f"parted /dev/{disk} mklabel gpt")
            self.run_command(f"parted /dev/{disk} mkpart primary ext4 1MiB 100%")
            self.run_command(f"mkfs.ext4 /dev/{disk}1")
            self.run_command(f"mount /dev/{disk}1 /mnt")
        elif scheme == 'Ручная разметка':
            QMessageBox.information(self, "Информация", "Запустите утилиту для разметки диска (например, cfdisk или fdisk) и создайте разделы.")
            self.run_command(f"cfdisk /dev/{disk}")
            root_partition = input("Введите имя корневого раздела (например, /dev/sda1): ")
            self.run_command(f"mkfs.ext4 {root_partition}")
            self.run_command(f"mount {root_partition} /mnt")
            home_partition = input("Введите имя раздела /home (если есть, иначе оставьте пустым): ")
            if home_partition:
                self.run_command(f"mkfs.ext4 {home_partition}")
                self.run_command(f"mkdir -p /mnt/home")
                self.run_command(f"mount {home_partition} /mnt/home")
        elif scheme == 'Установить рядом с Windows':
            QMessageBox.information(self, "Информация", "Запустите утилиту для разметки диска (например, cfdisk или fdisk) и создайте разделы для Linux.")
            self.run_command(f"cfdisk /dev/{disk}")
            root_partition = input("Введите имя корневого раздела (например, /dev/sda1): ")
            self.run_command(f"mkfs.ext4 {root_partition}")
            self.run_command(f"mount {root_partition} /mnt")
            home_partition = input("Введите имя раздела /home (если есть, иначе оставьте пустым): ")
            if home_partition:
                self.run_command(f"mkfs.ext4 {home_partition}")
                self.run_command(f"mkdir -p /mnt/home")
                self.run_command(f"mount {home_partition} /mnt/home")

    def install_base_system(self):
        self.run_command("pacstrap /mnt base base-devel linux linux-firmware")
        self.run_command("genfstab -U /mnt >> /mnt/etc/fstab")
        self.run_command("arch-chroot /mnt ln -sf /usr/share/zoneinfo/Region/City /etc/localtime")
        self.run_command("arch-chroot /mnt hwclock --systohc")
        self.run_command("arch-chroot /mnt pacman -S nano vim sudo os-prober grub --noconfirm")
        self.run_command("arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB")
        self.run_command("arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg")

    def create_user(self, username, password):
        self.run_command(f"arch-chroot /mnt useradd -m -G wheel -s /bin/bash {username}")
        self.run_command(f"arch-chroot /mnt bash -c 'echo \"{username}:{password}\" | chpasswd'")
        self.run_command("arch-chroot /mnt sed -i 's/# %wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/' /etc/sudoers")

    def install_packages(self, packages):
        self.run_command(f"arch-chroot /mnt pacman -S {' '.join(packages)} --noconfirm")

    def copy_configs(self, wm, username):
        config_path = f"/etc/wexium/{wm}"
        home_config_path = f"/mnt/home/{username}/.config/{wm}"
        if not os.path.exists(home_config_path):
            os.makedirs(home_config_path)
        for file in os.listdir(config_path):
            full_file_path = os.path.join(config_path, file)
            if os.path.isfile(full_file_path):
                self.run_command(f"cp {full_file_path} {home_config_path}")

    def validate_password(self, password):
        if len(password) < 8:
            return False, "Пароль должен быть не менее 8 символов"
        if not any(char.isdigit() for char in password):
            return False, "Пароль должен содержать хотя бы одну цифру"
        if not any(char.isupper() for char in password):
            return False, "Пароль должен содержать хотя бы одну заглавную букву"
        if not any(char.islower() for char in password):
            return False, "Пароль должен содержать хотя бы одну строчную букву"
        return True, ""

    def install(self):
        disk = self.disk_combo.currentText()
        partition_scheme = self.partition_combo.currentText()
        wm = self.wm_combo.currentText()
        username = self.user_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        timezone = self.timezone_combo.currentText()
        language = self.language_combo.currentText()

        if not username:
            QMessageBox.critical(self, "Ошибка", "Имя пользователя не может быть пустым!")
            return
        if not password:
            QMessageBox.critical(self, "Ошибка", "Пароль не может быть пустым!")
            return
        if password != confirm_password:
            QMessageBox.critical(self, "Ошибка", "Пароли не совпадают!")
            return
        valid, message = self.validate_password(password)
        if not valid:
            QMessageBox.critical(self, "Ошибка", message)
            return

        reply = QMessageBox.question(self, "Подтверждение установки", "Вы уверены, что хотите установить систему?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        self.partition_disk(disk, partition_scheme)
        self.install_base_system()
        self.create_user(username, password)

        if wm == 'KDE Plasma':
            self.install_packages(['plasma', 'plasma-meta', 'sddm'])
            self.run_command("arch-chroot /mnt systemctl enable sddm")
            self.copy_configs('kde', username)
        elif wm == 'BSPWM':
            self.install_packages(['bspwm', 'sxhkd', 'lightdm', 'lightdm-gtk-greeter'])
            self.run_command("arch-chroot /mnt systemctl enable lightdm")
            self.copy_configs('bspwm', username)
        elif wm == 'Hyprland':
            self.install_packages(['hyprland', 'lightdm', 'lightdm-gtk-greeter'])
            self.run_command("arch-chroot /mnt systemctl enable lightdm")
            self.copy_configs('hyprland', username)

        self.run_command(f"arch-chroot /mnt ln -sf /usr/share/zoneinfo/{timezone} /etc/localtime")
        self.run_command("arch-chroot /mnt hwclock --systohc")
        self.run_command(f"arch-chroot /mnt locale-gen")
        self.run_command(f"arch-chroot /mnt localectl set-locale LANG={language}")

        QMessageBox.information(self, "Установка завершена", f"{wm} установлена и настроена!")

if __name__ == "__main__":
    app = QApplication([])
    window = Installer()
    window.show()
    app.exec()