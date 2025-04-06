
# import joblib

# # Load the saved model
# model_filename = "intent_recognition_model.pkl"
# model = joblib.load(model_filename)

# # Function to predict intent
# def predict_intent(text):
#     return model.predict([text])[0]

# # Test the model with sample inputs
# test_sentences = [
#     "increase the sound",                        # increase_volume
#     "insrease brightness",                       # increase_brightness
#     "reboot my pc",                              # restart
#     "kill all apps",                             # close_all_apps
#     "play some music",                           # play_music
#     "play a movie",                              # play_movie
#     "open the browser",                          # opening_apps_and_websites
#     "close everything",                          # close_all_apps
#     "search for songs on youtube",               # play_on_youtube

#     "open Netflix",                              # opening_apps_and_websites
#     "exit notepad",                              # close_app
#     "open google.com",                           # opening_apps_and_websites
#     "go to Amazon",                              # opening_apps_and_websites
#     "what is the weather like in Delhi?",        # weather_query
#     "how is the weather here",                   # weather_query
#     "show me the latest news",                   # show_news
#     "search how to make pancakes",               # web_search
#     "google who is the prime minister of UK",    # web_search
#     "ask ChatGPT what is quantum computing",     # llm_query

#     "send a message to Rahul on WhatsApp",       # whatsapp_message
#     "call Riya via WhatsApp",                    # whatsapp_call
#     "start a video call with Mom on WhatsApp"    # whatsapp_video_call
# ]


# # Print predictions
# for sentence in test_sentences:
#     print(f"User: {sentence} -> Intent: {predict_intent(sentence)}")


import random
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

