import sys
import time
import difflib
import os
import json
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
from modules.Automations.macros_runner import list_macros, show_macro, run_macro, save_macro
from modules.Brain.study_timer import start_study_timer
from modules.Ollama.writers.assignment_writer import assignment_writer
from modules.Ollama.writers.assignment_enhancer import enhance_assignment
from modules.Brain.decision_assistant import decision_assistant
from modules.Brain.session import start_session, log_command, end_session, get_recent_commands, load_previous_session_commands
from modules.Brain.code_explainer import explain_code
from modules.Automations.boilerplate import (
    create_web_project,
    create_python_project
)
from modules.Automations.c_practical import write_c_boilerplate
from modules.Automations.practical_manager import (
    add_practical,
    mark_done,
    list_practicals,
    practical_status
)
from modules.Automations.commands_center import run_command_center
from modules.Ollama.generators.project_gen import project_gen, explain_last_project
from modules.Brain.syllabus_manager import syllabus_list, syllabus_show, syllabus_search
from modules.Ollama.writers.question_gen import generate_questions
from modules.Brain.tutor import train_skill, train_notes, show_weak, clear_weak, save_notes
from modules.Automations.file_workflow import (
    create_folder,
    copy_clipboard_file,
    move_clipboard_file,
    send_clipboard_file_whatsapp,
    send_file_to_contact
)
import core.state as state


_macro_recording_name = None
_macro_recording_commands = []
_last_executed_command = None

SAFE_MODE = False
ALIAS_FILE = os.path.join("aliases.json")

_HELP_ENTRIES = [
    {
        "category": "Core",
        "commands": [
            ("help", "Show available commands (use: help <keyword>)"),
            ("history [n]", "Show recent commands"),
            ("again", "Run the last command again"),
            ("safe mode on/off/status", "Confirm before risky actions"),
            ("exit / quit", "Exit Draco"),
            ("end session", "End the session and save summary"),
        ],
    },
    {
        "category": "Macros",
        "commands": [
            ("macro list", "List macros"),
            ("macro show <name>", "Show macro commands"),
            ("macro <name> [--repeat N]", "Run a macro"),
            ("macro record <name>", "Start recording commands into a macro"),
            ("macro stop", "Stop recording and save"),
            ("macro cancel", "Stop recording without saving"),
        ],
    },
    {
        "category": "Aliases",
        "commands": [
            ("alias list", "List aliases"),
            ("alias show <name>", "Show an alias"),
            ("alias add <name> <command>", "Create or overwrite an alias"),
            ("alias remove <name>", "Remove an alias"),
        ],
    },
    {
        "category": "Common",
        "commands": [
            ("open website <name>", "Open a website"),
            ("note add / note show", "Notes system"),
            ("system status", "System info"),
            ("send file on whatsapp", "Send clipboard file via WhatsApp"),
            ("study / focus / pomodoro", "Start study timer"),
        ],
    },
]


def _format_help(keyword=None):
    keyword_l = keyword.lower().strip() if keyword else None
    lines = []
    for section in _HELP_ENTRIES:
        matched = []
        for cmd_name, cmd_desc in section["commands"]:
            hay = f"{cmd_name} {cmd_desc}".lower()
            if not keyword_l or keyword_l in hay:
                matched.append((cmd_name, cmd_desc))
        if not matched:
            continue
        lines.append(f"\n[{section['category']}]\n")
        for cmd_name, cmd_desc in matched:
            lines.append(f"- {cmd_name}  ->  {cmd_desc}")
    if not lines:
        return "No matching help entries found. Try: help"
    return "\n".join(lines).strip()


def _suggest_command(cmd):
    cmd = (cmd or "").strip().lower()
    if not cmd:
        return None
    candidates = []
    for section in _HELP_ENTRIES:
        for cmd_name, _ in section["commands"]:
            candidates.append(cmd_name.lower())
            candidates.append(cmd_name.split()[0].lower())
    candidates = list(dict.fromkeys([x for x in candidates if x]))
    try:
        from modules.Automations.macros_runner import load_macros
        macros = load_macros()
        for name in macros.keys():
            candidates.append(f"macro {name}")
    except Exception:
        pass
    return difflib.get_close_matches(cmd, candidates, n=3, cutoff=0.6)


