import sys
from lab_telegram_fsm.bot import main


if __name__ == "__main__":
    if "--demo" in sys.argv:
        from demo import run
        run()
    else:
        main()
