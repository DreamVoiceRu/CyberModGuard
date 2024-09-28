import sys
import os
import shutil
import webbrowser

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog, QVBoxLayout, QPushButton, QTextEdit
import winreg
import time
from threading import Thread
import requests


class InstallerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        try:
            self.setWindowTitle("RUS DUB INSTALLER FOR CYBERPUNK2077:PHANTOM LIBERTY BY DREAMVOICE")
            self.setFixedSize(1200, 800)
            self.setWindowIcon(QIcon("img/logo_ico.png"))
            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.setContentsMargins(20, 20, 20, 20)  # Уменьшаем отступы
            main_layout.setSpacing(15)  # Устанавливаем расстояние между элементами

            # Логотип
            logo_label = QtWidgets.QLabel(self)
            logo_pixmap = QtGui.QPixmap("img/logo.png")
            if not logo_pixmap.isNull():
                scaled_logo = logo_pixmap.scaled(900, 250,
                                                 QtCore.Qt.KeepAspectRatio)  # Увеличиваем логотип пропорционально
                logo_label.setPixmap(scaled_logo)
            logo_label.setAlignment(QtCore.Qt.AlignCenter)
            main_layout.addWidget(logo_label)

            # Блок пути к игре
            path_group_box = QtWidgets.QGroupBox("Настройки пути")
            path_layout = QtWidgets.QHBoxLayout(path_group_box)
            self.game_path_label = QtWidgets.QLabel("Путь к игре: ", self)
            self.game_path = QtWidgets.QLabel(self.find_game_path(), self)
            self.open_folder_btn = QtWidgets.QPushButton("Открыть папку", self)
            self.open_folder_btn.setStyleSheet(
                "background-color: #1E90FF; color: white; font-size: 16px; padding: 10px 20px;")
            self.open_folder_btn.clicked.connect(self.open_folder)
            path_layout.addWidget(self.game_path_label)
            path_layout.addWidget(self.game_path)
            path_layout.addWidget(self.open_folder_btn)
            main_layout.addWidget(path_group_box)

            # Блок выбора модов
            mod_group_box = QtWidgets.QGroupBox("Выбор модификаций")
            checkbox_layout = QtWidgets.QVBoxLayout(mod_group_box)
            self.checkbox_dogtown = QtWidgets.QCheckBox('Субтитры ДогТауна', self)
            self.checkbox_radio = QtWidgets.QCheckBox('Радио шансон', self)
            self.checkbox_base_dub = QtWidgets.QCheckBox('Дубляж базовый', self)
            self.checkbox_dlc_dub = QtWidgets.QCheckBox('Дубляж DLC', self)
            self.checkbox_dogtown.setChecked(True)
            self.checkbox_radio.setChecked(True)
            self.checkbox_base_dub.setChecked(True)
            self.checkbox_dlc_dub.setChecked(True)
            checkbox_layout.addWidget(self.checkbox_dogtown)
            checkbox_layout.addWidget(self.checkbox_radio)
            checkbox_layout.addWidget(self.checkbox_base_dub)
            checkbox_layout.addWidget(self.checkbox_dlc_dub)
            main_layout.addWidget(mod_group_box)

            # Блок с кнопками
            button_layout = QtWidgets.QHBoxLayout()
            self.install_button = QtWidgets.QPushButton("Начать установку", self)
            self.install_button.setStyleSheet(
                "background-color: #8A2BE2; color: white; font-size: 20px; padding: 20px;")
            self.install_button.clicked.connect(self.start_installation)
            self.help_button = QtWidgets.QPushButton("Инструкция и описание", self)
            self.help_button.setStyleSheet(
                "background-color: #1E90FF; color: white; font-size: 20px; padding: 20px 20px;")
            self.help_button.clicked.connect(self.show_help)
            button_layout.addWidget(self.install_button)
            button_layout.addWidget(self.help_button)
            main_layout.addLayout(button_layout)

            # Прогресс-бар
            self.progress_bar = QtWidgets.QProgressBar(self)
            self.progress_bar.setValue(0)
            main_layout.addWidget(self.progress_bar)

            self.setLayout(main_layout)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при инициализации интерфейса: {str(e)}")

    def download_logo(self, url):
        """ Загрузка изображения с интернета. """
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = response.content
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(image_data)
            return pixmap
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить логотип: {str(e)}")
            return None

    def find_game_path(self):
        """ Поиск пути к игре из нескольких источников: Steam, GOG, и других. """
        try:

            steam_path = self.find_game_in_steam()
            if steam_path:
                return steam_path


            gog_path = self.find_game_in_gog()
            if gog_path:
                return gog_path


            other_path = self.find_game_in_other_launchers()
            if other_path:
                return other_path


            folder = QFileDialog.getExistingDirectory(self, "Выберите папку с игрой Cyberpunk 2077")
            if folder:
                return folder

            return "Игра не найдена."

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось найти путь к игре: {str(e)}")
            return "Ошибка поиска пути."

    def find_game_in_steam(self):
        """ Поиск игры в реестре Steam. """
        try:
            steam_key_path = r"SOFTWARE\Valve\Steam"
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, steam_key_path)
            steam_install_path, _ = winreg.QueryValueEx(reg_key, "InstallPath")
            winreg.CloseKey(reg_key)


            library_folders_path = os.path.join(steam_install_path, "steamapps", "libraryfolders.vdf")
            if os.path.exists(library_folders_path):
                with open(library_folders_path, 'r') as f:
                    content = f.read()


                if '1091500' in content:
                    for line in content.splitlines():
                        if 'path' in line:

                            lib_path = line.split('"')[3]
                            game_path = os.path.join(lib_path, "steamapps", "common", "Cyberpunk 2077")
                            archive_path = os.path.join(game_path, "archive")


                            if os.path.exists(game_path) and os.path.exists(archive_path):
                                return game_path

            return None

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None


    def find_game_in_gog(self):
        """ Поиск игры через реестр GOG. """
        try:
            gog_key_path = r"SOFTWARE\WOW6432Node\GOG.com\Games\1423049311"
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, gog_key_path)
            game_path, _ = winreg.QueryValueEx(reg_key, "PATH")
            archive_path = os.path.join(game_path, "archive")

            if os.path.exists(game_path) and os.path.exists(archive_path):
                return game_path
            winreg.CloseKey(reg_key)
            if os.path.exists(game_path):
                return game_path
            return None

        except Exception as e:
            return None

    def find_game_in_other_launchers(self):
        """ Поиск игры в других лаунчерах (Epic Games и других). """
        try:

            epic_games_path = r"C:\Program Files\Epic Games\Cyberpunk 2077"
            if os.path.exists(epic_games_path) and self.check_archive_exists(epic_games_path):
                return epic_games_path


            possible_paths = [
                r"C:\Games\Cyberpunk 2077",
                r"D:\Games\Cyberpunk 2077"
            ]

            for path in possible_paths:
                if os.path.exists(path) and self.check_archive_exists(path):
                    return path

            return None

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None

    def check_archive_exists(self, path):
        """ Проверка наличия папки archive. """
        archive_path = os.path.join(path, "archive")
        return os.path.exists(archive_path)

    def open_folder(self):
        """ Открытие папки с игрой. """
        try:
            folder = QFileDialog.getExistingDirectory(self, "Выберите папку с игрой", self.game_path.text())
            if folder:
                self.game_path.setText(folder)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть папку: {str(e)}")

    def start_installation(self):
        """ Запуск процесса установки с проверкой наличия модов и копированием файлов. """
        try:
            mod_path = os.path.join(self.game_path.text(), "archive", "pc", "mod")
            if not os.path.exists(mod_path):
                os.makedirs(mod_path)


            if os.listdir(mod_path):
                reply = QMessageBox.question(self, "Конфликт модов",
                                             "У вас уже другие моды. Вы уверены, что не будет конфликтов?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    self.open_folder()
                    return


            self.thread = Thread(target=self.install_mods)
            self.thread.start()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при запуске установки: {str(e)}")

    def show_help(self):

        file_path = os.path.join(os.getcwd(), 'README.html')


        file_url = 'file://' + file_path


        webbrowser.open(file_url)


    def start_installation(self):
        """ Запуск процесса установки с проверкой наличия модов и копированием файлов. """
        try:
            mod_path = os.path.join(self.game_path.text(), "archive", "pc", "mod")
            if not os.path.exists(mod_path):
                os.makedirs(mod_path)


            if os.listdir(mod_path):
                reply = QMessageBox.question(self, "Конфликт модов",
                                             "У вас уже другие моды. Вы уверены, что не будет конфликтов?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:

                    return


            self.thread = Thread(target=self.install_mods)
            self.thread.start()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при запуске установки: {str(e)}")

    def install_mods(self):
        """ Установка модов с прогрессом. """
        try:
            source_dir = os.path.join(os.getcwd(), "mod")
            mod_files = {
                "Dogtown_Subs_Switch_by_DreamVoice.archive": self.checkbox_dogtown.isChecked(),
                "Radio_Shanson_by_Tokyo(optionally).archive": self.checkbox_radio.isChecked(),
                "Rus_Dub_Base_by_DreamVoice.archive": self.checkbox_base_dub.isChecked(),
                "Rus_Dub_DLC_by_DreamVoice.archive": self.checkbox_dlc_dub.isChecked()
            }

            total_files = len([f for f, checked in mod_files.items() if checked])
            self.progress_bar.setMaximum(total_files)
            progress = 0

            for file_name, should_copy in mod_files.items():
                if not should_copy:
                    continue
                source_file = os.path.join(source_dir, file_name)
                destination_file = os.path.join(self.game_path.text(), "archive", "pc", "mod", file_name)
                shutil.copy(source_file, destination_file)
                progress += 1
                self.progress_bar.setValue(progress)
                time.sleep(1)


            QMessageBox.information(self, "Установка завершена", "Все моды успешно установлены!")
            self.progress_bar.setValue(0)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при установке модов: {str(e)}")



def main():
    try:
        app = QtWidgets.QApplication(sys.argv)


        app.setStyle("Fusion")
        dark_palette = QtGui.QPalette()
        dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
        dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        app.setPalette(dark_palette)

        window = InstallerApp()
        window.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(f"Ошибка запуска приложения: {str(e)}")


if __name__ == "__main__":
    main()
