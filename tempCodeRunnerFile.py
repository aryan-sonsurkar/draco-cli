import os
from core.commands import command_prompt
from core.tts import speak
from modules.Brain.session import start_session, log_command, end_session

def main():
    print("----------------------")
    print("Welcome to Draco CLI")
    print("----------------------")
    speak("Initializing systems....")
    speak("Loading modules.....")
    speak("Draco is Online.")
    start_session()
    command_prompt()
    
if __name__=="__main__":
    main()