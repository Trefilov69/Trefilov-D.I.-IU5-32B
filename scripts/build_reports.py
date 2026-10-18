"""Сборка отчетов из исходников и фактических результатов запуска.

Запуск из корня: ./.venv/Scripts/python.exe scripts/build_reports.py
Зависимости и команды приведены в README.md.
"""
import os
from pathlib import Path
import re
import subprocess
import sys
import textwrap
from xml.sax.saxutils import escape

import pymupdf as fitz
from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Image,
)

ROOT = Path(__file__).resolve().parents[1]
COURSE = "https://github.com/ugapanyuk/courses_content/wiki/COURSE_PCPL_MAIN"
FONT_DIR = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
FP = "ЛР2_Функциональные_возможности_Python"
LABS = {
    "ЛР2": {
        "number": "2", "title": "Объектно ориентированные возможности языка Python",
        "source": "https://github.com/ugapanyuk/BKIT_2022/wiki/lab_python_oop",
        "goal": "Изучить классы, наследование, абстрактные методы, свойства и пакеты Python.",
        "task": "Реализовать пакет lab_python_oop с абстрактной геометрической фигурой, цветом, прямоугольником, кругом и квадратом. В main.py создать фигуры с параметром N = 5, вывести площади и вызвать внешний пакет colorama.",
        "logic": "GeometricFigure задает абстрактный метод square. Rectangle и Circle реализуют вычисление площади, Square наследует Rectangle. FigureColor хранит цвет в свойстве. Методы класса возвращают название фигуры, __repr__ формирует строку с параметрами. Существующий код и отчет Word сохранены.",
        "checks": "Три теста unittest проверяют площади прямоугольника 5 × 4, квадрата со стороной 5 и круга с радиусом 5. Для круга используется сравнение с допустимой погрешностью.",
        "conclusion": "Реализованы и проверены основные механизмы ООП и использование внешнего пакета colorama.",
        "demo": [["main.py", "--demo"]],
    },
    FP: {
        "number": "2", "title": "Функциональные возможности языка Python",
        "source": "https://github.com/ugapanyuk/BKIT_2022/wiki/lab_python_fp",
        "goal": "Изучить генераторы, итераторы, функции высшего порядка, декораторы и контекстные менеджеры.",
        "task": "Выполнить все семь задач в пакете lab_python_fp. Каждый файл должен запускать пример самостоятельно. Обработать исходный набор вакансий data_light.json с помощью цепочки f1, f2, f3 и f4.",
        "logic": "field.py выдает значения одного поля или словари выбранных полей, пропуская None. gen_random.py генерирует целые числа во включительном диапазоне. unique.py реализует ленивый итератор Unique с **kwargs и ignore_case, сохраняя исходный регистр первого элемента. sort.py показывает две сортировки по убыванию модуля. print_result.py печатает имя функции и скаляр, список или словарь, возвращая исходный результат. cm_timer.py содержит класс и вариант с contextlib; оба печатают время даже при исключении. process_data.py получает путь через командную строку: f1 сортирует уникальные названия профессий без учета регистра, f2 использует filter, f3 использует map, f4 соединяет профессии со случайными зарплатами через zip. Исходный набор содержит 4635 записей; небольшой data_demo.json предназначен для читаемой экранной формы.",
        "checks": "Семь тестов проверяют пропуск None и сохранение нулевых значений, выбор нескольких полей, границы генератора, Unique со списком и генератором, формат декоратора, распространение исключений таймерами и всю цепочку f1–f4. В тесте цепочки случайная зарплата подменяется Mock-объектом через patch. Дополнительно программа запускается на полном исходном наборе вакансий.",
        "conclusion": "Выполнены все семь задач, включая обработку реального набора вакансий. Генераторы и итератор работают лениво; функции цепочки принимают результаты предыдущих стадий.",
        "demo": [["lab_python_fp/field.py"], ["lab_python_fp/gen_random.py"],
                 ["lab_python_fp/unique.py"], ["lab_python_fp/sort.py"],
                 ["lab_python_fp/print_result.py"], ["lab_python_fp/cm_timer.py"],
                 ["main.py", "data_demo.json"]],
    },
    "ЛР3": {
        "number": "3", "title": "Модульное тестирование в Python",
        "source": "https://github.com/ugapanyuk/BKIT_2022/wiki/lab_python_test",
        "goal": "Изучить модульное и поведенческое тестирование, а также замену зависимостей Mock-объектами.",
        "task": "Выбрать фрагмент ЛР2, подготовить его к тестированию, написать не менее трех тестов в TDD-фреймворке и трех сценариев в BDD-фреймворке. Дополнительно применить Mock-объекты.",
        "logic": "Взят расчет площадей фигур из ЛР2. В самостоятельном пакете lab_python_test вычисления отделены от консоли. Размеры преобразуются в числа, нулевые, отрицательные и бесконечные значения отклоняются. print_area принимает зависимость output, что позволяет проверить вывод без обращения к терминалу. unittest используется как фреймворк модульного тестирования, behave выполняет русскоязычные сценарии Given When Then. Исходная ЛР2 остается самостоятельной.",
        "checks": "Пять тестов unittest проверяют три площади, некорректные размеры и вызов Mock-функции вывода. Три BDD-сценария проверяют площади прямоугольника, квадрата и круга с точки зрения наблюдаемого результата.",
        "conclusion": "Тесты подтверждают вычисления, обработку неверных размеров и консольное представление результата. BDD-сценарии описывают поведение на языке предметной области.",
        "demo": [["main.py", "--demo"]], "bdd": True,
    },
    "ЛР4": {
        "number": "4", "title": "Шаблоны проектирования и модульное тестирование в Python",
        "source": "https://github.com/ugapanyuk/BKIT_2021/wiki/lab_python_test",
        "goal": "Изучить порождающие, структурные и поведенческие шаблоны и проверить их совместную работу.",
        "task": "Для одной предметной области реализовать три шаблона: один порождающий, один структурный и один поведенческий. Проверить код с помощью TDD-фреймворка, BDD-фреймворка и Mock-объектов.",
        "logic": "Предметная область - заказ напитка в кафе. Порождающий Фабричный метод: Cafe определяет create_product и использующий его order_price; CoffeeCafe и TeaCafe создают конкретные продукты. Структурный Декоратор: Milk оборачивает Product, сохраняет интерфейс price и добавляет 30 рублей. Поведенческая Стратегия: Order делегирует расчет RegularPrice или StudentDiscount. Денежные значения хранятся в Decimal; студенческая скидка равна 10 процентам.",
        "checks": "Семь тестов unittest проверяют фабрики, цену чая, декоратор и его вложение, обычную цену и скидку. Mock-объекты подменяют стратегию и продукт, проверяя аргументы и число вызовов. Три сценария behave проверяют кофе за 150 рублей, кофе с молоком за 180 рублей и заказ со скидкой за 162 рубля.",
        "conclusion": "Все три категории шаблонов представлены в единой модели заказа. Модульные проверки и BDD-сценарии подтверждают расчет стоимости и взаимодействие зависимостей.",
        "demo": [["main.py", "--demo"]], "bdd": True,
    },
    "ЛР5": {
        "number": "5", "title": "Разработка простого бота для Telegram",
        "source": "https://github.com/ugapanyuk/BKIT_2021/wiki/lab_bot1",
        "goal": "Освоить команды Telegram-бота, inline-кнопки и обработку callback-запросов.",
        "task": "Разработать простого Telegram-бота с функциональностью создания кнопок. Предметная область - справочник площадей геометрических фигур.",
        "logic": "Команда /start выводит InlineKeyboardMarkup с кнопками Квадрат, Прямоугольник и Круг. Нажатие отправляет callback_data. choose_figure подтверждает callback вызовом answer и редактирует сообщение, показывая формулу и пример. Клавиатура сохраняется для повторного выбора. /help выводит инструкцию. Токен читается из TELEGRAM_BOT_TOKEN; при его отсутствии программа завершает запуск с понятным сообщением.",
        "checks": "Четыре асинхронных теста проверяют кнопки /start, все три формулы, неизвестный callback и регистрацию обработчиков. AsyncMock подменяет ответы Telegram API. main.py --demo вызывает настоящие обработчики с локальным выводом. Доступ к Telegram API и реальный диалог в Telegram не проверялись: токен пользователя не предоставлен. Экранная форма ниже показывает локальную демонстрацию, а не интерфейс Telegram.",
        "conclusion": "Бот реализует команды и inline-кнопки; локальные тесты подтверждают ответы обработчиков. Для проверки в Telegram необходимо задать личный токен и запустить polling.",
        "demo": [["main.py", "--demo"]], "telegram": True,
    },
    "ЛР6": {
        "number": "6", "title": "Разработка Telegram бота на основе конечного автомата",
        "source": "https://github.com/ugapanyuk/BKIT_2021/wiki/lab_bot2",
        "goal": "Реализовать диалог Telegram-бота как конечный автомат из трех состояний.",
        "task": "Разработать бота для вычисления площади. Организовать выбор фигуры, ввод размеров и подтверждение как три состояния диалога.",
        "logic": "ConversationHandler содержит ровно три состояния: SHAPE = 0, DIMENSIONS = 1 и CONFIRM = 2. /start открывает SHAPE. Корректный выбор фигуры переводит в DIMENSIONS. Корректные размеры переводят в CONFIRM. Да выводит площадь и завершает разговор через END; Заново возвращает в SHAPE. Ошибки сохраняют текущее состояние. /cancel завершает разговор на любой стадии, /start позволяет начать заново. END - служебный маркер завершения библиотеки, а не четвертое состояние states. Бот работает в личных сообщениях; concurrent_updates(False) обеспечивает последовательную обработку. Данные отдельного пользователя находятся в context.user_data и очищаются при завершении. Размеры принимаются с десятичной точкой или запятой, для прямоугольника - через пробел.",
        "checks": "Восемь тестов проверяют расчет трех фигур, неверные значения, полный диалог, сохранение состояния при ошибке, повторный расчет, отмену, разделение контекстов пользователей и ровно три состояния в ConversationHandler. Асинхронные ответы подменены AsyncMock. main.py --demo проходит реальный код обработчиков, включая ошибочный ввод. Доступ к Telegram API и реальный диалог в Telegram не проверялись без личного токена. После перезапуска процесса незавершенные диалоги сбрасываются.",
        "conclusion": "Реализован автомат с тремя состояниями, проверкой ввода, повторным расчетом и отменой. Локальный диалог и тесты подтверждают переходы обработчиков; для проверки в Telegram требуется токен BotFather.",
        "demo": [["main.py", "--demo"]], "telegram": True,
    },
}


