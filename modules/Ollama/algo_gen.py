import subprocess

def algo_gen(cmd):
    cmd = cmd.replace("write algorithm for","")
    prompt = (
        f"Write algorithm for the given topic.No extra text only output algorithm.The topic is {cmd}"
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