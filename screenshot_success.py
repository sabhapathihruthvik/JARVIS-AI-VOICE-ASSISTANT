import pyautogui
import datetime
import os
from data import engine, speak  # Assuming you defined engine/speak in data.py
def take_screenshot(query=None):
    """Takes a screenshot and saves it in the OneDrive Screenshots folder with a timestamp."""
    # Define the target folder
    save_dir = r"C:\Users\Asus\OneDrive\Pictures\Screenshots"

    # Create folder if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Create a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)

    # Take screenshot and save
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    print(f"📸 Screenshot saved at: {filepath}")
    speak(f"📸 Screenshot saved")
    return filepath


# take_screenshot()
