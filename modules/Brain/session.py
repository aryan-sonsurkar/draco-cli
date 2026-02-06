import time
import json
import os
from core.tts import speak

SESSION_FILE = "data/session.json"

session_data = {
    "start_time": None,
    "commands": [],
    "files": [],
    "notes": []
}

def start_session():
    session_data["start_time"] = time.time()
    speak("Session started. I will track your work.")
    print(" Session started.")

def log_command(cmd):
    session_data["commands"].append(cmd)

def log_file(file):
    session_data["files"].append(file)

def log_note(note):
    session_data["notes"].append(note)

def end_session():
    session_data["end_time"] = time.time()
    duration = round(
        (session_data["end_time"] - session_data["start_time"]) / 60, 2
    )

    summary = {
        "duration_minutes": duration,
        "commands_used": len(session_data["commands"]),
        "files_opened": len(session_data["files"]),
        "notes_added": len(session_data["notes"]),
        "commands": session_data["commands"],
        "files": session_data["files"],
        "notes": session_data["notes"]
    }

    os.makedirs("data", exist_ok=True)
    with open(SESSION_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    print(" Session ended.")
    print(f" Duration: {duration} minutes")

    speak(
        f"Session ended. You worked for {duration} minutes. "
        f"You used {len(session_data['commands'])} commands."
    )
