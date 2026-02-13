import json
import os
from core.tts import speak

DATA_FILE = "data/syllabus.json"

def load_syllabus():
    if not os.path.exists(DATA_FILE):
        print("Syllabus database not found.")
        speak("Syllabus database not found.")
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def syllabus_list():
    data = load_syllabus()
    if not data:
        return

    print("Available Subjects:")
    for subject in data:
        print(f"- {subject}")

    speak("Here are your subjects.")

def syllabus_show(subject):
    data = load_syllabus()
    subject = subject.lower()

    if subject not in data:
        print("Subject not found.")
        speak("Subject not found.")
        return

    print(f"\nSyllabus for {subject}:\n")
    for topic in data[subject]:
        print(f"- {topic}")

    speak(f"Showing syllabus for {subject}")

def syllabus_search(keyword):
    data = load_syllabus()
    keyword = keyword.lower()

    print("\nMatching Topics:\n")

    found = False
    for subject, topics in data.items():
        for topic in topics:
            if keyword in topic.lower():
                print(f"{subject} → {topic}")
                found = True

    if not found:
        print("No matching topics found.")

    speak("Search completed.")
