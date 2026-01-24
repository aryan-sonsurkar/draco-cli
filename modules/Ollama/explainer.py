import subprocess

def explainer(cmd):
    cmd = cmd.replace("explain","")
    prompt = (
        f"Explain the given topic like i'm 5.Only output explaination no extra text.The topic is {cmd}"
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

def motivater():
    prompt = (
        "Give 2-line disciplined,no cringe motivation pure coder motivation.No extra text output only those lines."
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