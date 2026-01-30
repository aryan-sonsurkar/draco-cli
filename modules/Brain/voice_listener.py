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
            print(f"You said: {text} ")
            return text.lower()
        
        except sr.WaitTimeoutError:
            print("Listening timed out")
            speak("i didn't hear anything")
            return None
        
        except sr.UnknownValueError:
            print("Could not understand audio")
            speak("I couldn't understand that")
            return None
        
        except sr.RequestError:
            print("Speech service unavailable")
            speak("Speech service is unavailable")
            return None