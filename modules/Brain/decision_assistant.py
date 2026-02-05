from modules.Ollama.ollama_helper import ask_ollama
from core.tts import speak

def decision_assistant():
    print("----Decision Assistant----")

    speak("Enter your options seperate them by commas")
    option = input("Enter your options (comma seperated): ").strip()

    speak("Your energy level low, medium or high")
    energy = input("Your energy level (low/medium/high): ").strip()

    speak("Is there a deadline? yes or no")
    deadline= input("Is there a deadline? (yes/no):  ").strip()

    prompt = f"""
You are a logical AI assistant Draco.
Help the user decide objectively.

Options: {option}
Energy Level: {energy}
Deadline present: {deadline}

Give:
1. Best option
2. Reason (short)
3. Fallback option
Be concise and logical.
"""
    
    result = ask_ollama(prompt)
    print("\n--- Decision Result ---\n")
    print(result)