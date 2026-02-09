import sys
import time
from core.tts import speak
from modules.Brain.web_apps import web_commands
from modules.Brain.jokes import jokes
from modules.Brain.system import system_status, datetime_info
from modules.Brain.notes import notes
from modules.Brain.reminder import remind
from modules.Ollama.generators.calc_gen import generate_calculator_code,solve_calculator
from modules.Ollama.fallback import fallback
from modules.Ollama.writers.essay_writer import essay_writer
from modules.Ollama.writers.explainer import explainer,motivater
from modules.Ollama.generators.algo_gen import algo_gen
from modules.Ollama.writers.analyzer import analyze
from modules.Automations.git_helper import git_push, git_repo
from modules.Automations.file_opener import open_file_or_folder
from modules.Ollama.writers.reflector import reflect
from modules.Automations.typer import draco_type
from modules.Automations.web_searcher import draco_search
from modules.Automations.winding_up_system import wind_up
from modules.Automations.quick_actions import open_coding_setuo,open_exam_setup,open_study_setup
from modules.Automations.jarvis_theme import jarvis
from modules.Brain.voice_listener import listen_cmd
from core import state
from modules.Automations.macros_runner import list_macros, show_macro, run_macro
from modules.Brain.study_timer import start_study_timer
from modules.Ollama.writers.assignment_writer import assignment_writer
from modules.Ollama.writers.assignment_enhancer import enhance_assignment
from modules.Brain.decision_assistant import decision_assistant
from modules.Brain.session import start_session, log_command, end_session
from modules.Brain.code_explainer import explain_code
from modules.Automations.boilerplate import (
    create_web_project,
    create_python_project
)

def choose_mode():
    if state.INPUT_MODE is None:
        mode = input("Choose input mode (text/voice):   ").lower()
        state.INPUT_MODE = "voice" if "voice" in mode else "text"
        speak(f"{state.INPUT_MODE} mode activated")
    
def command_prompt():
    choose_mode()
    while True:
        if state.INPUT_MODE == "voice":
            cmd = listen_cmd()
            if not cmd:
                continue
            print(f"You said: {cmd}")
        else:
            cmd = input("You:  ").lower()
        
        handle_command(cmd)

def handle_command(cmd):
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
            sys.exit(0)
        
        elif cmd=="end session" or cmd=="session end":
             end_session()
             sys.exit(0)
             
        elif cmd=="what features do you have":
            print("I can automate things for you..This is my feature list:-\nIntroduction of myself\ncan speak output\n")
            speak("I can automate things for you..This is my feature list")

        elif cmd.startswith("open website"):
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
        
        elif "create an essay on" in cmd:
            essay = essay_writer(cmd)
            print(essay)
            speak("Here is your essay....")
        
        elif "explain me this" in cmd:
            explain = explainer(cmd)
            print(explain)
            speak(explain)
        
        elif "write algorithm for" in cmd:
            algorithm = algo_gen(cmd)
            print(algorithm)
            speak(algorithm)
        
        elif "motivate" in cmd:
            motivation = motivater()
            print(motivation)
            speak(motivation)
        
        elif cmd.startswith("analyze") or cmd.startswith("think"):
            print("[SYSTEM ANALYSIS INITIATED]")
            speak("SYSTEM ANALYSIS INITIATED")
            reply = analyze(cmd)
            print(reply)
            speak(reply)
            print("[ANALYSIS COMPLETED]")
            speak("ANALYSIS COMPLETED")
        
        elif cmd.startswith("git push with message"):
            git_cmd = git_push(cmd)
            print(git_cmd)
            speak("Here are the commands to push the repo on github. Bro you are doing great keep up the good work.I am proud of you!")

        elif cmd.startswith("create a new repo"):
            git_cmd = git_repo()
            print(git_cmd)
            speak("Bro just make a new repo with this and let's hit that consistency bar on top.")
        
        elif cmd.startswith("open file"):
            name = cmd.replace("open file","").strip()
            reply = open_file_or_folder(name)
            print(reply)
            speak(reply)

        elif cmd.startswith("open folder"):
            name = cmd.replace("open folder","").strip()
            reply = open_file_or_folder(name)
            print(reply)
            speak(reply)
        
        elif cmd=="daily reflection" or cmd=="reflect today" or cmd=="rate today" or cmd=="Today was a great day":
            reply = reflect()
            print("\n----------Draco Report----------\n")
            print(reply)
            speak(reply)
        
        elif cmd.startswith("draco type") or cmd.startswith("draco write") or cmd.startswith("write about"):
            cmd = cmd.replace("draco type","").replace("draco write","").replace("write about","").strip()
            if cmd:
                draco_type(cmd)
            else:
                print("\nPlease provide what to type.\n")
                speak("Please provide what to type.")
        
        elif cmd.startswith("search"):
            cmd = cmd.replace("search","").strip()
            draco_search(cmd)
        
        elif "end of the day" in cmd or "wind up" in cmd:
            wind_up()
        
        elif cmd=="study setup" or cmd=="open study setup":
            open_study_setup()

        elif cmd=="coding setup" or cmd=="open coding setup":
            open_coding_setuo()

        elif cmd=="exam prep setup" or cmd=="open exam prep setup" or cmd=="let's study for exam":
            open_exam_setup()

        elif "daddy's home" in cmd or "I am back" in cmd or "iron man mode" in cmd or "wake up draco" in cmd:
            jarvis()
        
        elif cmd.startswith("macro"):
            parts = cmd.split()

            if len(parts) == 1 or parts[1] == "help":
                print("Usage:")
                print("macro list")
                print("macro show <name>")
                print("macro <name>")
    
            elif parts[1] == "list":
                list_macros()

            elif parts[1] == "show" and len(parts) == 3:
                show_macro(parts[2])

            elif len(parts) == 2:
                run_macro(parts[1], handle_command)

            else:
                print("Invalid macro command.")

        elif cmd in ["study","focus","pomodoro"]:
            print("Entering Study Mode...\n")
            speak("Entering Study Mode")
            time.sleep(1)
            start_study_timer()
        
        elif cmd=="write assignment" or cmd=="assignment":
            assignment_writer()
        
        elif "enhance assignment" in cmd:
            enhance_assignment()
        
        elif "decide" in cmd or "choose" in cmd:
            decision_assistant()
        
        elif "explain my code" in cmd or "explain code" in cmd:
            explain_code()
        
        elif cmd.startswith("new"):
            parts = cmd.split()

            if len(parts) < 3:
                reply = "Usage: new web <project_name> or new python <project_name>"
                print(reply)
                speak(reply)
                return

            project_type = parts[1]
            project_name = parts[2]

            if project_type == "web":
                reply = create_web_project(project_name)
                print(reply)
                speak(reply)

            elif project_type == "python":
                reply = create_python_project(project_name)
                print(reply)
                speak(reply)

            else:
                reply = "Unknown project type. Available: web, python."
                print(reply)
                speak(reply)

        else:
            reply = fallback(cmd)
            print(reply)
            speak(reply) 