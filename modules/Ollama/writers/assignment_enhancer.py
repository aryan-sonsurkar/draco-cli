import pyperclip
import time
from modules.Ollama.ollama_helper import ask_ollama
from modules.Automations.typer import type_like_human
from core.tts import speak

def enhance_assignment(tone="formal"):
    print("\nSelect your text in Word and press CTRL + C...")
    speak("Select your text in Word and press CTRL + C")
    time.sleep(3)

    text = pyperclip.paste()

    if not text.strip():
        print("Clipboard is empty. Copy text first.")
        speak("Clipboard is empty. Copy text first.")
        return
    
    print("Enhancing assignment....")
    speak("Enhancing assignment")

    prompt = f"""
Rewrite the following assignment content.
Rules:-
- Keep the original meaning
- Improve grammar and clarity
- Sound like a real student
- Use {tone} English
- No AI phrases
- No emojis
- Suitable for diploma/college assignment

Text:
{text}
"""
    improved_text = ask_ollama(prompt)

    if not improved_text.strip():
        print("Empty Response...")
        speak("Empty Response")
        return
    
    print("Place your cursor in Word. Typing starting soon...")
    speak("Place your cursor in Word. Typing starting soon")
    time.sleep(5)

    type_like_human(improved_text)

    print("Assignment enhancement completed.")
    speak("Assignment enhancement completed.")