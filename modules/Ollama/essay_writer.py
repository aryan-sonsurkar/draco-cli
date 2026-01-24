import subprocess

def essay_writer(cmd):
    cmd = cmd.replace("create an essay on","")
    prompt = (
        f"Write a simple 400 words essay on the given topic.Don't add extra text just give me essay as output .The topic is {cmd}"
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