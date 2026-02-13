from modules.Ollama.ollama_helper import ask_ollama
from core.tts import speak
from modules.Automations.typer import type_like_human
import subprocess
import time
import pyautogui

def project_gen():
    speak("Enter project title")
    project_title = input("Enter project title:   ").strip()
    speak("Enter Project Idea")
    project_idea = input("Enter Project Idea:  ").strip()
    prompt = f"""
Create an project using any suitable langauge for it. Output only codes for it with file names and all.
Project Title: {project_title}
Project Idea: {project_idea}
"""
    project = ask_ollama(prompt)

    print("\nOpening Notepad.....\n")
    speak("Opening Notepad.....")
    subprocess.Popen("notepad.exe")
   
    time.sleep(2)
    pyautogui.click()
    print("\nDo not touch keyboard or mouse\n")
    speak("Do not touch keyboard or mouse")

    for i in range(3,0,-1):
        print(f"\nTyping starts in {i}....\n")
        speak(f"Typing starts in {i}....")
        time.sleep(1)
        
    type_like_human(project)
    print(f"\nSuccessfully created {project_title}\n")
    speak(f"Successfully created {project_title}")