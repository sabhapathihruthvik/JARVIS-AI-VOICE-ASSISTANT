# data.py
import pyttsx3

# 🎙️ Initialize text-to-speech
engine = pyttsx3.init()
def speak(text):
    """Speaks the given text aloud."""
    engine.say(text)
    engine.runAndWait()
# Contact list
contacts = {
    "name":"91phonenumber"
}

# Contact List
EMAIL_CONTACTS = {
   "name":"email address"
}

apps = {
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "docker": "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "vlc": "D:\\EDGE DOWNLOADS\\VLC\\vlc.exe",
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
    "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
    "file explorer": "explorer.exe",
    "task manager": "C:\\Windows\\System32\\Taskmgr.exe",
    "command prompt": "cmd.exe",
    "powershell": "powershell.exe",
    "control panel": "C:\\Windows\\System32\\control.exe",
    "settings": "ms-settings:",
    "paint": "mspaint.exe",
    "snipping tool": "C:\\Windows\\System32\\SnippingTool.exe",
    "wordpad": "C:\\Program Files\\Windows NT\\Accessories\\wordpad.exe",
    "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
    "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "opera": "C:\\Users\\YourUser\\AppData\\Local\\Programs\\Opera\\launcher.exe",
    "brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
    "visual studio code": "C:\\Users\\YourUser\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "android studio": "C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe",
    "windows media player": "C:\\Program Files\\Windows Media Player\\wmplayer.exe",
    "whatsapp": "C:\\Users\\YourUser\\AppData\\Local\\WhatsApp\\WhatsApp.exe"

}

WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "wikipedia": "https://www.wikipedia.org",
    "stackoverflow": "https://stackoverflow.com",
    "linkedin": "https://www.linkedin.com",
    "gmail": "https://mail.google.com",
    "netflix": "https://www.netflix.com",
    "amazon": "https://www.amazon.com",
    "facebook": "https://www.facebook.com"
}

# Paths for music and movies
MUSIC_FOLDER = "C:\\Users\\Asus\\OneDrive\\Music"
MOVIE_FOLDER = "C:\\Users\\Asus\\OneDrive\\Videos\\Movies"

# Player paths
MEDIA_PLAYER = "C:\\Program Files\\Windows Media Player\\wmplayer.exe"
VLC_PLAYER = "D:\\EDGE DOWNLOADS\\VLC\\vlc.exe"

