import os
import subprocess
import time
import pyautogui
import pyttsx3
import webbrowser
from fuzzywuzzy import process
from data import apps, WEBSITES
from data import speak, engine  # Assuming you defined engine/speak in data.py
# Initialize text-to-speech engine



def open_mysql():
    try:
        print("Opening MySQL...")
        engine.say("Opening MySQL")
        engine.runAndWait()

        # Open the terminal
        subprocess.Popen("start cmd", shell=True)
        time.sleep(2.5)  # Wait for the terminal to open and become active

        
        time.sleep(1)

        # Type the MySQL login command
        pyautogui.typewrite('mysql -u root -P 3306 -h localhost -p', interval=0.005)
        pyautogui.press('enter')
        time.sleep(1)

        # Type the password (you may want to hide this securely)
        pyautogui.typewrite('7894561230', interval=0.05)
        pyautogui.press('enter')

    except Exception as e:
        print(f"Failed to open MySQL: {e}")
        engine.say("Failed to open MySQL")
        engine.runAndWait()

def opening_apps_and_websites(query):

    query = query.lower()

    # Special handling for MySQL
    if "mysql" in query or "my sql" in query or "sql" in query:
        open_mysql()
        return

    best_app, app_score = process.extractOne(query, apps.keys())
    best_web, web_score = process.extractOne(query, WEBSITES.keys())

    if max(app_score, web_score) < 70:
        print("No suitable application or website found.")
        engine.say("No suitable application or website found.")
        engine.runAndWait()
        return

    try:
        if app_score >= web_score:
            print(f"Opening application: {best_app}")
            engine.say(f"Opening {best_app}")
            engine.runAndWait()

            if apps[best_app].startswith("ms-settings:"):
                subprocess.Popen(['start', apps[best_app]], shell=True)
            else:
                os.startfile(apps[best_app])
        else:
            print(f"Opening website: {best_web}")
            engine.say(f"Opening {best_web}")
            engine.runAndWait()
            webbrowser.open(WEBSITES[best_web])
    except Exception as e:
        print(f"Error while opening: {e}")
        engine.say("An error occurred while trying to open")
        engine.runAndWait()


# # Example input
# # open_apps_and_websites("Launch exel")
# open_apps_and_websites("Open youtub")
# opening_apps_and_websites("Start whatsapp")
# open_apps_and_websites("Open my sql")

