import time
import datetime
from core.tts import speak

def run_scheduler():
    triggered = False

    while True:
        now = datetime.datetime.now()
        day = now.strftime("%A")
        hour = now.hour
        minute = now.minute

        if day in ["Saturday", "Sunday"] and hour == 19 and minute == 0:
            if not triggered:
                speak("It's time for Guild Wars. Let's rush.")
                print("\n[DRACO ALERT] It's time for Guild Wars. Let's rush.\n")
                triggered = True

        if minute != 0:
            triggered = False

        time.sleep(15)
