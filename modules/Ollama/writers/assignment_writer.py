import subprocess
import time
from modules.Ollama.ollama_helper import ask_ollama
from modules.Automations.typer import type_like_human
from core.tts import speak

def assignment_writer():
    print("Enter Assignment title:  ")
    speak("Enter assignment title")
    title = input(">  ")

    print("Enter assignment instructions:  ")
    speak("Enter assignment instructions")
    instructions = input(">  ")

    print("Opening Microsoft Word...")
    speak("opening microsoft word")
    subprocess.Popen("start winword",shell=True)
    time.sleep(5)

    prompt = f"""
Write a well-structured assignment.
Title: {title}
Instructions: {instructions}

Format:
- Title
- Introduction
- Main Content
- Conclusion
"""
    print("Generating Content...")
    speak("Generating Content")
    content = ask_ollama(prompt)

    print("Typing in Word. Do not touch keyboard or mouse.")
    speak("Typing in Word. Do not touch keyboard or mouse.")
    time.sleep(2)

    type_like_human(content)
    print("Assignment Completed!")
    speak("Assignment Completed!")