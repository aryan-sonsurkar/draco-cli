import os
import re
import json
import subprocess
import sys

try:
    from modules.Ollama.ollama_helper import ask_ollama
except Exception:
    ask_ollama = None


GAMES_DIR = os.path.join("generated_games")


def _slugify(name):
    name = (name or "").strip().lower()
    name = re.sub(r"[^a-z0-9_\- ]+", "", name)
    name = re.sub(r"\s+", "-", name).strip("-")
    return name or "game"


def list_games():
    if not os.path.exists(GAMES_DIR):
        return []
    names = []
    for d in os.listdir(GAMES_DIR):
        p = os.path.join(GAMES_DIR, d)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "main.py")):
            names.append(d)
    return sorted(names)


def run_game(name):
    name = _slugify(name)
    game_path = os.path.join(GAMES_DIR, name, "main.py")
    if not os.path.exists(game_path):
        print("Game not found.")
        return
    subprocess.run([sys.executable, game_path], check=False)


def _default_game_code(idea):
    idea = idea.strip() if idea else "a simple terminal game"
    return (
        "def main():\n"
        f"    print('Welcome! Idea: {idea.replace("'", "\\'")}')\n"
        "    print('This is a generated terminal game skeleton.')\n"
        "    print('Type quit to exit.')\n"
        "    while True:\n"
        "        cmd = input('> ').strip().lower()\n"
        "        if cmd in ['quit','exit','q']:\n"
        "            print('Goodbye!')\n"
        "            return\n"
        "        print('You typed:', cmd)\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )


def make_game(idea, name=None):
    if not idea:
        print("Please provide a game idea.")
        return None

    os.makedirs(GAMES_DIR, exist_ok=True)

    folder_name = _slugify(name or idea.split(" ")[0])
    game_dir = os.path.join(GAMES_DIR, folder_name)
    os.makedirs(game_dir, exist_ok=True)

    code = None
    if ask_ollama is not None:
        prompt = (
            "Generate a single-file Python terminal game. Requirements:\n"
            "- Only use Python standard library\n"
            "- Must be runnable as main.py\n"
            "- Must include a main() function\n"
            "- No external dependencies\n"
            "- Game should match this idea: "
            + idea
            + "\nReturn ONLY the Python code." 
        )
        try:
            code = ask_ollama(prompt)
        except Exception:
            code = None

    if not code or "def main" not in code:
        code = _default_game_code(idea)

    main_file = os.path.join(game_dir, "main.py")
    with open(main_file, "w", encoding="utf-8") as f:
        f.write(code)

    meta = {
        "name": folder_name,
        "idea": idea,
    }
    with open(os.path.join(game_dir, "game.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Game created: {folder_name}")
    print(f"Run: game run {folder_name}")
    return folder_name
