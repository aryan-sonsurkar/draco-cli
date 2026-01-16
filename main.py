import os
from core.commands import command_prompt
from core.tts import speak

def main():
    print("----------------------")
    print("Welcome to Draco CLI")
    print("----------------------")

    command_prompt()

if __name__=="__main__":
    main()