# Функциональные возможности языка Python

Задание: https://github.com/ugapanyuk/BKIT_2022/wiki/lab_python_fp

Запуск из этой папки в PowerShell после подготовки .venv в корне:

```powershell
../.venv/Scripts/python.exe -m pip install -r requirements.txt
../.venv/Scripts/python.exe main.py
../.venv/Scripts/python.exe -m unittest discover -s tests -v
```

Все семь задач находятся в lab_python_fp. Каждый файл можно запускать отдельно.

```powershell
../.venv/Scripts/python.exe main.py data_demo.json
../.venv/Scripts/python.exe main.py data_light.json
```

Исходные данные: [data_light.json из курса](https://github.com/ugapanyuk/BKIT_2021/blob/main/notebooks/fp/files/data_light.json). Файл загружен без изменений, содержит 4635 записей.

При обычном запуске main.py (в том числе кнопкой ▶ в VS Code) открывается ручной ввод. Выбирайте пункт меню и вводите свои значения в панели Терминал. Можно выполнить несколько проверок подряд. Для выхода введите 0; в диалоге ЛР6 также доступна /exit. Режим --demo показывает готовый пример без ручного ввода.

Отчет: [исходник Markdown](report/report.md), [PDF](report/report.pdf).
