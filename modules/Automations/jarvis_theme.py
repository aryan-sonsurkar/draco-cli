import os
from core.tts import speak
import webbrowser
import subprocess
import time

def jarvis():
    print("\nWelcome Back Sir! \nIRON MAN MODE ACTIVATED\n")
    speak("Welcome back sir! IRON MAN MODE ACTIVATED.")
    time.sleep(1)
    webbrowser.open("https://github.com")
    time.sleep(0.5)
    webbrowser.open("https://leetcode.com")
    time.sleep(0.5)
    webbrowser.open("https://chatgpt.com")
    time.sleep(0.5)
    subprocess.Popen("code",shell=True)
    time.sleep(0.5)
    subprocess.Popen("spotify",shell=True)
    print("All systems are ready. Let's build or research")
    speak("All systems are ready. Let's build or research")