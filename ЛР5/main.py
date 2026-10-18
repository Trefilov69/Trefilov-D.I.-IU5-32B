import sys
from lab_telegram_bot.bot import main


if __name__ == "__main__":
    try:
        if "--demo" in sys.argv:
            from demo import run
            run()
        elif "--telegram" in sys.argv:
            main()
        else:
            from interactive import run
            run()
    except (EOFError, KeyboardInterrupt):
        print("\nПрограмма завершена.")
