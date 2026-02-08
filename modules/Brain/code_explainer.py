from modules.Ollama.ollama_helper import ask_ollama
from core.tts import speak

def explain_code():
    print("Paste Your Code Below:\n")
    speak("Paste Your Code Below")
    print("Type END on a new line when finished.\n")
    speak("Type END on a new line when finished.")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    
    code = "\n".join(lines)

    if not code.strip():
        print("No code provided.")
        speak("No code provided.")
        return
    
    prompt = f"""
Explain the following code in very simple langauge.
Assume I am tired and new to programming.
No jargon.
Short explanations.
Step by Step.
Do NOT rewrite the code.

CODE:
{code}
"""
    result = ask_ollama(prompt)

    print("\n---Simple Explanation--0\n")
    print(result)
    speak(result)
    