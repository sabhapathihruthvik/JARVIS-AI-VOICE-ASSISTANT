import re
import webbrowser
import pyttsx3
from data import speak, engine
def web_search(query):
    """Performs a Google search based on a spoken query."""
    if not query:
        speak("Sorry, I didn't catch your query.")
        return

    query = query.lower()

    # Remove trigger phrases to extract core search topic
    patterns_to_remove = [
        r"search (for|about|in)?\s?", 
        r"google\s?(search)?", 
        r"look\s?up\s?", 
        r"give me (the|a)?\s?",
        r"find (me)?\s?",
        r"show me\s?",
        r"from google",
        r"in google",
        r"search for (the)?\s"
    ]

    cleaned_query = query
    for pattern in patterns_to_remove:
        cleaned_query = re.sub(pattern, "", cleaned_query).strip()

    # Build Google search URL
    search_url = f"https://www.google.com/search?q={cleaned_query.replace(' ', '+')}"

    # Open in web browser
    webbrowser.open(search_url)
    print(f"🔍 Searching Google for: {cleaned_query}")
    speak(f"Searching Google for {cleaned_query}")

# Example usage
# web_search("search about quantum computing in google")
