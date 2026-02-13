import os
import threading
from core.commands import command_prompt
from core.tts import speak
from modules.Brain.session import start_session
from modules.Automations.scheduler import run_scheduler

def main():
    print("----------------------")
    print("Welcome to Draco CLI")
    print("----------------------")

    speak("Initializing systems....")
    speak("Loading modules.....")
    speak("Draco is Online.")

    start_session()

    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    command_prompt()

if __name__ == "__main__":
    main()
