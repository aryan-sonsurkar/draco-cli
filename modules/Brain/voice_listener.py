import speech_recognition as sr
from core.tts import speak

def listen_cmd(timeout=10):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening...")
        speak("Listening")

        r.adjust_for_ambient_noise(source,duration=0.5)

        try:
            audio = r.listen(source,timeout=timeout)
            text = r.recognize_google(audio)
            return text.lower()
        
        except Exception:
            return "...."