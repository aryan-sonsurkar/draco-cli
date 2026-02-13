from modules.Ollama.ollama_helper import ask_ollama
from core.tts import speak

def generate_questions():
    speak("Paste your notes. Press Enter twice when done.")

    print("\nPaste Notes Below:\n")

    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    notes = "\n".join(lines)

    speak("Generating questions.")

    prompt = f"""
Generate exam preparation questions from these notes.

Include:
- Viva questions
- Multiple choice questions
- Short answer questions
- Long answer questions

Notes:
{notes}
"""

    questions = ask_ollama(prompt)

    print("\nGenerated Questions:\n")
    print(questions)

    speak("Questions generated.")
