import subprocess
import sys
import os
import requests
import zipfile
import psutil
import shutil
import webbrowser

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon, QFontDatabase, QFont
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog, QVBoxLayout, QPushButton, QTextEdit


import winreg
import time
from threading import Thread



class InstallerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.perform_initial_checks()

    def initUI(self):
        try:
            self.setWindowTitle("Установщик Русской Озвучки Cyberpunk 2077 – Phantom Liberty (DreamVoice)")
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
            path_group_box.setStyleSheet("font-size: 14px;")
            path_layout = QtWidgets.QHBoxLayout(path_group_box)
            self.game_path_label = QtWidgets.QLabel("Путь к игре: ", self)
            self.game_path_label.setStyleSheet("font-size: 14px;")
            self.game_path = QtWidgets.QLabel(self.find_game_path(), self)
            self.game_path.setStyleSheet(self.color_change(self.game_path.text()))
            self.open_folder_btn = QtWidgets.QPushButton("Выбрать папку", self)
            self.open_folder_btn.setStyleSheet(
                "background-color: #9370DB; color: black; font-size: 16px; padding: 10px 20px;")
            self.open_folder_btn.clicked.connect(self.open_folder)
            path_layout.addWidget(self.game_path_label)
            path_layout.addWidget(self.game_path)
            path_layout.addWidget(self.open_folder_btn)
            main_layout.addWidget(path_group_box)

            # Блок выбора модов
            mod_group_box = QtWidgets.QGroupBox("Выбор модификаций")
            mod_group_box.setStyleSheet("font-size: 14px;")
            checkbox_layout = QtWidgets.QHBoxLayout(mod_group_box)
            # Кнопка для выделения/снятия выделения всех чекбоксов
            self.toggle_button = QtWidgets.QPushButton("Выделить/Отменить все", self)
            self.toggle_button.setStyleSheet("background-color: #4682B4; color: black; font-size: 20px; padding: 10px 20px; height:70px;width:10px")


            # Функция для переключения состояния чекбоксов
            def toggle_all_checkboxes():
                # Если все чекбоксы не отмечены, то отмечаем их, иначе снимаем выделение
                all_checked = self.checkbox_dogtown.isChecked() and self.checkbox_radio.isChecked() and \
                              self.checkbox_base_dub.isChecked() and self.checkbox_dlc_dub.isChecked()

                new_state = not all_checked
                self.checkbox_dogtown.setChecked(new_state)
                self.checkbox_radio.setChecked(new_state)
                self.checkbox_base_dub.setChecked(new_state)
                self.checkbox_dlc_dub.setChecked(new_state)

            # Подключаем кнопку к функции
            self.toggle_button.clicked.connect(toggle_all_checkboxes)

            # Добавляем кнопку в layout справа от текста
            checkbox_layout.addWidget(self.toggle_button)



            # Группа 1: Русификация субтитров и радио
            group1_layout = QtWidgets.QVBoxLayout()
            self.checkbox_dogtown = QtWidgets.QCheckBox('Русификация субтитров ДогТауна', self)
            self.checkbox_radio = QtWidgets.QCheckBox("Добавить радио 'Шансон' (опционально)", self)
            self.checkbox_dogtown.setChecked(True)
            self.checkbox_radio.setChecked(True)
            group1_layout.addWidget(self.checkbox_dogtown)
            group1_layout.addWidget(self.checkbox_radio)

            # Группа 2: Озвучка
            group2_layout = QtWidgets.QVBoxLayout()
            self.checkbox_base_dub = QtWidgets.QCheckBox('Доозвученные диалоги из Основной игры', self)
            self.checkbox_dlc_dub = QtWidgets.QCheckBox('Озвученное дополнение «Призрачная свобода»', self)
            self.checkbox_base_dub.setChecked(True)
            self.checkbox_dlc_dub.setChecked(True)
            group2_layout.addWidget(self.checkbox_base_dub)
            group2_layout.addWidget(self.checkbox_dlc_dub)

            # Добавляем группы в горизонтальный макет
            checkbox_layout.addLayout(group1_layout)
            checkbox_layout.addLayout(group2_layout)

            # Добавляем группу в основной макет
            main_layout.addWidget(mod_group_box)

            # Блок с кнопками
            button_layout = QtWidgets.QHBoxLayout()

            # Кнопка "Установить модификации"
            self.install_button = QtWidgets.QPushButton("Установить модификации", self)
            self.install_button.setStyleSheet(
                "background-color: #9370DB; color: black; font-size: 20px; padding: 20px;")
            self.install_button.clicked.connect(self.start_installation)


            # Кнопка "Руководство пользователя"
            self.help_button = QtWidgets.QPushButton("Руководство пользователя", self)
            self.help_button.setStyleSheet(
                "background-color: #4682B4; color: black; font-size: 20px; padding: 20px 20px;")
            self.help_button.clicked.connect(self.show_help)

            # Кнопка "Удалить модификации"
            self.remove_button = QtWidgets.QPushButton("Удалить модификации", self)
            self.remove_button.setStyleSheet(
                "background-color: #B22222; color: black; font-size: 20px; padding: 20px;")
            self.remove_button.clicked.connect(self.remove_modifications)

            # Добавление кнопок в макет
            button_layout.addWidget(self.install_button)
            button_layout.addWidget(self.help_button)
            button_layout.addWidget(self.remove_button)

            # Добавление макета кнопок в основной макет
            main_layout.addLayout(button_layout)

            # Прогресс-бар
            self.progress_bar = QtWidgets.QProgressBar(self)
            self.progress_bar.setValue(0)
            main_layout.addWidget(self.progress_bar)

            self.setLayout(main_layout)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при инициализации интерфейса: {str(e)}")

    def remove_modifications(self):
        """Удаление модификаций из папки игры."""
        try:
            # Путь к папке с модами
            mod_path = os.path.join(self.game_path.text(), "archive", "pc", "mod")

            # Проверка существования папки с модификациями
            if not os.path.exists(mod_path) or not os.listdir(mod_path):
                QMessageBox.information(self, "Удаление модификаций", "Модификации не найдены для удаления.")
                return

            # Подтверждение удаления
            reply = QMessageBox.question(
                self, "Подтверждение удаления",
                "Вы уверены, что хотите удалить все модификации?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:

                # Удаление только указанных модов
                mods_to_remove = [
                    "Dogtown_Subs_Switch_by_DreamVoice.archive",
                    "Radio_Shanson_by_Tokyo(optionally).archive",
                    "Rus_Dub_Base_by_DreamVoice.archive",
                    "Rus_Dub_DLC_by_DreamVoice.archive"
                ]

                removed_files = 0
                for file_name in mods_to_remove:
                    file_path = os.path.join(mod_path, file_name)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        removed_files += 1
                if removed_files == len(mods_to_remove):
                    QMessageBox.information(self, "Удаление завершено", "Все DREAMVOICE модификации успешно удалены.")
                else:
                    QMessageBox.warning(self, "Удаление завершено",
                                        f"Удалено {removed_files}/{len(mods_to_remove)} файлов. (все установленные от DREAMVOICE)")


        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении модификаций: {str(e)}")

    def perform_initial_checks(self):
        """ Проверка необходимых файлов и зависимостей. """
        missing_items = []

        # Проверяем шрифты
        font_path = "img/RobotoFlex[slnt,wdth,wght,opsz].ttf"
        if not os.path.exists(font_path):
            missing_items.append(f"Отсутствует шрифт: {font_path}")

        # Проверяем изображения
        logo_path = "img/logo.png"
        if not os.path.exists(logo_path):
            missing_items.append(f"Отсутствует логотип: {logo_path}")

        # Проверяем библиотеки
        try:
            import requests
        except ImportError:
            missing_items.append("Библиотека 'requests' не установлена.")

        # Выводим предупреждения
        if missing_items:
            QMessageBox.warning(self, "Проблемы при запуске", "\n".join(missing_items))

    def check_ep1_and_context(self):
        """ Проверка и установка файлов ep1 и context с Яндекс.Диска с динамическим прогрессом. """
        try:
            self.progress_bar.setValue(0)  # Сбрасываем прогресс
            self.progress_bar.setMaximum(100)

            # URL для Яндекс.Диска
            yandex_disk_url = "https://disk.yandex.ru/d/UUHYOh_VDI91ww"
            archive_name = "ep1_and_context.zip"
            target_dir = os.getcwd()
            archive_path = os.path.join(target_dir, archive_name)

            # 1. Получение прямой ссылки
            self.progress_bar.setValue(5)  # Прогресс на 5%
            response = requests.get(
                f"https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={yandex_disk_url}")
            if response.status_code == 200:
                download_url = response.json()["href"]
            else:
                raise Exception("Не удалось получить ссылку на скачивание с Яндекс.Диска")

            # 2. Скачивание архива
            print("Скачивание архива...")
            with requests.get(download_url, stream=True) as file_response:
                file_response.raise_for_status()
                total_length = int(file_response.headers.get("content-length", 0))  # Общий размер файла
                downloaded = 0  # Отслеживаем скаченные данные

                with open(archive_path, "wb") as archive_file:
                    for chunk in file_response.iter_content(chunk_size=8192):
                        archive_file.write(chunk)
                        downloaded += len(chunk)

                        if total_length > 0:  # Если известен размер файла
                            progress = int((downloaded / total_length) * 30)  # От 5% до 35% прогресса
                            self.progress_bar.setValue(5 + progress)
                        else:
                            # Если размер файла неизвестен, устанавливаем прогресс в зависимости от количества полученных данных
                            downloaded_mb = downloaded / (1024 ** 2)  # Считаем скачанные мегабайты
                            progress = min(30, int(downloaded_mb))  # Ограничиваем прогресс 30%
                            self.progress_bar.setValue(5 + progress)

            print("Архив успешно скачан.")

            # 3. Распаковка архива
            self.progress_bar.setValue(40)  # Устанавливаем прогресс на 40%
            print("Распаковка архива...")
            unpack_dir = os.path.join(target_dir, "unpacked_ep1_context")
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                files = zip_ref.namelist()
                total_files = len(files)
                for idx, file_name in enumerate(files, 1):
                    zip_ref.extract(file_name, unpack_dir)
                    # Обновляем прогресс распаковки от 40% до 70%
                    progress = int((idx / total_files) * 30)
                    self.progress_bar.setValue(40 + progress)

            print("Архив успешно распакован.")

            # 4. Копирование файлов
            self.progress_bar.setValue(70)  # Устанавливаем прогресс на 70%
            print("Копирование файлов...")
            game_archive_dir = os.path.join(self.game_path.text(), "archive", "pc", "content")
            game_ep1_dir = os.path.join(self.game_path.text(), "archive", "pc", "ep1")
            unpacked_content_dir = os.path.join(unpack_dir, "content")
            unpacked_ep1_dir = os.path.join(unpack_dir, "ep1")

            os.makedirs(game_archive_dir, exist_ok=True)
            os.makedirs(game_ep1_dir, exist_ok=True)

            # Копируем файлы в context
            context_files = ["lang_ru_text.archive", "lang_ru_voice.archive", "lang_en_text.archive",
                             "lang_en_voice.archive"]
            for idx, file_name in enumerate(context_files, 1):
                source_file = os.path.join(unpacked_content_dir, file_name)
                target_file = os.path.join(game_archive_dir, file_name)
                if not os.path.exists(target_file):
                    shutil.copy(source_file, target_file)

                # Обновляем прогресс копирования context от 70% до 85%
                progress = int((idx / len(context_files)) * 15)
                self.progress_bar.setValue(70 + progress)

            # Копируем файлы в ep1
            ep1_files = context_files + ["audio_1_general.archive"]
            for idx, file_name in enumerate(ep1_files, 1):
                source_file = os.path.join(unpacked_ep1_dir, file_name)
                target_file = os.path.join(game_ep1_dir, file_name)
                if not os.path.exists(target_file):
                    shutil.copy(source_file, target_file)

                # Обновляем прогресс копирования ep1 от 85% до 95%
                progress = int((idx / len(ep1_files)) * 10)
                self.progress_bar.setValue(85 + progress)

            # 5. Удаление временных файлов
            self.progress_bar.setValue(95)
            print("Удаление временных файлов...")
            os.remove(archive_path)
            shutil.rmtree(unpack_dir)
            self.progress_bar.setValue(100)
            print("Временные файлы успешно удалены.")

            QMessageBox.information(self, "Готово", "Файлы ep1 и context успешно установлены!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Ошибка: {e}")
        finally:
            self.progress_bar.setValue(0)  # Сброс прогресса после завершения

    def color_change(self,path_game):
        if path_game == "Игра не обнаружена. Укажите папку вручную.":
            return "color: #FF4C4C; font-size: 16px;"
        else:
            return "color: #CCCCCC; font-size: 16px;"

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
        """ Поиск пути к игре из нескольких источников: Steam, GOG, Epic Games и других. """
        try:
            # Попытка найти игру через Steam
            steam_path = self.find_game_in_steam()
            if steam_path:
                return steam_path

            # Попытка найти игру через GOG
            gog_path = self.find_game_in_gog()
            if gog_path:
                return gog_path

            # Попытка найти игру через Epic Games и другие лаунчеры
            other_path = self.find_game_in_other_launchers()
            if other_path:
                return other_path

            # Запрос ручного пути у пользователя
            folder = QFileDialog.getExistingDirectory(None, "Выберите папку с игрой Cyberpunk 2077")
            if folder:
                return folder

            return "Игра не обнаружена. Укажите папку вручную."
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Не удалось найти путь к игре: {str(e)}")
            return "Ошибка поиска пути."

    def find_game_in_steam(self):
        """ Поиск игры в реестре Steam и через libraryfolders.vdf. """
        try:
            # Открываем реестр для пути Steam
            steam_key_path = r"SOFTWARE\Valve\Steam"
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, steam_key_path)
            steam_install_path, _ = winreg.QueryValueEx(reg_key, "InstallPath")
            winreg.CloseKey(reg_key)

            # Читаем файл libraryfolders.vdf
            library_folders_path = os.path.join(steam_install_path, "steamapps", "libraryfolders.vdf")
            if not os.path.exists(library_folders_path):
                return None

            game_paths = []
            with open(library_folders_path, 'r') as f:
                for line in f:
                    if '"path"' in line:
                        lib_path = line.split('"')[3]
                        game_path = os.path.join(lib_path, "steamapps", "common", "Cyberpunk 2077")
                        if os.path.exists(game_path) and self.check_archive_exists(game_path):
                            game_paths.append(game_path)

            # Проверка стандартного пути
            default_game_path = os.path.join(steam_install_path, "steamapps", "common", "Cyberpunk 2077")
            if os.path.exists(default_game_path) and self.check_archive_exists(default_game_path):
                game_paths.append(default_game_path)

            if game_paths:
                return game_paths[0]  # Возвращаем первый найденный путь

            return "Игра не найдена в Steam."
        except Exception as e:
            print(f"Ошибка поиска Steam: {e}")


    def find_game_in_gog(self):
        """ Поиск игры через реестр GOG. """
        try:
            gog_key_path = r"SOFTWARE\WOW6432Node\GOG.com\Games\1423049311"
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, gog_key_path)
            game_path, _ = winreg.QueryValueEx(reg_key, "PATH")
            winreg.CloseKey(reg_key)

            if os.path.exists(game_path) and self.check_archive_exists(game_path):
                return game_path
            return None
        except Exception as e:
            print(f"Ошибка поиска GOG: {e}")
            return None

    def find_game_in_other_launchers(self):
        """ Поиск игры в других лаунчерах (Epic Games, стандартные пути). """
        try:
            # Проверяем путь Epic Games через стандартный путь
            epic_games_path = r"C:\Program Files\Epic Games\Cyberpunk 2077"
            if os.path.exists(epic_games_path) and self.check_archive_exists(epic_games_path):
                return epic_games_path

            # Дополнительная проверка через реестр Epic Games
            epic_key_path = r"SOFTWARE\Epic Games\EpicGamesLauncher"
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, epic_key_path)
            install_path, _ = winreg.QueryValueEx(reg_key, "AppDataPath")
            winreg.CloseKey(reg_key)

            # Проверяем возможный путь Cyberpunk 2077
            possible_epic_path = os.path.join(install_path, "Cyberpunk 2077")
            if os.path.exists(possible_epic_path) and self.check_archive_exists(possible_epic_path):
                return possible_epic_path

            # Альтернативные пути
            possible_paths = [
                r"C:\Games\Cyberpunk 2077",
                r"D:\Games\Cyberpunk 2077",
                r"E:\Games\Cyberpunk 2077"
            ]

            for path in possible_paths:
                if os.path.exists(path) and self.check_archive_exists(path):
                    return path

            return None
        except Exception as e:
            print(f"Ошибка поиска Epic Games: {e}")
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
                self.game_path.setStyleSheet(self.color_change(self.game_path.text()))

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
                    return

            self.thread = Thread(target=self.install_mods)
            self.thread.start()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при запуске установки: {str(e)}")

    def show_help(self):

        file_path = os.path.join(os.getcwd(), 'README.html')

        file_url = 'file://' + file_path

        webbrowser.open(file_url)

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

                # Создаём окно с выбором действия
            reply = QMessageBox.question(
                    self,
                    "Установка завершена",
                    "Все моды успешно установлены! Что вы хотите сделать дальше? Выбор: \n OK:НИЧЕГО \n OPEN: Открыть папку с модами \n Yes: Запустить игру",
                    QMessageBox.Ok | QMessageBox.Open | QMessageBox.Yes
                )

            # Проверяем условие
            if reply == QMessageBox.Open:
                # Формируем путь к папке с модами
                mod_path = os.path.join(self.game_path.text(), "archive", "pc", "mod")

                # Проверяем существует ли путь
                if os.path.exists(mod_path):
                    try:
                        # Используем subprocess для открытия папки
                        subprocess.Popen(f'explorer "{mod_path}"')
                    except Exception as e:
                        QMessageBox.critical(self, "Ошибка", f"Не удалось открыть папку: {e}")

            elif reply == QMessageBox.Yes:
                    # Запускаем игру
                    game_exe = os.path.join(self.game_path.text(), "bin", "x64", "Cyberpunk2077.exe")
                    if os.path.exists(game_exe):
                        os.startfile(game_exe)
                    else:
                        QMessageBox.critical(self, "Ошибка запуска", "Не удалось найти исполняемый файл игры!")
            self.progress_bar.setValue(0)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при установке модов: {str(e)}")


def main():
    try:
        app = QtWidgets.QApplication(sys.argv)

        app.setStyle("Fusion")
        dark_palette = QtGui.QPalette()
        dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#1C1C1C"))
        dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("#CCCCCC"))
        dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor("#CCCCCC"))
        dark_palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor("#CCCCCC"))
        dark_palette.setColor(QtGui.QPalette.Text, QtGui.QColor("#CCCCCC"))
        dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor("#CCCCCC"))
        dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
        dark_palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor("#1C1C1C"))
        app.setPalette(dark_palette)



        app.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont("img/RobotoFlex[slnt,wdth,wght,opsz].ttf"))[0]))

        window = InstallerApp()
        window.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(f"Ошибка запуска приложения: {str(e)}")


if __name__ == "__main__":
    main()
