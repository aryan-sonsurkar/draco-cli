import subprocess

def generate_calculator_code(cmd):
    prompt = (
        "Write a simple calculator program in python. It should take two numbers from the user ans allow +,-,*,/. Keep the code beggineer friendly and clean. Only give the code, no explanation."
    )
    result = subprocess.run(
        ["ollama","run","llama3"],
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="ignore",
        capture_output=True
    )
    return result.stdout.strip()

def solve_calculator(cmd):
    result = subprocess.run(
        ["ollama","run","llama3"],
        input=cmd,
        text=True,
        encoding="utf-8",
        errors="ignore",
        capture_output=True
    )
    return result.stdout.strip()