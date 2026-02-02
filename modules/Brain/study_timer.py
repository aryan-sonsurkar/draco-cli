import time
import os

FOCUS_TIME = 25*60
BREAK_TIME = 5*60

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_timer(total_seconds, mode):
    while total_seconds > 0:
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        clear_screen()
        print("STUDY TIMER")
        print("------------------")
        print(f"MODE : {mode}")
        print(f"TIME : {minutes:02d}:{seconds:02d}")
        print("------------------")

        time.sleep(1)
        total_seconds -= 1

def main():
    session = 1

    while True:
        clear_screen()
        print(f"SESSION {session} STARTING")
        time.sleep(2)

        run_timer(FOCUS_TIME, "FOCUS")
        clear_screen()
        print("FOCUS SESSION COMPLETE")
        time.sleep(2)

        run_timer(BREAK_TIME, "BREAK")
        clear_screen()
        print("BREAK COMPLETE")
        time.sleep(2)

        session += 1

def start_study_timer():
    main()