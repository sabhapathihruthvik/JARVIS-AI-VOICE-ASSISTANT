import yt_dlp
import webbrowser
from data import speak  # Assuming you defined speak in data.py
def search_youtube(query):
    """
    Takes a user's query (text) and searches for the first video on YouTube,
    then plays it in the browser.
    """
    search_query = f"ytsearch1:{query}"  # Ensures only 1 result is fetched
    ydl_opts = {"quiet": True, "extract_flat": True, "skip_download": True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(search_query, download=False)

        if result and "entries" in result and result["entries"]:
            video_url = result["entries"][0]["url"]
            print(f"Playing: {video_url}")
            webbrowser.open(video_url)  # Open in browser
        else:
            print("No results found!")

    except Exception as e:
        print(f"Error fetching video: {e}")
        speak("Sorry, I couldn't find that video.")

# # Example usage
# query="play parallel universe theory on youtube"
# search_youtube(query)
