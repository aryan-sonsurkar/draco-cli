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

def get_recent_commands(limit=20):
    try:
        limit = int(limit)
    except Exception:
        limit = 20
    if limit <= 0:
        return []
    return session_data.get("commands", [])[-limit:]

def get_last_command():
    commands = session_data.get("commands", [])
    return commands[-1] if commands else None

def load_previous_session_commands(limit=20):
    try:
        if not os.path.exists(SESSION_FILE):
            return []
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
        commands = data.get("commands", [])
        try:
            limit = int(limit)
        except Exception:
            limit = 20
        if limit <= 0:
            return []
        return commands[-limit:]
    except Exception:
        return []

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
