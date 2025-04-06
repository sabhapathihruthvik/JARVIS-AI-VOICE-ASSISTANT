import os
import random
import subprocess   
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from time import sleep
import screen_brightness_control as sbc
from data import MUSIC_FOLDER, MOVIE_FOLDER, MEDIA_PLAYER, VLC_PLAYER




# Function to play a random music file
def play_music(query):
    if not os.path.exists(MUSIC_FOLDER):
        print("Music folder not found!")
        return
    
    music_files = [os.path.join(MUSIC_FOLDER, file) for file in os.listdir(MUSIC_FOLDER) if file.endswith(('.mp3', '.wav', '.flac'))]
    
    if not music_files:
        print("No music files found!")
        return
    
    song = random.choice(music_files)  # Pick a random song
    print(f"Playing music: {song}")
    subprocess.Popen([MEDIA_PLAYER, song], shell=True)

# Function to play a random movie file
def play_movie(query):
    if not os.path.exists(MOVIE_FOLDER):
        print("Movie folder not found!")
        return
    
    movie_files = [os.path.join(MOVIE_FOLDER, file) for file in os.listdir(MOVIE_FOLDER) if file.endswith(('.mp4', '.mkv', '.avi'))]
    
    if not movie_files:
        print("No movie files found!")
        return
    
    movie = random.choice(movie_files)  # Pick a random movie
    print(f"Playing movie: {movie}")
    subprocess.Popen([VLC_PLAYER, movie], shell=True)

# Function to stop music by closing all instances of Windows Media Player
def stop_music(query):
    os.system("taskkill /IM wmplayer.exe /F")
    print("Music stopped (Windows Media Player closed).")

# Function to stop movie by closing all instances of VLC Player
def stop_movie(query):
    os.system("taskkill /IM vlc.exe /F")
    print("Movie stopped (VLC closed).")

def shutdown(query):
    try:
        print("Shutting down the system...")
        os.system("shutdown /s /t 1")  # /s = shutdown, /t 1 = wait 1 sec
    except Exception as e:
        print(f"Error shutting down: {e}")

def restart(query):
    try:
        print("Restarting the system...")
        os.system("shutdown /r /t 1")  # /r = restart, /t 1 = wait 1 sec
    except Exception as e:
        print(f"Error restarting: {e}")

def increase_brightness(query=None):
    try:
        # Get the current brightness level
        current = sbc.get_brightness(display=0)[0]
        new_brightness = min(current + 20, 100)  # Increase by 20%, cap at 100%

        # Set new brightness
        sbc.set_brightness(new_brightness, display=0)
        print(f"Brightness increased to {new_brightness}%")

    except Exception as e:
        print(f"Error increasing brightness: {e}")

def decrease_brightness(query=None):
    try:
        # Get the current brightness level
        current = sbc.get_brightness(display=0)[0]
        new_brightness = max(current - 15, 0)  # Decrease by 15%, floor at 0%

        # Set new brightness
        sbc.set_brightness(new_brightness, display=0)
        print(f"Brightness decreased to {new_brightness}%")

    except Exception as e:
        print(f"Error decreasing brightness: {e}")

def increase_volume(query):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(current_volume + 0.20, 1.0)  # Increase by 20%, cap at 100%
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    print(f"Volume increased to {int(new_volume * 100)}%")

def decrease_volume(query):

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(current_volume - 0.15, 0.0)  # Decrease by 15%, floor at 0%
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    print(f"Volume decreased to {int(new_volume * 100)}%")


# play_music("Play some music")
# stop_music("Stop the music")
# play_movie("Play a movie")
# sleep(5)  # Wait for 5 seconds before stopping
# stop_movie("Stop the movie")