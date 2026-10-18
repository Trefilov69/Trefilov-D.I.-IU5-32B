"""Проверка пользовательского ввода через реальные процессы main.py."""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FP = "ЛР2_Функциональные_возможности_Python"
CASES = [
    ("ЛР2", "1\n6\n7\nкрасный\n0\n", "площадь = 42"),
    ("ЛР2", "2\n2,5\n\n0\n", "площадь = 6.25"),
    ("ЛР2", "3\n-2\n0\n", "Ошибка"),
    ("ЛР3", "1\n6\n7\n0\n", "Площадь: 42.00"),
    ("ЛР3", "2\n-5\n2\n3\n0\n", "Площадь: 9.00"),
    ("ЛР3", "3\n2,5\n0\n", "Площадь: 19.63"),
    ("ЛР3", "2\nnan\n0\n", "Ошибка"),
    ("ЛР4", "1\n1\nда\n0\n", "К оплате: 162.00"),
    ("ЛР4", "2\n2\nнет\n0\n", "К оплате: 160.00"),
    ("ЛР4", "1\n-1\n0\n", "Ошибка"),
    (FP, '1\n[{"x":0},{"x":null},{"y":2}]\nx y\n0\n', "{'y': 2}"),
    (FP, "2\n3\n5\n5\n0\n", "[5, 5, 5]"),
    (FP, '3\n["a","A","b"]\nда\n0\n', "['a', 'b']"),
    (FP, "4\n-7 2 -3\n0\n", "[-7.0, -3.0, 2.0]"),
    (FP, '5\n{"x":42}\n0\n', "x = 42"),
    (FP, "6\n5\n0\n", "contextlib, сумма: 10"),
    (FP, "7\n\n0\n", "с опытом Python"),
    (FP, "1\ninvalid-json\n0\n", "Ошибка"),
    (FP, "7\nmissing-file.json\n0\n", "Ошибка"),
    ("ЛР5", "2\n6 7\n0\n", "Бот: Площадь: 42.00"),
    ("ЛР5", "1\n-2\n1\n3\n0\n", "Бот: Площадь: 9.00"),
    ("ЛР6", "2\n-6 7\n6 7\n1\n0\n", "Бот: Площадь: 42.00"),
    ("ЛР6", "1\n5\n2\n3\n2\n1\n0\n", "Бот: Площадь: 12.57"),
    ("ЛР6", "1\n/cancel\n/start\n1\n3\n1\n0\n", "Бот: Площадь: 9.00"),
]


def main():
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    for index, (folder, user_input, expected) in enumerate(CASES, 1):
        result = subprocess.run([sys.executable, str(ROOT / folder / "main.py")],
                                input=user_input, text=True, encoding="utf-8",
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                cwd=ROOT, env=env, timeout=30)
        if result.returncode != 0 or expected not in result.stdout or "Traceback" in result.stdout:
            raise AssertionError(f"Case {index}: {folder}\n{result.stdout}")
    for folder in ("ЛР2", FP, "ЛР3", "ЛР4", "ЛР5", "ЛР6"):
        result = subprocess.run([sys.executable, str(ROOT / folder / "main.py")],
                                input="", text=True, encoding="utf-8", cwd=ROOT,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                env=env, timeout=30)
        if result.returncode != 0 or "Traceback" in result.stdout:
            raise AssertionError(f"EOF handling: {folder}\n{result.stdout}")
    launcher_input = ("4\n1\n1\nда\n0\n5\n2\n6 7\n0\n"
                      "6\n1\n3\n1\n0\n3\n2\n7\n0\n"
                      "7\n4\n-7 2 -3\n0\n2\n2\n5\n\n0\n"
                      "1\n1\n-5\n4\n0\n")
    result = subprocess.run([sys.executable, str(ROOT / "main.py")],
                            input=launcher_input, text=True, encoding="utf-8",
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            cwd=ROOT.parent, env=env, timeout=60)
    expected_results = ("К оплате: 162.00", "Бот: Площадь: 42.00",
                        "Бот: Площадь: 9.00", "Площадь: 49.00",
                        "[-7.0, -3.0, 2.0]", "площадь = 25", "Действительные корни")
    if result.returncode != 0 or "Traceback" in result.stdout or not all(
            value in result.stdout for value in expected_results):
        raise AssertionError(f"Common launcher\n{result.stdout}")
    print(f"Interactive checks passed: {len(CASES)} scenarios, 6 EOF checks, all 7 launcher entries")


if __name__ == "__main__":
    main()
