import subprocess

def fallback(cmd):
    prompt = f"""You are draco, a terminal-based assistant. Answer briefly, terminal-styl, no emojis.
    User input:
    {cmd}
    """
    result = subprocess.run(
        ["ollama","run","llama3"],
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="ignore",
        capture_output=True
    )
    return result.stdout.strip()