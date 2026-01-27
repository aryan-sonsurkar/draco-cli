import os
import time
from core.tts import speak

def close_apps():
    print("\nInitializing system deactivation...\n")
    speak("Initializing system deactivation")
    time.sleep(1)
    print("\nClosing active applications...\n")
    speak("Closing active applications")
    os.system("taskkill /f /im explorer.exe")

def shutdown_system():
    print("\nShutting down system. Good work today.\n")
    speak("Shutting down system. Good work today.")
    time.sleep(1)
    os.system("shutdown /s /t 0")

def lock_system():
    print("\nLocking system. Rest well.\n")
    speak("Locking system. Rest well.")
    time.sleep(1)
    os.system("start explorer.exe")
    os.system("rundll32.exe user32.dll,LockWorkStation")

def wind_up():
    close_apps()
    print("\nWorkspace secured.\n")
    speak("Workspace secured.")
    speak("Shall i shutdown the system or lock it?")
    choice = input("Shall i shutdown the system or lock it? (shutdown/lock):  ").lower()
    if "shutdown" in choice:
        shutdown_system()
    elif "lock" in choice:
        lock_system()
    else:
        print("\nInvalid Choice! Wind up cancelled.\n")
        speak("Invalid Choice! Wind up cancelled.")