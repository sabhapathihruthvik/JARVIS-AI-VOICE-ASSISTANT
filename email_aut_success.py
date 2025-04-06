import google.generativeai as genai
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fuzzywuzzy import process
from dotenv import load_dotenv
import os
from data import EMAIL_CONTACTS, speak, engine  # Make sure speak is functional

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "sabhapathihruthvik@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PWORD")  # App password

# Fetch response from Gemini
def get_gemini_response(question):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Generate email subject and body
def generate_email_content(topic, recipient_name,query):
    prompt = f"""
    I am Hruthvik, the HR Manager. I need to send an email to {recipient_name}. My company is Eureka Technologies. Phone number is 6304628009.
    This email will be sent directly to the recipient, please make no mistakes and don't include ambiguous information.
    The topic is: '{topic}'.
    Do not include placeholders like [Your Name], [Company Name], [Contact Information], or similar. Instead, use the real details provided.
    The below is the exact query thats being provided for writing email, so please write email relevant to it
    {query}
    Please write a formal and well-structured email.
    Format it as:
    
    Subject: <Email subject>
    Body:
    <Email content>
    
    Make sure the tone is professional and the language is clear.
    """
    email_text = get_gemini_response(prompt)

    subject_match = re.search(r"Subject:\s*(.+)", email_text, re.IGNORECASE)
    subject = subject_match.group(1) if subject_match else "No Subject"

    body_match = re.search(r"Body:\s*(.+)", email_text, re.IGNORECASE | re.DOTALL)
    body = body_match.group(1) if body_match else "Could not generate email content."

    return subject.strip(), body.strip()

# Find best match for contact name
def find_best_match(name, contacts):
    best_match, score = process.extractOne(name.lower(), contacts.keys())
    return best_match if score > 80 else None

# Send the actual email
def send_email(recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())

        print("✅ Email sent successfully!")
        speak("Email sent successfully.")
    except Exception as e:
        error_msg = f"❌ Error sending email: {e}"
        print(error_msg)
        speak("There was an error sending the email.")

def write_email(query):
    # Try regex first
    match = re.search(r"write an email to (\w+)\s+about\s+(.+)", query.lower())

    if match:
        recipient_name = match.group(1)
        email_topic = match.group(2)
    else:
        # Fallback to Gemini for parsing if regex fails
        speak("Let me understand your request better.")
        extraction_prompt = f"""
        The user said: '{query}'.

        From this text, extract:
        1. The recipient's name.
        2. The topic of the email or what the email is about.

        Format:
        Recipient: <Name>
        Topic: <Email topic>

        If any of them cannot be determined, say 'None'.
        """
        response = get_gemini_response(extraction_prompt)
        print("🧠 Gemini Extraction:", response)

        rec_match = re.search(r"Recipient:\s*(\w+)", response, re.IGNORECASE)
        topic_match = re.search(r"Topic:\s*(.+)", response, re.IGNORECASE)

        recipient_name = rec_match.group(1) if rec_match else None
        email_topic = topic_match.group(1) if topic_match else None

    if not recipient_name or not email_topic:
        error_text = "❌ Unable to extract recipient or topic."
        print(error_text)
        speak("Sorry, I couldn't extract the recipient or topic. Please try again with more clarity.")
        return

    best_match = find_best_match(recipient_name, EMAIL_CONTACTS)
    
    if not best_match:
        msg = f"❌ No contact found for '{recipient_name}'."
        print(msg)
        speak(f"No contact found for {recipient_name}.")
        return

    recipient_email = EMAIL_CONTACTS[best_match]

    subject, body = generate_email_content(email_topic, best_match.title(), query)

    print(f"📩 Sending email to: {recipient_email}")
    print(f"📌 Subject: {subject}")
    print(f"✉️ Body:\n{body}\n")

    send_email(recipient_email, subject, body)

    print("✅ Email has been sent!")

# Example use
#write_email("Write an email to sumanth asking about his well being")