MANUAL_INPUTS = {
    "ЛР2": "1\n6\n7\nкрасный\n0\n",
    FP: "4\n-7 2 -3\n0\n",
    "ЛР3": "2\n7\n0\n",
    "ЛР4": "2\n2\nда\n0\n",
    "ЛР5": "2\n6 7\n0\n",
    "ЛР6": "2\n6 7\n1\n0\n",
}


def run(folder, args, input_data=None):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    result = subprocess.run([sys.executable, *args], cwd=ROOT / folder, env=env,
                            text=True, encoding="utf-8", stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=120, input=input_data)
    if result.returncode:
        raise RuntimeError(f"{folder}: {args}\n{result.stdout}")
    return result.stdout


def screenshot(text, path):
    font = ImageFont.truetype(str(FONT_DIR / "consola.ttf"), 19)
    lines = []
    for line in text.splitlines():
        lines.extend(textwrap.wrap(line, width=96, replace_whitespace=False,
                                   drop_whitespace=False) or [""])
    # Экранная форма - ограниченная область терминала; полный текст рядом в .txt.
    if len(lines) > 44:
        lines = lines[:42] + ["...", "Полный вывод сохранен в текстовом файле рядом с отчетом."]
    image = PILImage.new("RGB", (1160, max(150, len(lines) * 26 + 50)), "#10151c")
    draw = ImageDraw.Draw(image)
    for index, line in enumerate(lines):
        draw.text((24, 24 + 26 * index), line, font=font, fill="#edf1f5")
    image.save(path)


