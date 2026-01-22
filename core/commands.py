from core.tts import speak
from modules.commands.web_apps import web_commands
from modules.commands.jokes import jokes
from modules.commands.system import system_status, datetime_info
from modules.commands.notes import notes
from modules.commands.reminder import remind
from modules.commands.calc_gen import generate_calculator_code,solve_calculator
from modules.commands.fallback import fallback

def command_prompt():
    while True:
        cmd = input("\nEnter your command: \n")
        cmd = cmd.lower()

        if cmd=="who are you":
            reply = "I am Draco CLI. A project made for automating tasks."
            print(reply)
            speak(reply)
        
        elif cmd=="who created you":
            reply = "My master Aryan Sonsurkar created me to learn python deeply and automate his tasks."
            print(reply)
            speak(reply)

        elif cmd=="exit" or cmd=="quit":
            reply = "Shutting down systems.....Goodbye."
            print(reply)
            speak(reply)
            break
        
        elif cmd=="what features do you have":
            print("I can automate things for you..This is my feature list:-\nIntroduction of myself\ncan speak output\n")
            speak("I can automate things for you..This is my feature list")

        elif "open" in cmd:
            web_commands(cmd)
        
        elif "joke" in cmd:
            jokes()
        
        elif "help" in cmd or "commands" in cmd:
             print("Available Commands:\n- who are you\n- who created you\n- open github\n- open youtube\n- open leetcode\n- joke\n- exit")
             speak("Available Commands...")
        
        elif "system status" in cmd or "system info" in cmd or "my pc" in cmd:
            system_status()
        
        elif "today's date" in cmd or "date" in cmd or "time" in cmd:
            datetime_info()
            
        elif "note" in cmd:
            notes(cmd)
        
        elif "remind me" in cmd:
            remind(cmd)
        
        elif "introduce yourself" in cmd or "introduce" in cmd:
            reply = """
            Hello. I am Draco.
            A terminal-based assistant designed for automation,focus,and efficiency.

            I can help you with:
            - Quick Commands
            - System Utilities
            - Notes and reminders
            - Productivity and automation tasks

            Try: system status | note | remind me
            """
            print(reply)
            speak(reply)

        elif "why were you created" in cmd or "purpose" in cmd or "why do you exist" in cmd or "why are you created" in cmd:
            reply = """
            I was created to assist,not to replace.
            I exist to reduce friction between thought and execution.
            To observe commands, process intent, and act without hesitation.

            I do not seek validation.
            I do not make decisions for you.

            I was built to support focus, automate routine tasks, 
            and respond when efficiency matters more than emotion.

            You think.I execute.
            That is my purpose.
            """
            print(reply)
            speak(reply)

        elif "calculator" in cmd and ("make" in cmd or "create" in cmd):
            code = generate_calculator_code(cmd)
            print(code)
            speak("Generated Calculator.")
        
        elif cmd.startswith("calculate"):
            answer = solve_calculator(cmd)
            print(answer)
            speak("Here are the results.")

        else:
            reply = fallback(cmd)
            print(reply)
            speak(reply)