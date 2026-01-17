import webbrowser
from core.tts import speak

def web_commands(cmd):
    if cmd=="open chatgpt":
        reply = "Opening ChatGPT"
        print(reply)
        speak(reply)
        webbrowser.open("https://chatgpt.com")
    
    elif cmd=="open github":
        reply = "Opening GitHub ,Bro commit well!"
        print(reply)
        speak(reply)
        webbrowser.open("https://github.com")
        
    else:
        reply ="Sorry i can't open it"
        print(reply)
        speak(reply)