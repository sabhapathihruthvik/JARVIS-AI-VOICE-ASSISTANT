import re
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QTextEdit, QWidget, QVBoxLayout
from PyQt6.QtGui import QFont
from dotenv import load_dotenv
import os
import google.generativeai as genai
from data import speak, engine



# 🔐 Load API key and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 🤖 Gemini response function
def get_gemini_response(question):
    """Takes user input, sends it to Gemini AI, and returns the response."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# 🪟 GUI for showing LLM results
class LLMWindow(QMainWindow):
    def __init__(self, title, answer):
        super().__init__()
        self.setWindowTitle("AI Assistant - Gemini Response")
        self.setGeometry(100, 100, 800, 400)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        tab = QWidget()
        layout = QVBoxLayout()
        self.text_area = QTextEdit()
        self.text_area.setText(answer)
        self.text_area.setFont(QFont("Consolas", 12))
        self.text_area.setReadOnly(True)

        layout.addWidget(self.text_area)
        tab.setLayout(layout)
        self.tabs.addTab(tab, title)

        self.show()

# 🧠 Main helper function
def llm_query(query):
    if not query:
        speak("I didn't receive any query.")
        return

    query = query.lower()

    # Trigger phrases to strip
    triggers = [
        r"ask (chatgpt|the ai|the assistant|the bot|the language model|gemini)\s?(to)?",
        r"(query|tell|send|use|let)\s?(the)?\s?(ai|assistant|llm|language model|chatgpt|gemini|bot)?\s?(to)?",
        r"(what does|how does|what is|define|solve)\s?(gemini|chatgpt|the ai|the assistant)?",
    ]

    clean_prompt = query
    for pattern in triggers:
        clean_prompt = re.sub(pattern, "", clean_prompt).strip()

    if not clean_prompt:
        speak("Please specify what you want to ask.")
        return

    # 🧠 Get response from Gemini
    answer = get_gemini_response(clean_prompt)

    speak("Here is the result.")

    # 🪟 Show result using PyQt
    app = QApplication(sys.argv)
    window = LLMWindow("Gemini Result", answer)
    app.exec()

# 🔄 Sample use
# llm_query("Ask the assistant to explain black holes")
# llm_query("Tell me about the latest in AI technology")