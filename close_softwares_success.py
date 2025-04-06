import os
import psutil
from fuzzywuzzy import process as fuzz_process
from data import engine, speak
from data import apps

def close_app(query):
    query = query.lower()
    print(f"Received command to close: {query}")

    # Fuzzy match against app names
    best_match, score = fuzz_process.extractOne(query, apps.keys())

    if score > 80:
        app_path = apps[best_match]
        exe_name = os.path.basename(app_path)  # Extracts only the executable name

        closed_any = False

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == exe_name.lower():
                    os.system(f"taskkill /F /PID {proc.info['pid']}")
                    closed_any = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        if closed_any:
            print(f"All instances of {best_match} are closed.")
            speak(f"All instances of {best_match} are closed")
        else:
            print(f"{best_match} is not running.")
            speak(f"{best_match} is not running")
    else:
        print("Application not found. Please try again.")
        speak("Application not found. Please try again.")

# close_app("close whatsapp")  # Example usage