def source_files(folder):
    files = []
    for pattern in ("*.py", "**/*.py", "**/*.feature", "requirements.txt"):
        for path in (ROOT / folder).glob(pattern):
            if "__pycache__" not in path.parts and path not in files:
                if path.name == "__init__.py":
                    continue
                files.append(path)
    return sorted(files, key=lambda path: ("tests" in path.parts or "features" in path.parts,
                                          str(path.relative_to(ROOT / folder))))


def make_markdown(folder, spec, demo, tests, bdd, demo_images):
    lines = ["Министерство науки и высшего образования Российской Федерации",
             "Московский государственный технический университет имени Н Э Баумана",
             "Факультет Информатика и системы управления",
             "Кафедра Системы обработки информации и управления", "",
             f"# Лабораторная работа {spec['number']}", f"## {spec['title']}", "",
             "Дисциплина: Парадигмы и конструкции языков программирования",
             "Выполнил: студент группы ИУ5-32Б Трефилов Д.И.", "Москва 2026", "",
             "## 1 Цель работы", spec["goal"], "", "## 2 Постановка задачи", spec["task"], "",
             f"Источник задания: {spec['source']}", f"Список курса: {COURSE}", "",
             "## 3 Структура и логика программы", spec["logic"], "",
             "## 4 Порядок запуска", "Команды выполняются из папки работы в подготовленном окружении.",
             "```powershell", "python -m pip install -r requirements.txt",
             "python main.py",
             "python -m unittest discover -s tests -v"]
    if spec.get("bdd"):
        lines.append("python -m behave")
    lines += ["```", ""]
    if spec.get("telegram"):
        lines += ["Запуск с подключением к Telegram в PowerShell:", "```powershell",
                  "$env:TELEGRAM_BOT_TOKEN = 'ваш_токен'", "python main.py --telegram", "```",
                  "Файл .env автоматически не загружается. Токен в отчет и Git не добавляется.", ""]
    if folder == FP:
        lines += ["Полный исходный набор: data_light.json, 4635 записей, 14232722 байт.",
                  "Источник данных: https://github.com/ugapanyuk/BKIT_2021/blob/main/notebooks/fp/files/data_light.json",
                  "Для полного набора: python main.py data_light.json. Для короткого примера: python main.py data_demo.json.", ""]
    lines += ["## 5 Проверка программы", spec["checks"], "", "### Пример выполнения",
              "```text", demo.rstrip(), "```", ""]
    for title, filename in demo_images:
        lines += [f"### {title}", f"![Экранная форма консольного вывода]({filename})", ""]
    lines += ["### Модульные тесты", "```text", tests.rstrip(), "```", "",
              "![Экранная форма тестирования](tests.png)", ""]
    if bdd:
        lines += ["### BDD сценарии", "```text", bdd.rstrip(), "```", ""]
    lines += ["## 6 Выводы", spec["conclusion"], "", "## Приложение Листинги программ", ""]
    for path in source_files(folder):
        relative = path.relative_to(ROOT / folder).as_posix()
        raw = path.read_bytes()
        source = raw.decode("utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")
        lines += [f"### {relative}", "```" + ("python" if path.suffix == ".py" else "text"),
                  source.rstrip(), "```", ""]
    return "\n".join(lines)


