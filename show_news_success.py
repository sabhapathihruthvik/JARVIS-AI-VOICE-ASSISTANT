import requests
import pyttsx3
import feedparser
from data import speak, engine

def show_news(query):
    """Fetches and presents news headlines based on a category in the query using Google News RSS."""
    print('📰 Fetching News...')

    # Define available categories
    categories = {
        "business": "business",
        "entertainment": "entertainment",
        "general": "world",
        "health": "health",
        "science": "science",
        "sports": "sports",
        "technology": "technology"
    }
    
    category = "world"  # Default category for general news

    # Extract category from query
    if query:
        query_lower = query.lower()
        for cat in categories:
            if cat in query_lower:
                category = categories[cat]
                break

    # Google News RSS URL
    url = f"https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFptYUdjU0FtVnVLQUFQAQ?hl=en-IN&gl=IN&ceid=IN:en"

    if category != "world":
        url = f"https://news.google.com/rss/search?q={category}&hl=en-IN&gl=IN&ceid=IN:en"

    try:
        # Fetch RSS feed
        feed = feedparser.parse(url)

        if not feed.entries:
            message = f"Sorry, no {category} news articles found at the moment."
            print("🚫 " + message)
            speak(message)
            return

        # Get top 5 news articles
        articles = feed.entries[:3]

        print(f"\n📢 Top {category.capitalize()} News Headlines:\n")
        news_summary = []

        for i, article in enumerate(articles, 1):
            title = article.title
            source = article.link

            print(f"{i}. {title}")
            print(f"   🔗 {source}\n")

            news_summary.append(f"Headline {i}: {title}.")

        # Speak the news
        speak(f"Here are the top {category} news headlines.")
        for news in news_summary:
            speak(news)

    except Exception as e:
        error_message = "⚠️ Error occurred while fetching news."
        print(error_message, e)
        speak("Sorry, I couldn't fetch the news at this time.")

# Example call
# show_news("Tell me the latest sports news")
