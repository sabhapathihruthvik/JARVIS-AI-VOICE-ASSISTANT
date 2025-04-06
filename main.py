import pyttsx3
import joblib
import speech_recognition as sr
from fuzzywuzzy import fuzz

# Intent Handler Imports
from close_softwares_success import close_app
from device_controls_success import play_music, play_movie, stop_music, stop_movie, shutdown, restart, increase_brightness, decrease_brightness, increase_volume, decrease_volume
from opening_apps_and_websites import opening_apps_and_websites
from email_aut_success import write_email
from search_in_yt_success import search_youtube
from whatsapp_message_automation_success import whatsapp_message
from whatsapp_calls_automation_success import whatsapp_call, whatsapp_video_call
from weathernews_success import weather
from show_news_success import show_news
from web_search_success import web_search
from llm_query_success import llm_query
from screenshot_success import take_screenshot
from time_and_date_success import get_time_date
from show_battery_status import battery_status
from calendar_helper_success import calendar_helper
from store_memory import memory_feature
from spelling_success import spell_word_handler

# ---------------------------
# Text-to-Speech
# ---------------------------
engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------------------
# Load the Intent Recognition Model
# ---------------------------
model = joblib.load("intent_recognition_model.pkl")

# ---------------------------
# Wake Word Config
# ---------------------------
WAKE_WORD = "jarvis"
FUZZY_THRESHOLD = 80

def detect_wake_word(text):
    words = text.lower().split()
    for i, word in enumerate(words):
        if fuzz.ratio(word, WAKE_WORD) >= FUZZY_THRESHOLD:
            remaining = ' '.join(words[i+1:])
            return True, remaining
    return False, None

# ---------------------------
# Process Command
# ---------------------------
def process_command(command):
    print(f"User Command: {command}")
    try:
        intent = model.predict([command])[0]
        print(f"Predicted Intent: {intent}")
        if intent in globals():
            globals()[intent](command)
        else:
            speak("Sorry, I don't know how to handle that command yet.")
    except Exception as e:
        speak("I couldn’t understand that command.")
        print("Error:", e)

# ---------------------------
# Main Loop
# ---------------------------
def listen_loop():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        speak("Jarvis is online. Say the wake word to activate.")

    while True:
        with mic as source:
            print("🎙️ Listening for wake word...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio).lower()
            print("Heard:", text)
            wake, rest = detect_wake_word(text)

            if wake:
                speak("Yes Boss")
                command_text = rest.strip()

                # If no command after wake word, listen again
                if not command_text:
                    # speak("Listening to your command.")
                    with mic as source:
                        audio = recognizer.listen(source, timeout=3, phrase_time_limit=7)
                    command_text = recognizer.recognize_google(audio).lower()
                    print("Command after prompt:", command_text)

                process_command(command_text)
            else:
                print("Wake word not detected.")

        except sr.WaitTimeoutError:
            print("⏳ Listening timed out.")
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
        except sr.RequestError as e:
            print(f"❗ API error: {e}")

# ---------------------------
# Run the Assistant
# ---------------------------
if __name__ == "__main__":
    listen_loop()




































# # ---------------------------
# # All Imports
# # ---------------------------
# import struct
# import pvporcupine
# import pyaudio
# import speech_recognition as sr
# import pyttsx3
# import joblib

# # Intent Handler Imports
# from close_softwares_success import close_app
# from device_controls_success import play_music, play_movie, stop_music, stop_movie, shutdown, restart, increase_brightness, decrease_brightness, increase_volume, decrease_volume
# from opening_apps_and_websites import opening_apps_and_websites
# from email_aut_success import write_email
# from search_in_yt_success import search_youtube
# from whatsapp_message_automation_success import whatsapp_message
# from whatsapp_calls_automation_success import whatsapp_call, whatsapp_video_call
# from weathernews_success import weather
# from show_news_success import show_news
# from web_search_success import web_search
# from llm_query_success import llm_query
# from screenshot_success import take_screenshot
# from time_and_date_success import get_time_date
# from show_battery_status import battery_status
# from calendar_helper_success import calendar_helper
# from store_memory import memory_feature
# from spelling_success import spell_word_handler

# # ---------------------------
# # Text-to-Speech Engine
# # ---------------------------
# engine = pyttsx3.init()

# def speak(text):
#     print(text)
#     engine.say(text)
#     engine.runAndWait()

# # Load the trained intent recognition model
# model_filename = "intent_recognition_model.pkl"
# model = joblib.load(model_filename)

# # ---------------------------
# # Command Listener
# # ---------------------------
# def listen_for_command():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening for your command...")
#         recognizer.adjust_for_ambient_noise(source)

#         try:
#             audio = recognizer.listen(source, timeout=5)
#             command = recognizer.recognize_google(audio)
#             print(f"Command: {command}")

#             # Predict intent
#             intent = model.predict([command])[0]
#             print(f"Predicted Intent: {intent}")

#             # Call the matching function
#             if intent in globals():
#                 globals()[intent](command)
#             else:
#                 speak("Sorry, I dooooon't know how to handle that command yet.")

#         except sr.UnknownValueError:
#             speak("Sorry, I couldn't understand that.")
#         except sr.RequestError:
#             speak("Error connecting to the speech recognition service.")
#         except sr.WaitTimeoutError:
#             speak("No command received, please try again.")

# # ---------------------------
# # Wake Word Detection
# # ---------------------------
# def hotword_detection():
#     porcupine = None
#     paud = None
#     audio_stream = None

#     try:
#         porcupine = pvporcupine.create(keywords=["jarvis"])
#         paud = pyaudio.PyAudio()
#         audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16,
#                                  input=True, frames_per_buffer=porcupine.frame_length)

#         print("Listening for wake word 'Jarvis'...")

#         while True:
#             audio_data = audio_stream.read(porcupine.frame_length)
#             audio_data = struct.unpack_from("h" * porcupine.frame_length, audio_data)

#             keyword_index = porcupine.process(audio_data)

#             if keyword_index >= 0:
#                 print("Wake word detected!")
#                 speak("Yes Boss")

#                 listen_for_command()
#                 print("Listening again for wake word 'Jarvis'...")

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         if porcupine is not None:
#             porcupine.delete()
#         if audio_stream is not None:
#             audio_stream.close()
#         if paud is not None:
#             paud.terminate()

# # ---------------------------
# # Start the Assistant
# # ---------------------------
# if __name__ == "__main__":
#     hotword_detection()
