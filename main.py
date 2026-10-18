"""Общее меню лабораторных. Также запускается файлом Запустить лабораторные.cmd."""
import argparse
import os
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent
LABS = {
    "1": ("ЛР1 — Биквадратное уравнение", "ЛР1_Основные_конструкции_Python/procedural/biquadratic.py"),
    "2": ("ЛР2 — Геометрические фигуры и ООП", "ЛР2/main.py"),
    "3": ("ЛР3 — Модульное тестирование", "ЛР3/main.py"),
    "4": ("ЛР4 — Шаблоны проектирования, заказ в кафе", "ЛР4/main.py"),
    "5": ("ЛР5 — Простой бот, локальный режим", "ЛР5/main.py"),
    "6": ("ЛР6 — Бот с конечным автоматом, локальный режим", "ЛР6/main.py"),
    "7": ("Функциональные возможности Python — семь задач", "ЛР2_Функциональные_возможности_Python/main.py"),
}


def run_lab(choice):
    title, relative = LABS[choice]
    target = ROOT / relative
    print(f"\n=== {title} ===", flush=True)
    old_path, old_argv, old_cwd = sys.path[:], sys.argv[:], Path.cwd()
    previous_modules = set(sys.modules)
    try:
        os.chdir(target.parent)
        sys.path.insert(0, str(target.parent))
        sys.argv = [str(target)]
        # В том же процессе input() читает ввод без потерь и буферизации родителем.
        runpy.run_path(str(target), run_name="__main__")
    except SystemExit as exc:
        if exc.code not in (0, None):
            print(f"Программа завершена: {exc.code}")
    except ModuleNotFoundError as exc:
        print(f"Не установлен пакет: {exc.name}. Установите зависимости по README.")
    finally:
        os.chdir(old_cwd)
        sys.path[:] = old_path
        sys.argv[:] = old_argv
        # У ботов одинаковые имена demo и interactive, но разные реализации.
        for name in set(sys.modules) - previous_modules:
            filename = getattr(sys.modules[name], "__file__", None)
            if filename and Path(filename).resolve().is_relative_to(target.parent):
                del sys.modules[name]


def main():
    python_venv = ROOT / ".venv" / "Scripts" / "python.exe"
    if python_venv.exists() and Path(sys.executable).resolve() != python_venv.resolve():
        os.execv(str(python_venv), [str(python_venv), str(Path(__file__).resolve()), *sys.argv[1:]])
    parser = argparse.ArgumentParser(description="Запуск лабораторных работ")
    parser.add_argument("--lab", choices=LABS, help="Открыть выбранную работу напрямую")
    args = parser.parse_args()
    if args.lab:
        run_lab(args.lab)
        return
    while True:
        print("\nЛАБОРАТОРНЫЕ РАБОТЫ")
        for number, (title, _) in LABS.items():
            print(f"{number} — {title}")
        print("0 — Выход")
        choice = input("Введите номер работы и нажмите Enter: ").strip()
        if choice == "0":
            return
        if choice not in LABS:
            print("Выберите номер из меню.")
            continue
        run_lab(choice)
        print("\nВозврат к выбору лабораторной работы.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nПрограмма завершена.")
