import asyncio
import edge_tts
import tempfile
import os
from playsound import playsound
from core.language import translate
from core import state

VOICE_MAP = {
    "english": "en-US-GuyNeural",
    "hindi": "hi-IN-MadhurNeural",
    "marathi": "hi-IN-MadhurNeural"
}

async def _speak_async(text):
    if not text:
        return

    translated = translate(text)

    voice = VOICE_MAP.get(state.LANGUAGE, VOICE_MAP["english"])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        temp_path = f.name

    try:
        communicate = edge_tts.Communicate(translated, voice)
        await communicate.save(temp_path)
        playsound(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def speak(text):
    try:
        asyncio.run(_speak_async(text))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_speak_async(text))
