from modules.Ollama.ollama_helper import ask_ollama
from core.tts import speak
from modules.Automations.typer import type_like_human
import subprocess
import time
import pyautogui
import os
import re

LAST_PROJECT_CONTENT = None
LAST_PROJECT_TITLE = None


def extract_files(ai_output):
    files = {}
    current_file = None
    buffer = []

    for line in ai_output.splitlines():
        match = re.match(r"\s*File:\s*(.+)", line, re.IGNORECASE)

        if match:
            if current_file:
                files[current_file] = "\n".join(buffer).strip()
                buffer = []

            current_file = match.group(1).strip()
        else:
            buffer.append(line)

    if current_file:
        files[current_file] = "\n".join(buffer).strip()

    return files


def project_gen():
    global LAST_PROJECT_CONTENT, LAST_PROJECT_TITLE

    speak("Enter project title")
    project_title = input("Enter project title: ").strip()

    speak("Enter Project Idea")
    project_idea = input("Enter Project Idea: ").strip()

    prompt = f"""
Create a small project.

Output format strictly:

File: filename.ext
<code>

File: filename.ext
<code>

Project Title: {project_title}
Project Idea: {project_idea}
"""

    project = ask_ollama(prompt)

    files = extract_files(project)

    if not files:
        print("Failed to detect project structure.")
        speak("Failed to detect project structure.")
        return

    print("\nProject Blueprint:\n")
    speak("Project blueprint ready.")

    for fname in files:
        print(f"- {fname}")

    confirm = input("\nProceed with generation? (y/n): ").lower()

    if confirm != "y":
        speak("Project generation cancelled.")
        return

    os.makedirs(project_title, exist_ok=True)

    for fname, content in files.items():
        full_path = os.path.join(project_title, fname)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    LAST_PROJECT_CONTENT = project
    LAST_PROJECT_TITLE = project_title

    subprocess.Popen("notepad.exe")
    time.sleep(2)
    pyautogui.click()

    speak("Typing project files.")

    for fname, content in files.items():
        print(f"\nTyping {fname}...\n")
        speak(f"Typing {fname}")

        type_like_human(f"\n\n===== {fname} =====\n\n")
        type_like_human(content)

    speak(f"Successfully created {project_title}")
    print(f"\nProject '{project_title}' generated.\n")


def explain_last_project():
    if not LAST_PROJECT_CONTENT:
        print("No project found.")
        speak("No project found.")
        return

    speak("Explaining last generated project.")

    explanation = ask_ollama(f"""
Explain this generated project in simple terms:

{LAST_PROJECT_CONTENT}
""")

    print("\nProject Explanation:\n")
    print(explanation)
    speak("Explanation completed.")