def setup_fonts():
    for name, file in (("Body", "times.ttf"), ("BodyBold", "timesbd.ttf"),
                       ("Code", "consola.ttf")):
        pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / file)))
    pdfmetrics.registerFontFamily("Body", normal="Body", bold="BodyBold")


def pdf_report(folder, spec, markdown):
    report_dir = ROOT / folder / "report"
    styles = getSampleStyleSheet()
    body = ParagraphStyle("ReportBody", fontName="Body", fontSize=12, leading=16,
                          spaceAfter=7)
    heading = ParagraphStyle("ReportHeading", parent=body, fontName="BodyBold",
                             fontSize=14, leading=18, spaceBefore=12,
                             keepWithNext=True)
    small_heading = ParagraphStyle("ReportSubheading", parent=heading, fontSize=11,
                                   leading=14)
    center = ParagraphStyle("ReportCenter", parent=body, alignment=TA_CENTER)
    cover_title = ParagraphStyle("CoverTitle", parent=center, fontName="BodyBold",
                                 fontSize=17, leading=23)
    code_style = ParagraphStyle("Source", fontName="Code", fontSize=8.2, leading=10.5,
                               spaceAfter=6)
    story = []
    for text in ("Министерство науки и высшего образования Российской Федерации",
                 "Московский государственный технический университет имени Н Э Баумана",
                 "Факультет Информатика и системы управления",
                 "Кафедра Системы обработки информации и управления"):
        story.append(Paragraph(text, center))
    story.append(Spacer(1, 35 * mm))
    story.append(Paragraph(f"Лабораторная работа {spec['number']}", cover_title))
    story.append(Paragraph(spec["title"], cover_title))
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("Дисциплина Парадигмы и конструкции языков программирования", center))
    story.append(Spacer(1, 28 * mm))
    story.append(Paragraph("Выполнил: студент группы ИУ5-32Б", body))
    story.append(Paragraph("Трефилов Д.И.", body))
    story.append(Paragraph("Проверил: ____________________", body))
    story.append(Paragraph("Дата защиты: ____________________", body))
    story.append(Spacer(1, 23 * mm))
    story.append(Paragraph("Москва 2026", center))
    story.append(PageBreak())
    content = markdown[markdown.index("## 1 Цель работы"):].splitlines()
    in_code = False
    code_lines = []

    def add_code():
        # Мягкий перенос в PDF не меняет исходный листинг в Markdown.
        wrapped = []
        for line in code_lines:
            wrapped.extend(textwrap.wrap(line.expandtabs(4), width=97,
                                          replace_whitespace=False,
                                          drop_whitespace=False) or [""])
        story.append(Preformatted("\n".join(wrapped), code_style))

    for line in content:
        if line.startswith("```"):
            if in_code:
                add_code()
                code_lines = []
            in_code = not in_code
        elif in_code:
            code_lines.append(line)
        elif line.startswith("!["):
            filename = re.search(r"\]\(([^)]+)\)", line).group(1)
            image_path = report_dir / filename
            with PILImage.open(image_path) as im:
                width, height = im.size
            scale = min(165 * mm / width, 180 * mm / height)
            story.append(Image(str(image_path), width=width * scale, height=height * scale))
            story.append(Spacer(1, 4 * mm))
        elif line.startswith("## "):
            story.append(Paragraph(escape(line[3:]), heading))
        elif line.startswith("### "):
            story.append(Paragraph(escape(line[4:]), small_heading))
        elif line:
            # URL переносится на несколько строк, чтобы не выходить за поля.
            text = escape(line)
            for url in re.findall(r"https?://\S+", line):
                display = escape(url).replace("/", "/<wbr/>").replace("_", "_<wbr/>")
                text = text.replace(escape(url), display)
            story.append(Paragraph(text, body))

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont("Body", 9)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, str(document.page))
        canvas.restoreState()

    output = report_dir / "report.pdf"
    document = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=20 * mm,
                                 leftMargin=25 * mm, topMargin=20 * mm,
                                 bottomMargin=20 * mm, title=spec["title"],
                                 author="Трефилов Д.И.")
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    return output


