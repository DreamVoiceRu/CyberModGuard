 """ Показать инструкцию по установке. """
        dialog = QDialog(self)
        dialog.setWindowTitle("Инструкция")
        dialog.resize(1200, 800)  # Устанавливаем размер окна
        instruction = """
        <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Инструкция по установке Rus_Dub_by_DreamVoice_v5.0</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1e1e1e;
            color: #e0e0e0;
            margin: 20px;
            line-height: 1.6;
        }
        h1, h2, h3 {
            color: #00bcd4; /* Cyberpunk blue */
            border-bottom: 2px solid #00bcd4;
            padding-bottom: 5px;
        }
        a {
            color: #ff4081; /* Cyberpunk pink */
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        img {
            max-width: 100%;
            height: auto;
            border: 2px solid #00bcd4;
            border-radius: 5px;
        }
        .highlight {
            background-color: #292929;
            border-left: 5px solid #00bcd4;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .thanks {
            border: 1px solid #444;
            padding: 10px;
            background-color: #292929;
            font-size: 1.1em;
            margin: 20px 0;
            border-radius: 5px;
        }
        .mod-info {
            border-top: 1px solid #444;
            margin-top: 20px;
            padding-top: 10px;
        }
        .mod-info h3 {
            color: #00bcd4;
            border-bottom: 1px solid #00bcd4;
            padding-bottom: 5px;
        }
        .mod-info p {
            margin: 5px 0;
        }
        code {
            background-color: #333;
            color: #ff4081;
            padding: 2px 4px;
            border-radius: 3px;
        }
        ol li {
            margin-bottom: 10px;
        }
        .bug-report {
            background-color: #292929;
            border: 2px solid #ff4081;
            padding: 10px;
            margin: 20px 0;
            border-radius: 5px;
        }
    </style>
</head>
<body>

    <h1>Инструкция по установке Rus_Dub_by_DreamVoice_v5.0</h1>

    <p><strong>Только для версии 2.13</strong></p>

    <p>Убедитесь, что в папках <code>Cyberpunk 2077\archive\pc\content</code> и <code>Cyberpunk 2077\archive\pc\ep1</code> присутствуют следующие файлы:</p>

    <ul>
        <li><code>lang_ru_text.archive</code></li>
        <li><code>lang_ru_voice.archive</code></li>
        <li><code>lang_en_text.archive</code></li>
        <li><code>lang_en_voice.archive</code></li>
    </ul>

    <div>
    <img src="img/Наличие%20файлов%20в%20content.png" alt="Наличие файлов в content">
    <img src="img/Наличие%20файлов%20в%20ep1.png" alt="Наличие файлов в ep1">
    </div>

    <div class="thanks">
        ❣ <strong>Благодарим вас за установку нашей озвучки для дополнения "Призрачная свобода"!</strong> ❣<br>
        Мы старались создать максимально качественный продукт, чтобы ваше погружение стало ещё более захватывающим!<br><br>
        <strong>Не забывайте</strong>, что мы всегда рады вашим отзывам и предложениям! Присоединяйтесь к нашему сообществу в Telegram, чтобы быть в курсе последних новостей и обновлений:<br>
        <a href="https://t.me/DreamVoiceRu">DreamVoice Telegram: https://t.me/DreamVoiceRu</a><br><br>
        Желаем вам приятной игры и незабываемых приключений!<br>
        С любовью, команда <strong>DreamVoice</strong>.
    </div>

    <div class="mod-info">
        <h2>Дополнительная информация</h2>

        <p><strong>Только для версии 2.13</strong></p>

        <h3>Rus_Dub_Base_by_DreamVoice</h3>
        <p>Мод представляет собой пакет озвучки, который включает не озвученные реплики из основной части игры, изменённые разработчиками.</p>

        <h3>Rus_Dub_DLC_by_DreamVoice</h3>
        <p>Мод включает озвучку для <strong>DLC Cyberpunk 2077: Phantom Liberty</strong>.</p>

        <h3>Dogtown_Subs_Switch_by_DreamVoice</h3>
        <p>Мод включает субтитры для <strong>DLC</strong> и основной игры (дополнительные реплики) <strong>Cyberpunk 2077: Phantom Liberty</strong>.</p>

        <h3>#Racing_ru_voice_fix</h3>
        <p><strong>Автор: Иван И.</strong><br>
        Мод улучшает атмосферу уличных гонок, делая диалоги более живыми и соответствующими событиям. Этот мод встроен в архивы и активируется автоматически при установке.</p>
        <p><strong>Описание мода:</strong><br>
        Мод обновляет озвучку для определённых сцен, изменяя диалоги, произносимые во время гонок, чтобы они были более выразительными и подходили контексту.</p>

        <h3>#Radio_hosts_fix</h3>
        <p><strong>Автор: Иван И.</strong><br>
        Мод оптимизирует радиоэфир, делая его более естественным и приятным для восприятия. Этот мод встроен в архивы и активируется автоматически при установке.</p>
        <p><strong>Описание мода:</strong><br>
        Мод улучшает взаимодействие с диалогами радиоведущих, изменяя задержки диалогов для более плавного восприятия радиоэфира.</p>

        <h3>Radio_Shanson_by_Tokyo (Опциональный мод)</h3>
        <p><strong>Автор: Токио</strong><br>
        Мод заменяет радио <strong>91.9 Блюз-Рояль</strong> на радио <strong>Шансон</strong>, добавляя в игровой процесс русскую музыкальную атмосферу.</p>
    </div>

</body>
</html>

        """

        # Создаем текстовое поле для инструкции
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)  # Запрет редактирования текста
        text_edit.setHtml(instruction)  # Устанавливаем HTML-инструкцию

        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(dialog.accept)

        # Макет диалогового окна
        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        layout.addWidget(close_button)
        dialog.setLayout(layout)

        # Показываем диалоговое окно
        dialog.exec_()