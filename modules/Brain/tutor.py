import random
import json
import os
import subprocess
from core.tts import speak

WEAK_FILE = "data/weak_memory.json"
NOTES_DIR = "data/notes/"


def ask_ollama(prompt):
    process = subprocess.Popen(
        ["ollama", "run", "llama3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )

    stdout, stderr = process.communicate(prompt)

    return (stdout or "").strip()


def load_weak_memory():
    if not os.path.exists(WEAK_FILE):
        return []
    try:
        with open(WEAK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_weak_memory(data):
    with open(WEAK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def add_to_weak_memory(question, answer):
    memory = load_weak_memory()

    for item in memory:
        if item.get("question") == question:
            return

    memory.append({"question": question, "answer": answer})
    save_weak_memory(memory)



def remove_from_weak_memory(question):
    memory = load_weak_memory()
    memory = [q for q in memory if q["question"] != question]
    save_weak_memory(memory)


def generate_question(source):

    question = ask_ollama(f"""
You are a teacher.

Ask one conceptual question about this topic:

{source}

Only ask the question.
""")

    if not question or len(question) < 5:
        print("Model failed to generate valid question")
        return "", ""

    answer = ask_ollama(f"""
Provide a concise, 2-3 sentence plain-text answer for this question.
Do not use bullet points, markdown formatting, code blocks, or long examples.

Question: {question}
""")
    if not answer:
        print("Model failed to generate valid answer")
        return "", ""

    return question, answer


def check_answer(question, correct_answer, user_answer):
    result = ask_ollama(f"""
Question: {question}
Correct Answer: {correct_answer}
User Answer: {user_answer}

Is the user answer correct?
Reply only YES or NO.
""")

    if result is None:
        return False

    return "YES" in result.upper()


def ask_question(question, answer):
    print("\nQuestion:")
    print(question)

    speak(question)

    user_answer = input("\nYour Answer: ")

    if check_answer(question, answer, user_answer):
        print("\nCorrect.")
        remove_from_weak_memory(question)
    else:
        print("\nIncorrect.")
        print("\nCorrect Answer:")
        print(answer)

        add_to_weak_memory(question, answer)

def train_skill():
    speak("Enter topic.")
    topic = input("Topic: ")

    weak_memory = load_weak_memory()

    # Filter out any invalid or empty entries that might have been stored earlier
    valid_memory = [
        item
        for item in weak_memory
        if isinstance(item, dict)
        and item.get("question")
        and str(item.get("question")).strip()
        and item.get("answer")
        and str(item.get("answer")).strip()
    ]

    if valid_memory:
        item = random.choice(valid_memory)
        speak("Revisiting previous question.")
        ask_question(item["question"], item["answer"])
    else:
        question, answer = generate_question(topic)

        if not question or not answer:
            print("Generation failed.")
            return

        ask_question(question, answer)


def save_notes():
    speak("Enter notes name.")
    name = input("Notes name: ")

    if not name:
        print("Invalid name.")
        return

    speak("Paste notes.")
    notes = input("Notes:\n")

    os.makedirs(NOTES_DIR, exist_ok=True)

    with open(os.path.join(NOTES_DIR, f"{name}.txt"), "w", encoding="utf-8") as f:
        f.write(notes)

    print("Notes saved.")


def list_notes():
    if not os.path.exists(NOTES_DIR):
        print("No notes found.")
        return []

    files = [f for f in os.listdir(NOTES_DIR) if f.endswith(".txt")]

    if not files:
        print("No notes available.")
        return []

    print("\nAvailable Notes:\n")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f.replace('.txt','')}")

    return files


def train_notes():
    files = list_notes()
    if not files:
        return

    try:
        choice = int(input("Select: "))
        selected = files[choice - 1]
    except:
        print("Invalid selection.")
        return

    with open(os.path.join(NOTES_DIR, selected), "r", encoding="utf-8") as f:
        notes = f.read()

    question, answer = generate_question(notes)

    if not question or not answer:
        print("Generation failed.")
        return

    ask_question(question, answer)


def show_weak():
    memory = load_weak_memory()

    if not memory:
        print("No weak questions stored.")
        return

    print("\nWeak Questions:\n")
    for i, item in enumerate(memory, 1):
        print(f"{i}. {item['question']}")


def clear_weak():
    save_weak_memory([])
    print("Weak memory cleared.")
