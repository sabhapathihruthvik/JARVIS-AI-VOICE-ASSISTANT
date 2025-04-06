
import subprocess
import time
import pyautogui
import pyttsx3
from fuzzywuzzy import process
from data import speak, engine, contacts

# Initialize text-to-speech engine

engine.setProperty('rate', 150)



def get_correct_contact(name):
    """Matches user input with the closest contact name using fuzzy matching."""
    best_match = process.extractOne(name, contacts.keys(), score_cutoff=75)  # Adjust cutoff if needed
    if best_match:
        print(f"Best match for '{name}': {best_match[0]} with score {best_match[1]}")
        return best_match[0], contacts[best_match[0]]
    return None, None

def extract_call_details(query):
    """
    Extracts the recipient's name and call type (voice or video) from the given query.
    Returns the contact name, phone number, and call type.
    """
    query = query.lower()
    words = query.split()
    recipient_name = None
    call_type = None

    # Identify call type (voice or video)
    if "video call" in query or "video" in query:
        call_type = "video"
    elif "voice call" in query or "call" in query:
        call_type = "voice"

    # Identify possible recipient name
    for word in words:
        match, number = get_correct_contact(word)
        if match:
            recipient_name = match
            return recipient_name, contacts[recipient_name], call_type

    return None, None, None

def whatsapp_video_call(query):
    """Extracts recipient details and initiates a WhatsApp video call."""
    recipient_name, phone, call_type = extract_call_details(query)

    if recipient_name and phone:
        speak(f"Starting a video call with {recipient_name}.")

        # Open WhatsApp chat with the given phone number
        whatsapp_url = f"whatsapp://send?phone={phone}"
        full_command = f'start "" "{whatsapp_url}"'

        subprocess.run(full_command, shell=True)
        time.sleep(4)  # Wait for WhatsApp to fully load the chat

        # Press Tab 10 times to reach the video call button
        for _ in range(10):
            pyautogui.press("tab")
            time.sleep(0.02)  # Small delay between key presses

        # Press Enter to start the video call
        pyautogui.press("enter")
    else:
        speak("Sorry, I couldn't determine the contact.")

def whatsapp_call(query):
    """Extracts recipient details and initiates a WhatsApp voice call."""
    recipient_name, phone, call_type = extract_call_details(query)

    if recipient_name and phone:
        speak(f"Calling {recipient_name} via WhatsApp.")

        whatsapp_url = f"whatsapp://call?phone={phone}"
        full_command = f'start "" "{whatsapp_url}"'

        subprocess.run(full_command, shell=True)
        time.sleep(5)
    else:
        speak("Sorry, I couldn't determine the contact.")

