import sys
from lab_python_fp.process_data import main as process_main
from lab_python_fp.interactive import main


if __name__ == "__main__":
    try:
        if "--demo" in sys.argv:
            sys.argv.remove("--demo")
            process_main()
        elif len(sys.argv) > 1:
            process_main()
        else:
            main()
    except (EOFError, KeyboardInterrupt):
        print("\nПрограмма завершена.")
