import datetime
import pyttsx3
from fuzzywuzzy import fuzz
from data import speak, engine  # Assuming you defined engine/speak in data.py

def get_time_date(query):
    query = query.lower()

    # Fuzzy match to determine if it's about time, date, or both
    time_keywords = ["time", "clock", "hour"]
    date_keywords = ["date", "day", "month", "year"]
    
    is_time = any(fuzz.partial_ratio(word, query) > 80 for word in time_keywords)
    is_date = any(fuzz.partial_ratio(word, query) > 80 for word in date_keywords)

    now = datetime.datetime.now()
    
    if is_time and is_date:
        response = f"Today is {now.strftime('%A, %d %B %Y')} and the time is {now.strftime('%I:%M %p')}"
    elif is_time:
        response = f"The current time is {now.strftime('%I:%M %p')}"
    elif is_date:
        response = f"Today is {now.strftime('%A, %d %B %Y')}"
    else:
        response = "Sorry, I couldn't understand if you wanted the time or date."
    print(response)
    speak(response)

# user_query = "What's the date now?"
# get_time_date(user_query)

