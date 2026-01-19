from core.tts import speak
import time

reminders = []

def remind(cmd):
    reminder = cmd.replace("remind me to","").strip()
    if " in " in reminder:
        split_result = reminder.split(" in ")
        task_part = split_result[0]
        time_part = split_result[1]
    else:
        print("You haven't mentioned time.")
        speak("You haven't mentioned time.")

    if "minutes" in time_part:
        number = time_part.replace("minutes","").strip()
        number = int(number)
        total_seconds = number * 60

    elif "minute" in time_part:
        number = time_part.replace("minute","").strip()
        number = int(number)
        total_seconds = number * 60

    elif "hour" in time_part:
        number = time_part.replace("hour","").strip()
        total_seconds = number * 3800

    elif "hours" in time_part:
        number = time_part.replace("hours","").strip()
        total_seconds = number * 3800

    else:
        print("Invalid time unit!")
        speak("Invalid time unit!")

    reminders.append({
        "task":task_part,
        "seconds":total_seconds
    })

    reply = f"Okay, I will remind you to {task_part} in {time_part}"
    print(reply)
    speak(reply)

    time.sleep(total_seconds)

    final_msg = f"Reminder! It's time to {task_part}"
    print(final_msg)
    speak(final_msg)