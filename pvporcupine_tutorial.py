import struct
import time
import threading
import pvporcupine
import pyaudio
import speech_recognition as sr
import pyttsx3
import joblib
from data import speak, engine
# Load the trained intent recognition model
model_filename = "intent_recognition_model.pkl"
model = joblib.load(model_filename)


# Add more functions corresponding to your intents...

# ---------------------------
# Command Listener
# ---------------------------
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            speak(f"You said: {command}")

            # Predict intent
            intent = model.predict([command])[0]
            print(f"Predicted Intent: {intent}")

            # Execute intent function in a new thread
            if intent in globals():
                threading.Thread(target=globals()[intent], args=(command,)).start()
            else:
                speak("Sorry, I don't know how to handle that command yet.")

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
        except sr.RequestError:
            speak("Error connecting to the speech recognition service.")

# ---------------------------
# Wake Word Detection
# ---------------------------
def hotword_detection():
    porcupine = None
    paud = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(keywords=["jarvis"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16,
                                 input=True, frames_per_buffer=porcupine.frame_length)

        print("Listening for wake word 'Jarvis'...")

        while True:
            audio_data = audio_stream.read(porcupine.frame_length)
            audio_data = struct.unpack_from("h" * porcupine.frame_length, audio_data)

            keyword_index = porcupine.process(audio_data)

            if keyword_index >= 0:
                print("Wake word detected!")
                speak("Yes Boss")
                # Start listening in a new thread so main loop continues
                threading.Thread(target=listen_for_command).start()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()











































# import struct
# import time
# import pvporcupine
# import pyaudio
# import speech_recognition as sr
# import pyttsx3
# from data import speak, engine




# def listen_for_command():
#     """Listen for user speech after wake word detection and repeat it back."""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening for your command...")
#         recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
#         try:
#             audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
#             command = recognizer.recognize_google(audio)  # Convert speech to text
#             print(f"You said: {command}")
#             speak(f"You said: {command}")  # Repeat user's speech
#         except sr.UnknownValueError:
#             print("Sorry, I couldn't understand that.")
#             speak("Sorry, I couldn't understand that.")
#         except sr.RequestError:
#             print("Error connecting to speech recognition service.")
#             speak("Error connecting to speech recognition service.")

# def hotword_detection():
#     """Detects the wake word 'Jarvis' and listens for a command."""
#     porcupine = None
#     paud = None
#     audio_stream = None

#     try:
#         porcupine = pvporcupine.create(keywords=["jarvis"])  # Use "jarvis" as wake word
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
#                 speak("Yes Boss")  # Respond to wake word
#                 listen_for_command()  # Listen for user's speech after wake word detection

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         if porcupine is not None:
#             porcupine.delete()
#         if audio_stream is not None:
#             audio_stream.close()
#         if paud is not None:
#             paud.terminate()

# # Run the hotword detection
# hotword_detection()