def render_qa(pdf, folder):
    target = ROOT / "tmp" / "pdf_qa" / folder
    target.mkdir(parents=True, exist_ok=True)
    thumbs = []
    with fitz.open(pdf) as document:
        for number, page in enumerate(document, 1):
            page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2)).save(target / f"page-{number}.png")
            image = PILImage.open(target / f"page-{number}.png").convert("RGB")
            image.thumbnail((330, 470))
            thumb = PILImage.new("RGB", (350, 500), "#d9dde2")
            thumb.paste(image, ((350 - image.width) // 2, 10))
            draw = ImageDraw.Draw(thumb)
            draw.text((12, 480), f"page {number}", fill="black")
            thumbs.append(thumb)
        # Проверка геометрии текста выявляет выход за границы страницы.
        for number, page in enumerate(document, 1):
            for block in page.get_text("blocks"):
                if block[0] < 0 or block[1] < 0 or block[2] > page.rect.width + 1 or block[3] > page.rect.height + 1:
                    raise RuntimeError(f"Text outside page: {folder}, {number}")
    for start in range(0, len(thumbs), 12):
        batch = thumbs[start:start + 12]
        rows = (len(batch) + 2) // 3
        sheet = PILImage.new("RGB", (1050, rows * 500), "white")
        for index, thumb in enumerate(batch):
            sheet.paste(thumb, ((index % 3) * 350, (index // 3) * 500))
        sheet.save(target / f"contact-{start // 12 + 1}.png")
    return len(thumbs)


def main():
    setup_fonts()
    for folder, spec in LABS.items():
        report_dir = ROOT / folder / "report"
        report_dir.mkdir(exist_ok=True)
        demo = ""
        demo_images = []
        for index, arguments in enumerate(spec["demo"], 1):
            chunk = "$ python " + " ".join(arguments) + "\n" + run(folder, arguments) + "\n"
            demo += chunk
            if folder == FP:
                filename = f"task-{index}.png"
                screenshot(chunk, report_dir / filename)
                demo_images.append((f"Задача {index} {Path(arguments[0]).stem}", filename))
        manual = ("$ python main.py\nВвод по строкам: " +
                  " | ".join(MANUAL_INPUTS[folder].rstrip().splitlines()) + "\n" +
                  run(folder, ["main.py"], MANUAL_INPUTS[folder]))
        screenshot(manual, report_dir / "manual.png")
        tests = run(folder, ["-m", "unittest", "discover", "-s", "tests", "-v"])
        # asyncio в debug-режиме может включать абсолютные пути в slow-callback diagnostic.
        tests = "\n".join(line for line in tests.splitlines() if not line.startswith("Executing <Task")) + "\n"
        tests = re.sub(r" \.\.\. Executing <Task[^\n]*", " ...", tests)
        bdd = run(folder, ["-m", "behave", "--no-capture"]) if spec.get("bdd") else ""
        if folder == FP:
            full_output = run(folder, ["main.py", "data_light.json"])
            (report_dir / "full_data_output.txt").write_text(
                "\n".join(line.rstrip() for line in full_output.splitlines()).rstrip() + "\n", encoding="utf-8")
        (report_dir / "demo_output.txt").write_text(demo.rstrip() + "\n", encoding="utf-8")
        (report_dir / "test_results.txt").write_text(tests + bdd, encoding="utf-8")
        screenshot(demo, report_dir / "demo.png")
        if not demo_images:
            demo_images = [("Экранная форма выполнения", "demo.png")]
        demo_images.append(("Ручная проверка со своими значениями", "manual.png"))
        screenshot(tests, report_dir / "tests.png")
        markdown = make_markdown(folder, spec, demo, tests, bdd, demo_images)
        (report_dir / "report.md").write_text(markdown, encoding="utf-8")
        pdf = pdf_report(folder, spec, markdown)
        pages = render_qa(pdf, folder)
        # Короткая инструкция в каждой папке, с общим окружением из корня.
        readme = (f"# {spec['title']}\n\nЗадание: {spec['source']}\n\n"
                  "Запуск из этой папки в PowerShell после подготовки .venv в корне:\n\n"
                  "```powershell\n../.venv/Scripts/python.exe -m pip install -r requirements.txt\n"
                  "../.venv/Scripts/python.exe main.py" +
                  "\n../.venv/Scripts/python.exe -m unittest discover -s tests -v\n" +
                  ("../.venv/Scripts/python.exe -m behave\n" if spec.get("bdd") else "") + "```\n\n")
        if spec.get("telegram"):
            readme += ("Подключение к Telegram:\n\n```powershell\n"
                       "$env:TELEGRAM_BOT_TOKEN = 'ваш_токен_от_BotFather'\n"
                       "../.venv/Scripts/python.exe main.py --telegram\n```\n\n"
                       "Токен читается из окружения; .env не загружается автоматически. "
                       "Локальная демонстрация и тесты работают без токена. "
                       "Проверка подключения к Telegram API без токена не выполнялась.\n\n")
        if folder == FP:
            readme += ("Все семь задач находятся в lab_python_fp. Каждый файл можно запускать отдельно.\n\n"
                       "```powershell\n../.venv/Scripts/python.exe main.py data_demo.json\n"
                       "../.venv/Scripts/python.exe main.py data_light.json\n```\n\n"
                       "Исходные данные: [data_light.json из курса](https://github.com/ugapanyuk/BKIT_2021/blob/main/notebooks/fp/files/data_light.json). "
                       "Файл загружен без изменений, содержит 4635 записей.\n\n")
        if folder == "ЛР6":
            readme += ("Диалог в личных сообщениях: SHAPE → DIMENSIONS → CONFIRM → END. "
                       "Заново возвращает к выбору фигуры; /cancel завершает разговор. "
                       "Ошибки сохраняют текущее состояние. /start начинает новый расчет. "
                       "END обозначает завершение, а не четвертое состояние. "
                       "Данные хранятся в памяти до завершения разговора или перезапуска процесса.\n\n")
        readme += ("При обычном запуске main.py (в том числе кнопкой ▶ в VS Code) "
                   "открывается ручной ввод. Выбирайте пункт меню и вводите свои значения "
                   "в панели Терминал. Можно выполнить несколько проверок подряд. "
                   "Для выхода введите 0; в диалоге ЛР6 также доступна /exit. "
                   "Режим --demo показывает готовый пример без ручного ввода.\n\n"
                   "Отчет: [исходник Markdown](report/report.md), [PDF](report/report.pdf).\n")
        (ROOT / folder / "README.md").write_text(readme, encoding="utf-8")
        print(f"{folder}: {pages} pages; tests passed", flush=True)


if __name__ == "__main__":
    for specification in LABS.values():
        specification["logic"] += (
            " Обычный запуск main.py открывает ручной ввод: пользователь выбирает пункт меню, "
            "вводит свои данные и получает результат. После проверки можно ввести другой набор. "
            "Готовые примеры запускаются с --demo. В ЛР5 и ЛР6 подключение к Telegram "
            "запускается отдельно с --telegram; по умолчанию используется локальный диалог без токена.")
    LABS["ЛР5"]["logic"] += " Команда /area позволяет ввести свои размеры и в Telegram."
    LABS["ЛР5"]["checks"] = LABS["ЛР5"]["checks"].replace("Четыре", "Пять") + (
        " Дополнительный тест проверяет расчет пользовательских размеров и ошибки команды /area.")
    main()
