from core.tts import speak
from modules.commands.web_apps import web_commands
from modules.commands.jokes import jokes
from modules.commands.system import system_status

def command_prompt():
    while True:
        cmd = input("Enter your command: \n")
        cmd = cmd.lower()

        if cmd=="who are you":
            reply = "I am Draco CLI. A project made for automating tasks."
            print(reply)
            speak(reply)
        
        elif cmd=="who created you":
            reply = "My master Aryan Sonsurkar created me to learn python deeply and automate his tasks."
            print(reply)
            speak(reply)

        elif cmd=="exit":
            reply = "Goodbye Bro!!!"
            print(reply)
            speak(reply)
            break
        
        elif cmd=="what features do you have":
            print("I can automate things for you..This is my feature list:-\nIntroduction of myself\ncan speak output\n")
            speak("I can automate things for you..This is my feature list")

        elif "open" in cmd:
            web_commands(cmd)
        
        elif "joke" in cmd:
            jokes(cmd)
        
        elif "help" in cmd or "commands" in cmd:
             print("Available Commands:\n- who are you\n- who created you\n- open github\n- open youtube\n- open leetcode\n- joke\n- exit")
             speak("Available Commands...")
        
        elif "system status" in cmd or "system info" in cmd or "my pc" in cmd:
            system_status()

        else:
            print("This is command is not available.")