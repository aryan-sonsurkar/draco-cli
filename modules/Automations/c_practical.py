import time
import os
import subprocess
from modules.Automations.typer import raw_type, press_keys
from core.tts import speak
from modules.Ollama.ollama_helper import ask_ollama
DOSBOX_PATHS = [
    r"C:\Program Files (x86)\DOSBox-0.74-3\DOSBox.exe",
    r"C:\Program Files\DOSBox-0.74-3\DOSBox.exe",
    r"C:\DOSBox\DOSBox.exe"
]

TURBOC_DIR = r"C:\TURBOC3"

C_BOILERPLATE = """
#include<stdio.h>
#include<conio.h>

void main()
{
    int ;
    clrscr();
    getch();
}
"""

def generate_c_program():
    speak("Tell me the C practical question.")
    question = input("Enter C practical question: ")

    prompt = f"""
    Write a complete Turbo C compatible C program.
    Use void main(), clrscr(), and getch().
    No modern syntax.
    Question: {question}
    """

    speak("Generating program using AI.")
    response = ask_ollama(prompt)

    write_generated_code(response)

def open_turbo_c():
    dosbox = None
    for path in DOSBOX_PATHS:
        if os.path.exists(path):
            dosbox = path
            break

    if not dosbox or not os.path.exists(TURBOC_DIR):
        speak("Turbo C setup not found.")
        print("Turbo C or DOSBox not found.")
        return False

    speak("Opening Turbo C plus plus.")

    commands = [
        "-c", f"mount c {TURBOC_DIR}",
        "-c", "c:",
        "-c", "cd BIN",
        "-c", "TC"
    ]

    subprocess.Popen([dosbox] + commands)
    time.sleep(12)
    return True

def write_generated_code(code):
    if not open_turbo_c():
        return

    time.sleep(2)

    press_keys("alt")
    press_keys("f")
    press_keys("n")

    time.sleep(2)

    raw_type(code)
    speak("Program written successfully.")