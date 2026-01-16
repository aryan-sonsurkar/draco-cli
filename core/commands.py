from core.tts import speak

def command_prompt():
    while True:
        cmd = input("Enter your command: \n")
        cmd = cmd.lower()

        if cmd=="who are you":
            reply = "I am Draco CLI. A project made for automating tasks."
            print(reply)
            speak(reply)
        
        elif cmd=="who created you":
            reply = "My master Aryan Sonsurkar created me to learn python deeply and automate his tasks."
            print(reply)
            speak(reply)

        elif cmd=="exit":
            reply = "Goodbye Bro!!!"
            print(reply)
            speak(reply)
            break

        else:
            print("This is command is not available.")