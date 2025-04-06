import psutil
import pyttsx3
from data import speak, engine

def battery_status(query=None):
    battery = psutil.sensors_battery()
    if battery is None:
        speak("Sorry, I couldn't access battery information.")
        return

    percent = battery.percent
    plugged = battery.power_plugged

    status_msg = f"Your battery is at {percent} percent."
    if plugged:
        status_msg += " It's currently charging."
    elif percent < 20:
        status_msg += " You should consider plugging it in soon."

    speak(status_msg)

