import argparse
import json
from pathlib import Path

# Поддерживаются python -m lab_python_fp.process_data и прямой запуск файла.
if __package__:
    from .field import field
    from .unique import Unique
    from .gen_random import gen_random
    from .print_result import print_result
    from .cm_timer import cm_timer_1
else:
    from field import field
    from unique import Unique
    from gen_random import gen_random
    from print_result import print_result
    from cm_timer import cm_timer_1


@print_result
def f1(arg):
    return sorted(Unique(field(arg, "job-name"), ignore_case=True), key=str.casefold)


@print_result
def f2(arg):
    return list(filter(lambda title: title.casefold().startswith("программист"), arg))


@print_result
def f3(arg):
    return list(map(lambda title: title + " с опытом Python", arg))


@print_result
def f4(arg):
    return [f"{title}, зарплата {salary} руб." for title, salary in zip(arg, gen_random(len(arg), 100000, 200000))]


def main():
    parser = argparse.ArgumentParser(description="Обработка вакансий")
    parser.add_argument("path", nargs="?", type=Path,
                        default=Path(__file__).resolve().parents[1] / "data_light.json")
    args = parser.parse_args()
    with args.path.open(encoding="utf-8-sig") as stream:
        data = json.load(stream)
    with cm_timer_1():
        f4(f3(f2(f1(data))))


if __name__ == "__main__":
    main()
