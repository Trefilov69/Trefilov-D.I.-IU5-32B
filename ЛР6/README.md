# Разработка Telegram бота на основе конечного автомата

Задание: https://github.com/ugapanyuk/BKIT_2021/wiki/lab_bot2

Запуск из этой папки в PowerShell после подготовки .venv в корне:

```powershell
../.venv/Scripts/python.exe -m pip install -r requirements.txt
../.venv/Scripts/python.exe main.py
../.venv/Scripts/python.exe -m unittest discover -s tests -v
```

Подключение к Telegram:

```powershell
$env:TELEGRAM_BOT_TOKEN = 'ваш_токен_от_BotFather'
../.venv/Scripts/python.exe main.py --telegram
```

Токен читается из окружения; .env не загружается автоматически. Локальная демонстрация и тесты работают без токена. Проверка подключения к Telegram API без токена не выполнялась.

Диалог в личных сообщениях: SHAPE → DIMENSIONS → CONFIRM → END. Заново возвращает к выбору фигуры; /cancel завершает разговор. Ошибки сохраняют текущее состояние. /start начинает новый расчет. END обозначает завершение, а не четвертое состояние. Данные хранятся в памяти до завершения разговора или перезапуска процесса.

При обычном запуске main.py (в том числе кнопкой ▶ в VS Code) открывается ручной ввод. Выбирайте пункт меню и вводите свои значения в панели Терминал. Можно выполнить несколько проверок подряд. Для выхода введите 0; в диалоге ЛР6 также доступна /exit. Режим --demo показывает готовый пример без ручного ввода.

Отчет: [исходник Markdown](report/report.md), [PDF](report/report.pdf).
