import os

def main():
    print("----------------------")
    print("Welcome to Draco CLI")
    print("----------------------")
    
    while True:
        cmd = input("Enter your command: \n")

        if cmd=="Who are you":
            print("I am Draco CLI. A project made for automate tasks.")
        
        elif cmd=="Who created you":
            print("My master Aryan Sonsurkar created me to learn python deeply and automate his tasks.")

        elif cmd=="Exit":
            print("Goodbye Bro!!!")
            break

        else:
            print("This is not in cmd list!!!")

if __name__=="__main__":
    main()