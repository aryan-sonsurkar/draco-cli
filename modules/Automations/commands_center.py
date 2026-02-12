import os
import time
import getpass
from datetime import datetime
from core import state
from core.tts import speak

def clear():
    os.system("cls")

def run_command_center():
    speak("Entering command center.")
    
    while True:
        clear()

        user = getpass.getuser()
        directory = os.getcwd().split("\\")[-1]
        current_time = datetime.now().strftime("%H:%M:%S")
        mode = state.INPUT_MODE.upper() if state.INPUT_MODE else "UNKNOWN"

        print("--------------- DRACO COMMAND CENTER ---------------\n")
        print(f"User        : {user}")
        print(f"Directory   : {directory}")
        print(f"Time        : {current_time}")
        print(f"Input Mode  : {mode}")
        print("\n----------------------------------------------------")
        print("Press Q to exit")
        
        time.sleep(1)

        if os.name == "nt":
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch().decode(errors="ignore").lower()
                if key == "q":
                    speak("Exiting command center.")
                    break
