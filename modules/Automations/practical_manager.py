import json
import os
from datetime import datetime
from core.tts import speak

DATA_FILE = "data/practicals.json"

def load_data():
    if not os.path.exists("data"):
        os.mkdir("data")

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_practical(num):
    data = load_data()
    if num in data:
        reply = f"Practical {num} already exists."
        print(reply)
        speak(reply)
        return

    data[num] = {
        "status": "pending",
        "created": datetime.now().strftime("%d-%m-%Y")
    }

    save_data(data)
    reply = f"Practical {num} added."
    print(reply)
    speak(reply)

def mark_done(num):
    data = load_data()
    if num not in data:
        reply = f"Practical {num} not found."
        print(reply)
        speak(reply)
        return

    data[num]["status"] = "done"
    data[num]["completed"] = datetime.now().strftime("%d-%m-%Y")
    save_data(data)

    reply = f"Practical {num} marked as done."
    print(reply)
    speak(reply)

def list_practicals():
    data = load_data()
    if not data:
        reply = "No practicals added yet."
        print(reply)
        speak(reply)
        return

    print("Practicals:")
    for num, info in data.items():
        print(f"{num} - {info['status']}")

    speak("Here is your practical list.")

def practical_status():
    data = load_data()
    total = len(data)
    done = sum(1 for p in data.values() if p["status"] == "done")
    pending = total - done

    reply = f"Total practicals {total}. Done {done}. Pending {pending}."
    print(reply)
    speak(reply)
