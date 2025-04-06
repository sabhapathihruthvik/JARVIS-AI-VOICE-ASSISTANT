# 🤖 JARVIS: AI Powered Voice Assistant

Welcome to **Jarvis**, an AI-powered voice assistant built with Python! This assistant integrates natural language processing, voice recognition, and email automation with generative AI to understand your commands and help you with tasks like sending emails, fetching information, and more.

---

## 🚀 Features

- 🎤 Voice-activated interface with wake-word detection ("Hey Jarvis")
- 🤖 Gemini AI (Google Generative AI) for natural language understanding and email generation
- ✉️ Intelligent email generation and sending
- 🔐 Environment variable support for secure API and email credentials
- 📦 Modular structure with clean separation of concerns
- 🧠 Fuzzy name matching for contact recognition
- 🗣️ Text-to-Speech responses via pyttsx3

---

## 🛠️ Tech Stack

- Python 3.10+
- [Google Generative AI](https://ai.google.dev/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- FuzzyWuzzy for name matching
- smtplib for email integration

---

## 📁 Project Structure

AI-POWERED-VOICE-ASSISTANT/ │ ├── data.py # Stores contacts and utility functions like speak() ├── main.py # Entry point for the assistant ├── utils/ │ └── email_utils.py # Email writing, Gemini prompts, email sending ├── credentials.json # 🔒 OAuth Credentials (IGNORED in Git) ├── token.json # 🔒 Token file for API access (IGNORED) ├── .env # 🔒 API keys and sensitive data (IGNORED) ├── .gitignore ├── README.md

---

## ⚙️ Setup Instructions

1. **Clone the Repository**


git clone https://github.com/sabhapathihruthvik/JARVIS-AI-VOICE-ASSISTANT.git
cd JARVIS-AI-VOICE-ASSISTANT

2.Create .env file


GOOGLE_API_KEY=your_google_gemini_api_key
EMAIL_PWORD=your_app_password_for_gmail


3.Install Dependencies


pip install -r requirements.txt


4.Add Contacts

In data.py:


EMAIL_CONTACTS = {
    "sumanth": "sumanth@example.com",
    "akhil": "akhil@example.com",
    # Add more here
}


5.Run the Assistant


python main.py


Say "Hey Jarvis" to activate it.
