import requests
import re
import pyttsx3
from data import speak,engine
API_KEY = "ebdba9422b2c256d5f9d9d71231555ac"




def get_location():
    """Fetches the user's city based on their IP address."""
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        return data.get("city", "Unknown")
    except:
        return "Unknown"

def weather(query):
    """Fetches and presents the weather information for a given city."""
    try:
        # Extract city name from query
        city_match = re.search(r"in\s([\w\s]+)", query, re.IGNORECASE)
        city = city_match.group(1) if city_match else get_location()

        # Check if a valid city is found
        if city == "Unknown":
            message = "Could not determine your location. Please specify a city."
            print("🚫 " + message)
            speak(message)
            return

        # API endpoint for weather
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        # Fetch weather data
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            message = f"Could not find weather data for '{city}'."
            print("🚫 " + message)
            speak(message)
            return

        # Extract details
        temperature = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Present the results in an improved format
        weather_report = (
            f"📍 Weather Report for {city}:\n"
            f"🌤 Condition: {weather_desc}\n"
            f"🌡 Temperature: {temperature}°C\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬 Wind Speed: {wind_speed} m/s"
        )

        print(weather_report)
        
        # Speak the results out loud
        speak(f"The weather in {city} is {weather_desc}. "
              f"The temperature is {temperature} degrees Celsius. "
              f"The humidity is {humidity} percent, "
              f"and the wind speed is {wind_speed} meters per second.")
        return None

    except Exception as e:
        error_message = f"Error fetching weather: {e}"
        print("🚫 " + error_message)
        speak("Sorry, I couldn't retrieve the weather information.")
    return None


# weather("What's the weather like ?")




# import os
# import requests
# import speech_recognition as sr
# import pyttsx3
# import spacy

# # OpenWeatherMap API Key
# API_KEY = "ebdba9422b2c256d5f9d9d71231555ac"

# # Load spaCy model for Named Entity Recognition (NER)
# nlp = spacy.load("en_core_web_sm")

# # Initialize Text-to-Speech engine
# engine = pyttsx3.init()

# def speak(text):
#     """Convert text to speech."""
#     engine.say(text)
#     engine.runAndWait()

# def get_weather(city):
#     """Fetch weather data for the given city from OpenWeatherMap."""
#     base_url = "http://api.openweathermap.org/data/2.5/weather"
#     params = {
#         "q": city,
#         "appid": API_KEY,
#         "units": "metric"
#     }
    
#     response = requests.get(base_url, params=params)
    
#     if response.status_code == 200:
#         data = response.json()
#         temp = data['main']['temp']
#         weather = data['weather'][0]['description']
#         return f"The current temperature in {city} is {temp}°C with {weather}."
#     else:
#         return f"Sorry, I couldn't fetch the weather for {city}. Please check the city name."

# def extract_city(text):
#     """Extract city name using Named Entity Recognition (NER)."""
#     doc = nlp(text)
#     for ent in doc.ents:
#         if ent.label_ == "GPE":  # GPE = Geopolitical Entity (like cities, countries)
#             return ent.text
#     return None

# def recognize_speech():
#     """Recognize user speech and return text."""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("🎤 Say a city name to get weather info...")
#         speak("Say a city name to get weather information.")
#         recognizer.adjust_for_ambient_noise(source)
#         try:
#             audio = recognizer.listen(source)
#             text = recognizer.recognize_google(audio)
#             print(f"🗣 Recognized: {text}")
#             return text
#         except sr.UnknownValueError:
#             print("❌ Sorry, I couldn't understand that.")
#             speak("Sorry, I couldn't understand that.")
#         except sr.RequestError:
#             print("⚠ Error: Unable to fetch speech recognition results.")
#             speak("There was an issue with speech recognition.")
#     return None

# if __name__ == "__main__":
#     user_input = recognize_speech()
    
#     if user_input:
#         city = extract_city(user_input)
        
#         if city:
#             print(f"🌍 Identified City: {city}")
#             weather_info = get_weather(city)
#             print(f"⛅ {weather_info}")
#             speak(weather_info)
#         else:
#             print("❌ No city name recognized. Please try again.")
#             speak("No city name recognized. Please try again.")