def _load_aliases():
    if not os.path.exists(ALIAS_FILE):
        return {}
    try:
        with open(ALIAS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_aliases(aliases):
    with open(ALIAS_FILE, "w", encoding="utf-8") as f:
        json.dump(aliases, f, indent=2)


def _expand_alias(cmd):
    aliases = _load_aliases()
    # Exact-match expansion only (keeps behavior predictable)
    expanded = aliases.get(cmd)
    return expanded if isinstance(expanded, str) and expanded.strip() else cmd


def _confirm_action(message):
    if not SAFE_MODE:
        return True
    try:
        ans = input(f"{message} (y/n): ").strip().lower()
        return ans in ["y", "yes"]
    except Exception:
        return False


def _dispatch_core(cmd):
    global SAFE_MODE

    if cmd == "safe mode on":
        SAFE_MODE = True
        print("Safe mode enabled.")
        speak("Safe mode enabled")
        return True

    if cmd == "safe mode off":
        SAFE_MODE = False
        print("Safe mode disabled.")
        speak("Safe mode disabled")
        return True

    if cmd in ["safe mode", "safe mode status"]:
        status = "ON" if SAFE_MODE else "OFF"
        print(f"Safe mode: {status}")
        speak("Safe mode status")
        return True

    if cmd.startswith("alias"):
        parts = cmd.split(maxsplit=3)
        aliases = _load_aliases()

        if len(parts) == 1 or (len(parts) == 2 and parts[1] == "help"):
            print("Usage:")
            print("alias list")
            print("alias show <name>")
            print("alias add <name> <command>")
            print("alias remove <name>")
            return True

        if parts[1] == "list" and len(parts) == 2:
            if not aliases:
                print("No aliases found.")
                return True
            print("Available aliases:")
            for name in sorted(aliases.keys()):
                print(f"- {name}")
            return True

        if parts[1] == "show" and len(parts) == 3:
            name = parts[2]
            if name not in aliases:
                print("Alias not found.")
                return True
            print(f"Alias '{name}': {aliases[name]}")
            return True

        if parts[1] == "remove" and len(parts) == 3:
            name = parts[2]
            if name not in aliases:
                print("Alias not found.")
                return True
            del aliases[name]
            _save_aliases(aliases)
            print(f"Removed alias '{name}'.")
            return True

        if parts[1] == "add" and len(parts) >= 4:
            name = parts[2].strip()
            target = parts[3].strip()
            if not name or not target:
                print("Usage: alias add <name> <command>")
                return True
            aliases[name] = target
            _save_aliases(aliases)
            print(f"Saved alias '{name}' -> {target}")
            return True

        print("Invalid alias command.")
        return True

    return False



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

        cmd = (cmd or "").strip().lower()

        if cmd and not cmd.startswith("alias") and not cmd.startswith("safe mode"):
            cmd = _expand_alias(cmd)

        global _macro_recording_name, _macro_recording_commands, _last_executed_command

        if _macro_recording_name and cmd and not cmd.startswith("macro record") and cmd not in ["macro stop", "macro cancel"]:
            _macro_recording_commands.append(cmd)

        if cmd:
            log_command(cmd)

        if cmd and cmd not in ["again"] and not cmd.startswith("history"):
            _last_executed_command = cmd

        handle_command(cmd)

def handle_command(cmd):
        global _macro_recording_name, _macro_recording_commands, _last_executed_command

        if _dispatch_core(cmd):
            return

        if cmd == "again":
            if _last_executed_command:
                handle_command(_last_executed_command)
            else:
                print("No previous command to run.")
                speak("No previous command to run")
            return

        elif cmd.startswith("history"):
            parts = cmd.split()
            limit = 20
            if len(parts) == 2:
                limit = parts[1]
            commands = get_recent_commands(limit)
            if not commands:
                commands = load_previous_session_commands(limit)
            if not commands:
                print("No command history found.")
                speak("No command history found")
                return
            print("Recent commands:")
            for i, cc in enumerate(commands, start=1):
                print(f"{i}. {cc}")
            return

        elif cmd == "help" or cmd.startswith("help "):
            keyword = cmd.replace("help", "", 1).strip()
            print(_format_help(keyword if keyword else None))
            speak("Showing help")
            return

        elif cmd.startswith("macro record"):
            parts = cmd.split(maxsplit=2)
            if len(parts) < 3 or not parts[2].strip():
                print("Usage: macro record <name>")
                speak("Usage macro record name")
                return
            _macro_recording_name = parts[2].strip()
            _macro_recording_commands = []
            print(f"Recording macro { _macro_recording_name }. Type commands, then run: macro stop")
            speak("Macro recording started")
            return

        elif cmd in ["macro stop", "macro cancel"]:
            if not _macro_recording_name:
                print("No macro recording in progress.")
                speak("No macro recording in progress")
                return
            name = _macro_recording_name
            commands = list(_macro_recording_commands)
            _macro_recording_name = None
            _macro_recording_commands = []
            if cmd == "macro cancel":
                print(f"Macro recording { name } canceled.")
                speak("Macro recording canceled")
                return
            save_macro(name, commands)
            print(f"Saved macro { name } with {len(commands)} commands.")
            speak("Macro saved")
            return

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
             print(_format_help(None))
             speak("Showing commands")
        
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
        
        elif "explain me " in cmd:
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
                if _confirm_action("This will type automatically. Proceed?"):
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
                print("macro <name> [--repeat N]")
                print("macro record <name>")
                print("macro stop")
    
            elif parts[1] == "list":
                list_macros()

            elif parts[1] == "show" and len(parts) == 3:
                show_macro(parts[2])

            elif len(parts) >= 2:
                name = parts[1]
                repeat = 1
                if "--repeat" in parts:
                    try:
                        idx = parts.index("--repeat")
                        repeat = parts[idx + 1]
                    except Exception:
                        repeat = 1
                run_macro(name, handle_command, repeat=repeat)

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
        
        elif cmd == "practical c" or cmd == "c practical":
            write_c_boilerplate()
        
        elif cmd.startswith("practical"):
            parts = cmd.split()

            if len(parts) == 1:
                reply = "Usage: practical add <num> | practical done <num> | practical list | practical status"
                print(reply)
                speak(reply)
                return

            if parts[1] == "add" and len(parts) == 3:
                add_practical(parts[2])

            elif parts[1] == "done" and len(parts) == 3:
                mark_done(parts[2])

            elif parts[1] == "list":
                list_practicals()

            elif parts[1] == "status":
                practical_status()

            else:
                reply = "Invalid practical command."
                print(reply)
                speak(reply)

        elif cmd == "command center":
            run_command_center()
        
        elif "create a project" in cmd or "project creator" in cmd or "draco project" in cmd:
            project_gen()
        
        elif "explain last project" in cmd or "explain this project" in cmd:
            explain_last_project()
        
        elif cmd.startswith("syllabus"):
            parts = cmd.split()

            if len(parts) == 1 or parts[1] == "list":
                syllabus_list()

            elif parts[1] == "show" and len(parts) >= 3:
                syllabus_show(" ".join(parts[2:]))

            elif parts[1] == "search" and len(parts) >= 3:
                syllabus_search(" ".join(parts[2:]))

            else:
                print("Invalid syllabus command.")
                speak("Invalid syllabus command.")
        
        elif cmd == "generate questions":
            generate_questions()
 
        elif cmd == "train skill":
            train_skill()
        
        elif cmd == "train notes":
            train_notes()
        
        elif cmd == "show weak":
            show_weak()
        
        elif cmd == "clear weak":
            clear_weak()
        
        elif cmd == "save notes":
            save_notes()

        elif cmd.startswith("create folder"):
            name = cmd.replace("create folder", "").replace("named", "").strip()
            path = create_folder(name)
            print(f"Folder created: {path}")
            speak("Folder created")

        elif cmd.startswith("copy file"):
            name = cmd.replace("copy file to", "").strip()
            dest = create_folder(name)
            print(copy_clipboard_file(dest))

        elif cmd.startswith("move file"):
            name = cmd.replace("move file to", "").strip()
            dest = create_folder(name)
            print(move_clipboard_file(dest))

        elif "send file on whatsapp" in cmd:
            if _confirm_action("This will send a file on WhatsApp. Proceed?"):
                print(send_clipboard_file_whatsapp())
        
        elif cmd.startswith("send file to"):
            if _confirm_action("This will send a file on WhatsApp. Proceed?"):
                print(send_file_to_contact(cmd))

        elif cmd == "speak hindi":
            state.LANGUAGE = "hindi"
            speak("Hindi mode activated")

        elif cmd == "speak marathi":
            state.LANGUAGE = "marathi"
            speak("Marathi mode activated")

        elif cmd == "speak english":
            state.LANGUAGE = "english"
            speak("English mode activated")
        
        elif cmd == "draco identity":
            print("\nDraco CLI | System Identity\n")
            speak("\nDraco CLI | System Identity\n")
            print("Core Type: Modular Command Line Assistant")
            speak("Core Type: Modular Command Line Assistant")
            print("Primary Role: Automation + AI + Workflow Optimization\n")
            speak("Primary Role: Automation + AI + Workflow Optimization\n")
            print("Active Systems:")
            speak("Active Systems:")
            print("• AI Engine: Online")
            speak("• AI Engine: Online")
            print("• Voice Engine: Ready")
            speak("• Voice Engine: Ready")
            print("• Language Mode: English")
            speak("• Language Mode: English")
            print("• Automation Modules: Loaded\n")
            speak("• Automation Modules: Loaded\n")
            print("Operational Focus:")
            speak("Operational Focus:")
            print("Assisting with productivity, automation, learning, and system tasks.\n")
            speak("Assisting with productivity, automation, learning, and system tasks.\n")
            print("Status:")
            speak("Status:")
            print("All systems functioning normally\n")
            speak("All systems functioning normally\n")

        else:
            suggestions = _suggest_command(cmd)
            if suggestions:
                print("Command not recognized.")
                print("Did you mean:")
                for s in suggestions:
                    print(f"- {s}")
                speak("Command not recognized")
                return
            reply = fallback(cmd)
            print(reply)
            speak(reply)
