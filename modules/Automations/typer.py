import pyautogui
import time
import random
import subprocess
from modules.Ollama.ollama_helper import ask_ollama
from core.tts import speak

def press_keys(*keys, delay=0.5):
    for key in keys:
        pyautogui.press(key)
        time.sleep(delay)

def raw_type(text, delay=0.03):
    pyautogui.write(text, interval=delay)

def type_like_human(text):
    for char in text:
        pyautogui.typewrite(char)
        time.sleep(random.uniform(0.0003,0.001))

def draco_type(cmd):
    print("\nOpening Notepad.....\n")
    speak("Opening Notepad.....")
    subprocess.Popen("notepad.exe")

    time.sleep(2)
    pyautogui.click()

    print("\nGenerating content .....\n")
    speak("Generating Content....")
    Prompt = f"Write a clean and simple text about:{cmd}"
    content = ask_ollama(Prompt)

    print("\nDo not touch keyboard or mouse\n")
    speak("Do not touch keyboard or mouse")

    for i in range(3,0,-1):
        print(f"\nTyping starts in {i}....\n")
        speak(f"Typing starts in {i}....")
        time.sleep(1)

    type_like_human(content)
    print(f"\nDone typing {cmd}\n")
    speak(f"Done typing {cmd}")