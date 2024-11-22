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
                for file_name in mods_to_remove:
                    file_path = os.path.join(mod_path, file_name)
                    if os.path.exists(file_path):  # Проверяем, существует ли файл перед удалением
                        try:
                            os.remove(file_path)
                            print(f"Файл {file_name} успешно удалён.")
                        except Exception as e:
                            print(f"Ошибка при удалении {file_name}: {e}")
                QMessageBox.information(self, "Удаление завершено", "Выбранные модификации успешно удалены.")


        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении модификаций: {str(e)}")

    def check_ep1_and_context(self):
        """ Проверка и установка файлов ep1 и context с Яндекс.Диска. """
        try:
            # Сохранение текущего значения прогресс-бара
            previous_max = self.progress_bar.maximum()
            self.progress_bar.setValue(0)

            # Установка новых значений прогресс-бара
            self.progress_bar.setMaximum(100)
            step = 20

            # URL для скачивания
            yandex_disk_url = "https://disk.yandex.ru/d/UUHYOh_VDI91ww"
            archive_name = "ep1_and_context.zip"
            target_dir = os.getcwd()
            archive_path = os.path.join(target_dir, archive_name)

            # Шаг 1. Скачивание архива
            self.progress_bar.setValue(10)
            try:
                print("Скачивание архива с Яндекс.Диска...")
                response = requests.get(yandex_disk_url, stream=True)
                response.raise_for_status()
                with open(archive_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print("Архив успешно скачан.")
            except Exception as e:
                raise Exception(f"Ошибка при скачивании архива: {e}")

            # Шаг 2. Распаковка архива
            self.progress_bar.setValue(30)
            unpack_dir = os.path.join(target_dir, "unpacked_ep1_context")
            try:
                print("Распаковка архива...")
                with zipfile.ZipFile(archive_path, "r") as zip_ref:
                    zip_ref.extractall(unpack_dir)
                print("Архив успешно распакован.")
            except Exception as e:
                raise Exception(f"Ошибка при распаковке архива: {e}")

            # Шаг 3. Подготовка путей для копирования
            self.progress_bar.setValue(50)
            game_archive_dir = os.path.join(self.game_path.text(), "archive", "pc", "content")
            game_ep1_dir = os.path.join(self.game_path.text(), "archive", "pc", "ep1")
            unpacked_content_dir = os.path.join(unpack_dir, "content")
            unpacked_ep1_dir = os.path.join(unpack_dir, "ep1")

            os.makedirs(game_archive_dir, exist_ok=True)
            os.makedirs(game_ep1_dir, exist_ok=True)

            # Файлы для проверки
            context_files = [
                "lang_ru_text.archive",
                "lang_ru_voice.archive",
                "lang_en_text.archive",
                "lang_en_voice.archive",
            ]
            ep1_files = [
                "lang_ru_text.archive",
                "lang_ru_voice.archive",
                "lang_en_text.archive",
                "lang_en_voice.archive",
                "audio_1_general.archive",
            ]

            # Шаг 4. Проверка и копирование файлов
            self.progress_bar.setValue(70)
            for file_name in context_files:
                source_file = os.path.join(unpacked_content_dir, file_name)
                target_file = os.path.join(game_archive_dir, file_name)
                if not os.path.exists(target_file):
                    print(f"Копирование отсутствующего файла: {file_name}")
                    shutil.copy(source_file, target_file)

            for file_name in ep1_files:
                source_file = os.path.join(unpacked_ep1_dir, file_name)
                target_file = os.path.join(game_ep1_dir, file_name)
                if not os.path.exists(target_file):
                    print(f"Копирование отсутствующего файла: {file_name}")
                    shutil.copy(source_file, target_file)

            # Шаг 5. Удаление временных файлов
            self.progress_bar.setValue(90)
            try:
                print("Удаление временных файлов...")
                os.remove(archive_path)
                shutil.rmtree(unpack_dir)
                print("Временные файлы успешно удалены.")
            except Exception as e:
                print(f"Ошибка при удалении временных файлов: {e}")

            # Завершение процесса
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "Готово", "Файлы ep1 и context успешно установлены!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Ошибка: {e}")
        finally:
            # Сброс прогресс-бара к исходным значениям
            self.progress_bar.setValue(0)
            self.progress_bar.setMaximum(previous_max)

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
            # Попробуем найти путь к Steam
            steam_key_path = r"SOFTWARE\Valve\Steam"
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, steam_key_path)
            steam_install_path, _ = winreg.QueryValueEx(reg_key, "InstallPath")
            winreg.CloseKey(reg_key)

            # Путь к файлу libraryfolders.vdf
            library_folders_path = os.path.join(steam_install_path, "steamapps", "libraryfolders.vdf")
            if not os.path.exists(library_folders_path):
                return None

            # Читаем libraryfolders.vdf и ищем ID игры 1091500
            with open(library_folders_path, 'r') as f:
                content = f.read()

            for line in content.splitlines():
                if '"path"' in line:
                    # Извлекаем путь библиотеки Steam
                    lib_path = line.split('"')[3]
                    game_path = os.path.join(lib_path, "steamapps", "common", "Cyberpunk 2077")
                    if os.path.exists(game_path) and self.check_archive_exists(game_path):
                        return game_path

            # Проверка стандартного пути Steam
            default_game_path = os.path.join(steam_install_path, "steamapps", "common", "Cyberpunk 2077")
            if os.path.exists(default_game_path) and self.check_archive_exists(default_game_path):
                return default_game_path

            return None
        except Exception as e:
            print(f"Ошибка поиска Steam: {e}")
            return None

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
            if self.game_path.text() != "Игра не обнаружена. Укажите папку вручную.":
                mod_path = os.path.join(self.game_path.text(), "archive", "pc", "mod")
                if not os.path.exists(mod_path):
                    os.makedirs(mod_path)
            else:
                QMessageBox.warning(self, "Ошибка", "У вас не выбрана папка с игрой")
                return


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

    def install_mods(self):
        if self.game_path.text() == "Игра не обнаружена. Укажите папку вручную.":
            QMessageBox.warning(self, "Ошибка", "У вас не выбрана папка с игрой")
        else:
            """ Установка модов с прогрессом и улучшенным завершением. """
            try:
                # Проверка наличия недостающих файлов в папках ep1 и content
                context_missing_files = [
                "lang_ru_text.archive",
                "lang_ru_voice.archive",
                "lang_en_text.archive",
                "lang_en_voice.archive"
                ]
                ep1_missing_files = [
                "lang_ru_text.archive",
                "lang_ru_voice.archive",
                "lang_en_text.archive",
                "lang_en_voice.archive",
                "audio_1_general.archive"
                ]

                context_path = os.path.join(self.game_path.text(), "archive", "pc", "content")
                ep1_path = os.path.join(self.game_path.text(), "archive", "pc", "ep1")

                missing_files = []

                # Проверяем папку context
                for file_name in context_missing_files:
                    if not os.path.exists(os.path.join(context_path, file_name)):
                        missing_files.append(f"content/{file_name}")

                # Проверяем папку ep1
                for file_name in ep1_missing_files:
                    if not os.path.exists(os.path.join(ep1_path, file_name)):
                        missing_files.append(f"ep1/{file_name}")

                if missing_files:
                    # Показать окно с уведомлением
                    missing_files_str = "\n".join(missing_files)
                    reply = QMessageBox.question(self, "Недостающие файлы",
                                             f"В папках ep1 и content отсутствуют следующие файлы:\n{missing_files_str}\n\n"
                                             "Предлагаем загрузить недостающие файлы (около 12.65 ГБ). Продолжить?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                    if reply == QMessageBox.No:
                        return

                    # Проверка свободного места на диске
                    free_space = psutil.disk_usage(os.path.abspath(os.getcwd())).free
                    required_space = 30 * 1024 ** 3  # 30 GB в байтах

                    if free_space < required_space:
                        QMessageBox.critical(self, "Недостаточно места",
                                         "На диске недостаточно свободного места (необходимо 30 ГБ).\n"
                                         "Переместите установщик на диск с достаточным количеством свободного места и повторите попытку.")
                        return

                    # Если место есть, вызываем функцию для скачивания и распаковки файлов
                    self.check_ep1_and_context()

                # Переходим к установке модов, если недостающих файлов нет
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

                self.progress_bar.setValue(0)

                # Создаём окно с выбором действия
                reply = QMessageBox.question(
                    self,
                    "Установка завершена",
                    "Все моды успешно установлены! Что вы хотите сделать дальше? Выбор: НИЧЕГО|Открыть папку с модами|Запустить игру",
                    QMessageBox.Ok | QMessageBox.Open | QMessageBox.Yes
                )

                if reply == QMessageBox.Open:
                    # Открываем папку с модами
                    mod_path = os.path.join(self.game_path.text(), "archive", "pc", "mod")
                    os.startfile(mod_path)

                elif reply == QMessageBox.Yes:
                    # Запускаем игру
                    game_exe = os.path.join(self.game_path.text(), "bin", "x64", "Cyberpunk2077.exe")
                    if os.path.exists(game_exe):
                        os.startfile(game_exe)
                    else:
                        QMessageBox.critical(self, "Ошибка запуска", "Не удалось найти исполняемый файл игры!")

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

        # Добавляем стиль для чекбоксов
        app.setStyleSheet("""
            QCheckBox {
                color: #CCCCCC;
                font-size: 14px;
            }

            QCheckBox::indicator {
                background-color: #7f9675;  /* Светло-серый фон */
                border: 1px solid #888888;  /* Темно-серая рамка */
                width: 20px;
                height: 20px;
                border-radius: 1px;  /* Скругленные углы */
            }

            QCheckBox::indicator:checked {
                background-color: #A9A9A9;  /* Темно-серый фон для отмеченного */
                border: 2px solid #888888;  /* Оставляем темную рамку */
            }

            QCheckBox::indicator:checked:hover {
                background-color: #7f9675;  /* Фон для отмеченного при наведении */
            }

            QCheckBox::indicator:unchecked:hover {
                background-color: #b6d7a8;  /* Фон для неотмеченного при наведении */
            }
        """)

        app.setFont(QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont("img/RobotoFlex[slnt,wdth,wght,opsz].ttf"))[0]))

        window = InstallerApp()
        window.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(f"Ошибка запуска приложения: {str(e)}")


if __name__ == "__main__":
    main()
