import subprocess

def analyze(cmd):
    if "think" in cmd:
        situation = cmd.replace("think","").strip()
    
    if "analyze" in cmd:
        situation = cmd.replace("analyze","").strip()
    
    prompt =(
        f"Analyze the given situation logically.Give short,structred reasoning.No extra text only display the output.Answer should have a career growth.The situation is {situation} Keep the answer short and no special symbols in answer. "
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
