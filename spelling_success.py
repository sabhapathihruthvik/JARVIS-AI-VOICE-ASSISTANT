import pyttsx3
import re

engine = pyttsx3.init()

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def spell_word_handler(query: str):
    query = query.lower()

    # Spell check
    spell_match = re.search(r"(spell|how do you write)\s['\"]?([a-zA-Z\-']+)['\"]?", query)
    if spell_match:
        word = spell_match.group(2)
        spelled = ', '.join(list(word.upper()))
        speak(f"{word.capitalize()} is spelled as: {spelled}")
        return

    speak("Please ask me to spell a word.")

# spell_word_handler("How do you spell psychology?")
