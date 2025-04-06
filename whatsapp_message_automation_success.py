import subprocess
import time
from urllib.parse import quote
import pyttsx3
import pyautogui
from fuzzywuzzy import process  # For handling spelling mistakes
from data import contacts, speak, engine


engine.setProperty('rate', 150)


def get_correct_contact(query):
    """Matches full input against contact names with improved fuzzy matching."""
    best_match = process.extractOne(query, contacts.keys(), score_cutoff=80)  # Higher cutoff to avoid wrong matches
    if best_match:
        print(f"Best match for '{query}': {best_match[0]} with score {best_match[1]}")
        return best_match[0], contacts[best_match[0]]
    return None, None

def whatsapp_message(query):
    """
    Takes a voice command (query) as input, extracts recipient and message, 
    sends a WhatsApp message, and then closes WhatsApp.
    """
    words = query.split()
    recipient_name = None
    message = None

    # Identify recipient by extracting the best matching full phrase
    for i in range(len(words)):
        partial_name = " ".join(words[:i+1])  # Try matching from the start of the query
        match, number = get_correct_contact(partial_name)
        if match:
            recipient_name = match
            message = " ".join(words[i+1:])  # Remaining words after name form the message
            break

    if not recipient_name:
        speak("Sorry, I couldn't determine the contact.")
        return

    if not message.strip():
        speak("Message is empty. Please provide a message.")
        return

    phone = contacts[recipient_name]
    whatsapp_url = f"whatsapp://send?phone={phone}&text={quote(message)}"
    full_command = f'start "" "{whatsapp_url}"'

    try:
        # Open WhatsApp
        subprocess.run(full_command, shell=True)
        time.sleep(3)  # Wait for WhatsApp to load
        
        pyautogui.press("enter")  # Send the message
        time.sleep(2)  # Wait for it to be sent

        # Close WhatsApp
        pyautogui.hotkey("alt", "f4")
        speak("Message sent.")

    except Exception as e:
        speak(f"Error sending message: {str(e)}")


# whatsapp_message("Send a message to amma saying hello")  # Example usage



# import subprocess
# import time
# from urllib.parse import quote
# import pyttsx3
# import pyautogui
# import speech_recognition as sr
# from fuzzywuzzy import process  # To handle spelling mistakes

# # Contact list
# contacts = {
#     "amma": "918639194136",
#     "appa": "919515042801",
#     "sumanth": "916300147979",
#     "dubba dayyam": "917780593512",
#     "paavanam": "919182866646",
#     "sushanth": "919177961089"
# }

# # Initialize text-to-speech engine
# engine = pyttsx3.init()
# engine.setProperty('rate', 150)

# ef speak(text):
#     """Speaks the given text and prints it."""
#     print(f"Jarvis: {text}")
#     engine.say(text)
#     engine.runAndWait()

# def recognize_speech():
#     """Uses speech recognition to capture user input."""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         speak("I am listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         try:
#             audio = recognizer.listen(source)
#             query = recognizer.recognize_google(audio).lower()
#             print(f"You said: {query}")
#             return query
#         except sr.UnknownValueError:
#             speak("Sorry, I couldn't understand. Please repeat.")
#             return None
#         except sr.RequestError:
#             speak("Speech recognition service is unavailable.")
#             return None

# def get_correct_contact(name):
#     """Matches user input with the closest contact name using fuzzy matching."""
#     best_match = process.extractOne(name, contacts.keys(), score_cutoff=70)  # Adjust cutoff if needed
#     if best_match:
#         return best_match[0], contacts[best_match[0]]
#     return None, None

# def extract_details(query):
#     """Extracts the recipient's name and message from the spoken query."""
#     words = query.split()
#     recipient_name = None
#     message_start_index = None

#     for i, word in enumerate(words):
#         # Identify possible recipient name
#         match, number = get_correct_contact(word)
#         if match:
#             recipient_name = match
#             message_start_index = i + 1
#             break  # Stop once a match is found

#     if recipient_name and message_start_index:
#         message = " ".join(words[message_start_index:])
#         return recipient_name, contacts[recipient_name], message
#     return None, None, None

# def send_whatsapp_message(phone, message, name):
#     """Sends a WhatsApp message and presses Enter automatically."""
#     whatsapp_url = f"whatsapp://send?phone={phone}&text={quote(message)}"
#     full_command = f'start "" "{whatsapp_url}"'
    
#     subprocess.run(full_command, shell=True)
#     time.sleep(3)  # Allow WhatsApp to open fully
    
#     pyautogui.press("enter")  # Press Enter to send the message
    
#     speak(f"Message sent successfully to {name}.")

# # Main function
# def main():
#     #speak("Hello! How can I assist you with WhatsApp messaging?")
    
#     while True:
#         query = recognize_speech()
#         if not query:
#             continue
        
#         recipient_name, phone, message = extract_details(query)

#         if recipient_name and phone and message:
#             send_whatsapp_message(phone, message, recipient_name)
#         else:
#             speak("Sorry, I couldn't determine the contact or message.")

#         speak("Do you want to send another message?")
#         confirmation = recognize_speech()
#         if confirmation and "quit" in confirmation:
#             speak("Okay, shutting down.")
#             break

# if __name__ == "__main__":
#     main()