# Training Data - Various Sentence Variations for Each Intent
training_data = [
("Turn up the volume", "increase_volume"),
("Raise the volume", "increase_volume"),
("Make it louder", "increase_volume"),
("Increase the sound", "increase_volume"),
("Boost the volume", "increase_volume"),
("Enhance the audio", "increase_volume"),
("Turn the sound up", "increase_volume"),
("Pump up the sound", "increase_volume"),
("Can you make it louder?", "increase_volume"),
("Raise the audio a bit", "increase_volume"),
("Volume is too low, increase it", "increase_volume"),

("Dim the lights", "decrease_brightness"),
("Too bright! Reduce it", "decrease_brightness"),
("Make it a little darker", "decrease_brightness"),
("Lower the brightness level", "decrease_brightness"),
("Can you dim the screen?", "decrease_brightness"),
("Reduce the display brightness", "decrease_brightness"),
("Make it less bright", "decrease_brightness"),
("Lower the screen light", "decrease_brightness"),
("Screen is too bright, dim it", "decrease_brightness"),
("Can you make it darker?", "decrease_brightness"),
("Brightness is too high, reduce it", "decrease_brightness"),

("Play some music", "play_music"),
("Start playing songs", "play_music"),
("Play my favorite playlist", "play_music"),
("Turn on some tunes", "play_music"),
("Begin playing audio files", "play_music"),
("Play a song from my PC", "play_music"),
("Start the music player", "play_music"),
("Play local songs", "play_music"),

("Play a movie", "play_movie"),
("Start the video player", "play_movie"),
("Turn on a film", "play_movie"),
("Show me a movie", "play_movie"),
("Start playing a film", "play_movie"),
("Play a video from my PC", "play_movie"),
("Run a movie file", "play_movie"),

("Play 'Shape of You' on YouTube", "search_youtube"),
("Start 'Despacito' video on YouTube", "search_youtube"),
("Search for 'lofi beats' on YouTube", "search_youtube"),
("Find and play 'Relaxing music' on YouTube", "search_youtube"),
("Play 'Imagine Dragons - Believer' video", "search_youtube"),
("Stream 'Workout motivation mix' on YouTube", "search_youtube"),
("Search and play 'Top hits 2024' on YouTube", "search_youtube"),
("Search for songs on YouTube", "search_youtube"),
("Look for music videos on YouTube", "search_youtube"),
("Find songs on YouTube", "search_youtube"),
("Search YouTube for my favorite tracks", "search_youtube"),
("Look up music on YouTube", "search_youtube"),
("Find my favorite artists on YouTube", "search_youtube"),

("Open Chrome", "opening_apps_and_websites"),
("Start Notepad", "opening_apps_and_websites"),
("Launch VS Code", "opening_apps_and_websites"),
("Run Microsoft Word", "opening_apps_and_websites"),
("Execute Calculator", "opening_apps_and_websites"),
("Start Spotify", "opening_apps_and_websites"),
("Launch Zoom", "opening_apps_and_websites"),
("Open Telegram", "opening_apps_and_websites"),

("Close Chrome", "close_app"),
("Exit Notepad", "close_app"),
("Shut down VS Code", "close_app"),
("Terminate Microsoft Word", "close_app"),
("Stop the Calculator", "close_app"),
("Close Spotify", "close_app"),
("End Zoom", "close_app"),
("Shut down Telegram", "close_app"),

("Open Google", "opening_apps_and_websites"),
("Go to YouTube", "opening_apps_and_websites"),
("Launch Twitter", "opening_apps_and_websites"),
("Start Facebook", "opening_apps_and_websites"),
("Browse Amazon", "opening_apps_and_websites"),
("Visit Wikipedia", "opening_apps_and_websites"),
("Open Stack Overflow", "opening_apps_and_websites"),
("Go to GitHub", "opening_apps_and_websites"),

("What is the weather today?", "weather"),
("Tell me the weather in New York", "weather"),
("How's the weather outside?", "weather"),
("Weather update for London", "weather"),
("Is it raining in Mumbai?", "weather"),
("Check today's forecast", "weather"),
("Weather report for San Francisco", "weather"),
("Will it snow in Toronto?", "weather"),
("Give me the temperature in Dubai", "weather"),
("How's the climate in Sydney?", "weather"),
("What's the weather like in Tokyo?", "weather"),

("Turn down the volume", "decrease_volume"),
("Lower the sound", "decrease_volume"),
("Reduce the volume", "decrease_volume"),
("Make it quieter", "decrease_volume"),
("Drop the sound level", "decrease_volume"),

("Increase screen brightness", "increase_brightness"),
("Make the screen brighter", "increase_brightness"),
("Boost the brightness", "increase_brightness"),
("Turn up the brightness", "increase_brightness"),
("Enhance the display light", "increase_brightness"),

("Shutdown the system", "shutdown"),
("Turn off the computer", "shutdown"),
("Kill the power", "shutdown"),
("Power off the PC", "shutdown"),
("End all processes", "shutdown"),

("Restart my PC", "restart"),
("Reboot the computer", "restart"),
("Give my system a restart", "restart"),
("Turn it off and on again", "restart"),
("Reset the machine", "restart"),
("Reboot the system", "restart"),
("Reboot the computer", "restart"),

("Show me the news", "show_news"),
("Give me today's headlines", "show_news"),
("What's happening in the world?", "show_news"),
("Open the news", "show_news"),
("Tell me the current affairs", "show_news"),
("Fetch latest news updates", "show_news"),
("Display the top stories", "show_news"),
("Get me breaking news", "show_news"),
("News update please", "show_news"),
("What’s in the news today?", "show_news"),
("Show me the latest news", "show_news"),
("Tell me the latest headlines", "show_news"),
("Get me today's news", "show_news"),
("Fetch the news for today", "show_news"),
("Display the news headlines", "show_news"),
("Bring up the news articles", "show_news"),
("Show me the current news", "show_news"),
("Get me the latest updates", "show_news"),
("Fetch today's headlines", "show_news"),

("Search for cute cat videos", "web_search"),
("Google how to cook pasta", "web_search"),
("Find me the best laptops under 50k", "web_search"),
("Look up Python tutorials", "web_search"),
("Can you Google this word?", "web_search"),
("Search the internet for cricket scores", "web_search"),
("Find top tech books online", "web_search"),
("Browse information on global warming", "web_search"),
("Show me images of space", "web_search"),

("Ask ChatGPT to explain recursion", "llm_query"),
("Query the AI about space travel", "llm_query"),
("What does Gemini say about inflation?", "llm_query"),
("Use the assistant to summarize this text", "llm_query"),
("Send this question to the AI", "llm_query"),
("Tell the LLM to generate a poem", "llm_query"),
("Ask the language model to define entropy", "llm_query"),
("Let the bot solve this riddle", "llm_query"),
("Query GPT for a math formula", "llm_query"),
("Use the AI to paraphrase the sentence", "llm_query"),

("Remember that I parked my car on level B2", "memory_feature"),
("Note that I have a meeting at 5 PM", "memory_feature"),
("Store this: My wallet is in the drawer", "memory_feature"),
("Save this memory: I left my charger in the living room", "memory_feature"),
("Don't forget I have a dentist appointment tomorrow", "memory_feature"),
("Remember my password is saved in the file", "memory_feature"),
("Keep in memory that I have to buy groceries", "memory_feature"),
("Save that I met Riya today", "memory_feature"),
("Note this down: my locker combination is 19-28-37", "memory_feature"),
("Please remember that I completed the task", "memory_feature"),
("Add this to memory: I'm going to the gym at 6", "memory_feature"),
("Can you remember I finished my homework?", "memory_feature"),
("Show me my saved memories", "memory_feature"),
("What did I ask you to remember?", "memory_feature"),
("Retrieve my notes", "memory_feature"),
("Display my memory log", "memory_feature"),
("Do you recall what I told you?", "memory_feature"),
("List all saved memories", "memory_feature"),
("Show stored notes", "memory_feature"),
("Can you display my reminders?", "memory_feature"),

("What meetings do I have today?", "calendar_helper"),
("Show tomorrow's calendar events", "calendar_helper"),
("Add a meeting called Project Review tomorrow at 3 PM", "calendar_helper"),
("Schedule Team Sync at 5 PM", "calendar_helper"),
("Create an event called Client Discussion at 11 AM lasting 2 hours", "calendar_helper"),
("Do I have any appointments on April 10th?", "calendar_helper"),
("Set up a Google Meet tomorrow morning for 1 hour", "calendar_helper"),
("Plan a Zoom call with John at 9:30 AM for 90 minutes", "calendar_helper"),
("I want to book a meeting at 2 PM titled Weekly Update", "calendar_helper"),
("What's on my calendar this week?", "calendar_helper"),
("Show me my schedule for today", "calendar_helper"),
("List my calendar events for this month", "calendar_helper"),

("What time is it?", "get_time_date"),
("Tell me the time", "get_time_date"),
("Can you tell the current time?", "get_time_date"),
("I want to know the time", "get_time_date"),
("Current time please", "get_time_date"),
("What's the time now?", "get_time_date"),
("Give me the time", "get_time_date"),
("What is today's date?", "get_time_date"),
("Tell me today's date", "get_time_date"),
("Can you tell the current date?", "get_time_date"),
("I want to know the date", "get_time_date"),
("Current date please", "get_time_date"),
("What's the date today?", "get_time_date"),
("Give me today's date", "get_time_date"),
("Date and time", "get_time_date"),
("Tell me date and time", "get_time_date"),
("What day is it?", "get_time_date"),
("Day, date and time please", "get_time_date"),
("What’s the date and time now?", "get_time_date"),
("Time and date now", "get_time_date"),

("Spell apple", "spell_word_handler"),
("How do you write opportunity?", "spell_word_handler"),
("Spell 'entrepreneur'", "spell_word_handler"),
("Can you spell intelligence?", "spell_word_handler"),
("Tell me how to spell beautiful", "spell_word_handler"),
("How is psychology spelled?", "spell_word_handler"),
("Spell the word 'phenomenon'", "spell_word_handler"),
("Can you tell me the spelling of serendipity?", "spell_word_handler"),
("Please spell environment", "spell_word_handler"),
("What's the spelling of ambiguity?", "spell_word_handler"),


("What's my battery percentage?", "battery_status"),
("Do I need to charge now?", "battery_status"),
("How much battery do I have left?", "battery_status"),
("Is my battery low?", "battery_status"),
("Tell me the battery level", "battery_status"),
("Battery status please", "battery_status"),
("What's the charge left?", "battery_status"),
("Show me my battery percentage", "battery_status"),
("Check battery level", "battery_status"),
("Do I have enough battery?", "battery_status"),

("Send a WhatsApp message to John", "whatsapp_message"),
("Message Dad on WhatsApp", "whatsapp_message"),
("Text Nisha using WhatsApp", "whatsapp_message"),
("Say hello to Akash via WhatsApp", "whatsapp_message"),
("Tell Anu I'll be late through WhatsApp", "whatsapp_message"),
("WhatsApp my friend about the meeting", "whatsapp_message"),
("Ping Riya on WhatsApp", "whatsapp_message"),
("Drop a message to Sam on WhatsApp", "whatsapp_message"),
("WhatsApp my colleague about the project", "whatsapp_message"),
("Text my sister on WhatsApp", "whatsapp_message"),

("Send an email to my professor", "write_email"),
("Write an email to HR regarding leave", "write_email"),
("Email my friend about the party", "write_email"),
("Compose a message to the manager", "write_email"),
("Draft an email to the client", "write_email"),
("Send a mail to my colleague", "write_email"),
("Mail my boss about the project update", "write_email"),
("Write and send an email to Priya", "write_email"),
("Create an email for the meeting details", "write_email"),
("Send an official email to the team", "write_email"),
("Email a thank-you note to the interviewer", "write_email"),
("Compose a formal email to the principal", "write_email"),
("Write an email about the bug I found", "write_email"),
("Send feedback to the support team via email", "write_email"),
("Draft an apology email to the teacher", "write_email"),
("Write an email to reschedule the appointment", "write_email"),
("Send a follow-up email to the recruiter", "write_email"),
("Email my resume to the company", "write_email"),
("Write a job application email", "write_email"),
("Send an email to check the assignment status", "write_email"),

("Call Mom on WhatsApp", "whatsapp_call"),
("Video call Dad using WhatsApp", "whatsapp_call"),
("WhatsApp video call to Nisha", "whatsapp_call"),
("Make a voice call to Akash via WhatsApp", "whatsapp_call"),
("WhatsApp call to Anu", "whatsapp_call"),
("Video chat with Riya on WhatsApp", "whatsapp_call"),
("WhatsApp voice call to Sam", "whatsapp_call"),
("WhatsApp call to my friend", "whatsapp_call"),
("Video call my colleague on WhatsApp", "whatsapp_call"),
("WhatsApp call to my sister", "whatsapp_call"),

("Start a video call with Priya on WhatsApp", "whatsapp_video_call"),
("WhatsApp video call Arjun", "whatsapp_video_call"),
("Make a video call to Sneha using WhatsApp", "whatsapp_video_call"),
("Do a WhatsApp video chat with Meena", "whatsapp_video_call"),
("Video call Raj via WhatsApp", "whatsapp_video_call"),
("WhatsApp video call to my friend", "whatsapp_video_call"),
("WhatsApp video call to my colleague", "whatsapp_video_call"),
("Video chat with my sister on WhatsApp", "whatsapp_video_call"),
("WhatsApp video call to my brother", "whatsapp_video_call"),
("WhatsApp video call to my cousin", "whatsapp_video_call"),

("Stop the music", "stop_music"),
("Pause the music", "stop_music"),
("Turn off the music", "stop_music"),
("Can you stop the music?", "stop_music"),
("I want the music to stop", "stop_music"),
("End the music playback", "stop_music"),
("Stop playing songs", "stop_music"),
("Halt the music now", "stop_music"),
("Music is annoying, stop it", "stop_music"),
("Turn off Windows Media Player", "stop_music"),
("Close the music player", "stop_music"),

("Stop the movie", "stop_movie"),
("Pause the video", "stop_movie"),
("Close the movie player", "stop_movie"),
("End the video now", "stop_movie"),
("Can you stop VLC?", "stop_movie"),
("I want the movie to stop", "stop_movie"),
("Turn off the movie", "stop_movie"),
("Stop VLC from playing", "stop_movie"),
("Shut the video down", "stop_movie"),
("Quit the movie player", "stop_movie"),
("Stop playing the film", "stop_movie"),

("Take a screenshot", "take_screenshot"),
("Capture my screen", "take_screenshot"),
("Grab a screenshot now", "take_screenshot"),
("Snap a screen photo", "take_screenshot"),
("Can you take a screenshot?", "take_screenshot"),
("I want a screenshot", "take_screenshot"),
("Capture the current screen", "take_screenshot"),
("Take a quick screenshot", "take_screenshot"),
("Screenshot this", "take_screenshot"),
("Save a picture of my screen", "take_screenshot"),
("Snap this screen", "take_screenshot"),
("Take a screen capture", "take_screenshot"),
("Make a screenshot", "take_screenshot"),
("Screenshot the current view", "take_screenshot"),
("Take a picture of my screen", "take_screenshot"),
("Snap this window", "take_screenshot"),
("Capture this window", "take_screenshot"),
("Take a snapshot of my screen", "take_screenshot"),
("Grab a screen capture", "take_screenshot"),
("Take a photo of my screen", "take_screenshot"), 

]

# Shuffle dataset
random.shuffle(training_data)

# Split into text and labels
texts, labels = zip(*training_data)

# Create model pipeline (TF-IDF + SVM Classifier)
model = make_pipeline(TfidfVectorizer(), SVC(kernel="linear"))

# Train the model
model.fit(texts, labels)

# Save the model
model_filename = "intent_recognition_model.pkl"
joblib.dump(model, model_filename)

print(f"✅ Model trained and saved as '{model_filename}'")
