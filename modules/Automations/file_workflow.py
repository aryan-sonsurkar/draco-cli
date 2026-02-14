import os
import shutil
import time
import subprocess
import pyperclip
import pyautogui


def get_clipboard_file():
    data = pyperclip.paste()

    if not data:
        return None

    data = data.strip().strip('"').strip("'")

    if os.path.exists(data):
        return data

    return None



def create_folder(folder_name, base_path=None):
    if base_path is None:
        base_path = os.getcwd()

    path = os.path.join(base_path, folder_name)

    if not os.path.exists(path):
        os.makedirs(path)

    return path


def copy_clipboard_file(destination_folder):
    file_path = get_clipboard_file()

    if not file_path:
        return "No file found in clipboard."

    shutil.copy(file_path, destination_folder)
    return f"File copied to {destination_folder}"


def move_clipboard_file(destination_folder):
    file_path = get_clipboard_file()

    if not file_path:
        return "No file found in clipboard."

    shutil.move(file_path, destination_folder)
    return f"File moved to {destination_folder}"


def open_whatsapp():
    try:
        os.startfile("whatsapp:")
        time.sleep(5)
        return True
    except:
        return False

def send_clipboard_file_whatsapp():
    file_path = get_clipboard_file()

    if not file_path:
        return "No file found in clipboard."

    if not open_whatsapp():
        return "WhatsApp not found."

    time.sleep(3)

    attach_btn = pyautogui.locateCenterOnScreen("assets/whatsapp_attach.png")

    if not attach_btn:
        return "Attach button not detected."

    pyautogui.click(attach_btn)
    time.sleep(1)

    document_btn = pyautogui.locateCenterOnScreen("assets/whatsapp_document.png")

    if not document_btn:
        return "Document button not detected."

    pyautogui.click(document_btn)
    time.sleep(2)

    pyperclip.copy(file_path)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)

    pyautogui.press("enter")
    time.sleep(2)

    pyautogui.press("enter")

    return "File sent via WhatsApp."

import json

CONTACTS_FILE = "data/contacts.json"


def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []

    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def resolve_contact(user_input):
    user_input = user_input.lower()

    contacts = load_contacts()

    for contact in contacts:
        for alias in contact.get("aliases", []):
            if alias in user_input:
                return contact

    return None


def open_chat(contact_name):
    time.sleep(2)

    pyautogui.hotkey("ctrl", "f")
    time.sleep(1)

    pyautogui.write(contact_name)
    time.sleep(1)

    pyautogui.press("enter")
    time.sleep(2)


def send_file_to_contact(user_command):
    file_path = get_clipboard_file()

    if not file_path:
        return "No file found in clipboard."

    contact = resolve_contact(user_command)

    if not contact:
        return "Contact not found."

    if not open_whatsapp():
        return "WhatsApp not found."

    search_name = contact["whatsapp_search"]

    open_chat(search_name)

    attach_btn = pyautogui.locateCenterOnScreen("assets/whatsapp_attach.png")

    if not attach_btn:
        return "Attach button not detected."

    pyautogui.click(attach_btn)
    time.sleep(1)

    document_btn = pyautogui.locateCenterOnScreen("assets/whatsapp_document.png")

    if not document_btn:
        return "Document button not detected."

    pyautogui.click(document_btn)
    time.sleep(2)

    pyperclip.copy(file_path)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)

    pyautogui.press("enter")
    time.sleep(2)

    pyautogui.press("enter")

    return f"File sent to {contact['name']}"