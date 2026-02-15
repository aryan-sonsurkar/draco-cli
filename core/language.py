from modules.Ollama.ollama_helper import ask_ollama
import core.state as state


def translate(text):
    if state.LANGUAGE == "english":
        return text

    target = state.LANGUAGE

    translated = ask_ollama(f"""
Translate the following text to {target}.
Return only translated text.

{text}
""")

    if not translated:
        return text

    cleaned = translated.strip()

    if cleaned.lower() in ["none", "null", ""]:
        return text

    return cleaned

