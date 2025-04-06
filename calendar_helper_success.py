import sys
import datetime
import os.path
import re
import pyttsx3
from dateutil import parser
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from plyer import notification
from threading import Thread
from data import speak, engine
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt

SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def create_event(summary, start_time_str, end_time_str):
    service = authenticate_google()
    event = {
        'summary': summary,
        'start': {'dateTime': start_time_str, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time_str, 'timeZone': 'Asia/Kolkata'},
        'reminders': {
            'useDefault': False,
            'overrides': [{'method': 'popup', 'minutes': 5}],
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    speak(f"Event '{summary}' created successfully.")
    return event.get('htmlLink')

def get_events_for_day(target_date):
    service = authenticate_google()
    start_of_day = datetime.datetime.combine(target_date, datetime.time.min).isoformat() + 'Z'
    end_of_day = datetime.datetime.combine(target_date, datetime.time.max).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=start_of_day, timeMax=end_of_day,
                                          singleEvents=True, orderBy='startTime').execute()
    return events_result.get('items', [])

def show_reminder_thread(events):
    def notify_me():
        now = datetime.datetime.now(datetime.timezone.utc)
        for event in events:
            start = event.get('start', {}).get('dateTime')
            summary = event.get('summary', 'No Title')
            if start:
                start_time = parser.parse(start)
                diff = (start_time - now).total_seconds()
                if 0 < diff <= 300:
                    notification.notify(
                        title="Upcoming Meeting Reminder",
                        message=f"{summary} at {start_time.strftime('%I:%M %p')}",
                        timeout=10
                    )
    Thread(target=notify_me).start()

class CalendarGUI(QWidget):
    def __init__(self, events):
        super().__init__()
        self.setWindowTitle("Calendar Events")
        self.setGeometry(200, 200, 600, 400)
        layout = QVBoxLayout()

        title = QLabel("Your Scheduled Events")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        table = QTableWidget()
        table.setRowCount(len(events))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Time", "Event"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for i, event in enumerate(events):
            start = event['start'].get('dateTime', event['start'].get('date'))
            time_str = parser.parse(start).strftime('%Y-%m-%d %I:%M %p')
            title = event.get('summary', 'No Title')

            table.setItem(i, 0, QTableWidgetItem(time_str))
            table.setItem(i, 1, QTableWidgetItem(title))

        layout.addWidget(table)
        self.setLayout(layout)
        self.show()

def display_gui_events(events):
    app = QApplication(sys.argv)
    gui = CalendarGUI(events)
    app.exec()

def calendar_helper(query: str):
    query = query.lower()
    auto_show_gui = any(kw in query for kw in ["today", "tomorrow", "on"])

    if "today" in query:
        today = datetime.date.today()
        events = get_events_for_day(today)
        if not events:
            speak("No meetings found for today.")
        else:
            speak("Here are your meetings for today.")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                speak(f"{start} - {event.get('summary', 'No Title')}")
            show_reminder_thread(events)
            print(events)
            if auto_show_gui:
                display_gui_events(events)
        return

    elif "tomorrow" in query:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        events = get_events_for_day(tomorrow)
        if not events:
            speak("No meetings found for tomorrow.")
        else:
            speak("Here are your meetings for tomorrow.")
            if auto_show_gui:
                display_gui_events(events)
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                speak(f"{start} - {event.get('summary', 'No Title')}")
            print(events)
        return

    elif "on" in query:
        try:
            date_str = query.split("on")[-1].strip()
            date = parser.parse(date_str, fuzzy=True).date()
            events = get_events_for_day(date)
            if not events:
                speak("No meetings found on that date.")
            else:
                speak(f"Here are your meetings on {date}.")
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    speak(f"{start} - {event.get('summary', 'No Title')}")
                if auto_show_gui:
                    display_gui_events(events)
            return
        except Exception:
            speak("Sorry, I couldn't understand the date you mentioned.")
            return

    if any(word in query for word in ["add", "create", "schedule", "set"]):
        title_match = re.search(r"(called|titled|named)\s(.+?)(\sat|\sfrom|$)", query)
        title = title_match.group(2).strip() if title_match else None

        time_match = re.search(r"(at|from)\s(.+?)(\sfor|\sto|$)", query)
        time_text = time_match.group(2).strip() if time_match else None

        duration_match = re.search(r"(for)\s(\d+)\s(hour|hours|minutes|min)", query)
        duration_mins = 60
        if duration_match:
            amount = int(duration_match.group(2))
            unit = duration_match.group(3)
            duration_mins = amount * 60 if "hour" in unit else amount

        if not title or not time_text:
            speak("Please specify the meeting name and time clearly.")
            return

        try:
            day_offset = 0
            if "tomorrow" in query:
                day_offset = 1
            base_date = datetime.date.today() + datetime.timedelta(days=day_offset)

            start_datetime = parser.parse(f"{base_date} {time_text}", fuzzy=True)
            end_datetime = start_datetime + datetime.timedelta(minutes=duration_mins)

            start_str = start_datetime.isoformat()
            end_str = end_datetime.isoformat()

            link = create_event(title, start_str, end_str)
            speak(f"Meeting scheduled. Here is the link:")
            print(link)
        except Exception as e:
            speak("Sorry, there was an issue scheduling the event.")
            print(e)
        return

    speak("I couldn't understand your request. Please try rephrasing it.")
    return



# calendar_helper_handler("Show me my events on 6th April")

# calendar_helper_handler("What are my meetings tomorrow")
# calendar_helper_handler("Create a meeting called Review Session at 11 AM for 45 minutes")
# calendar_helper_handler("Add a meeting on  april titled Strategy Discussion at 3 PM for 90 minutes")
# Schedule a strategic review meeting today at 6 PM
# calendar_helper_handler("Create a meeting called Strategic Review at 6 PM for 1 hour today")

# Schedule a white board meeting on the day after 7th April (i.e., 9th April)
# calendar_helper_handler("set a meeting called White Board Meeting at 10 AM for 1 hour on 9th April")


























































# import datetime
# import os.path
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build

# # If modifying these SCOPES, delete the token.json file.
# SCOPES = ['https://www.googleapis.com/auth/calendar']

# def authenticate_google():
#     creds = None
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
        
#         # Save credentials
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     return build('calendar', 'v3', credentials=creds)

# def get_upcoming_events(n=5):
#     service = authenticate_google()

#     now = datetime.datetime.utcnow().isoformat() + 'Z'
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                           maxResults=n, singleEvents=True,
#                                           orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     if not events:
#         return "No upcoming events found."

#     result = []
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         result.append(f"{start} - {event['summary']}")
    
#     return "\n".join(result)

# def create_event(summary, start_time_str, end_time_str):
#     service = authenticate_google()
    
#     event = {
#         'summary': summary,
#         'start': {'dateTime': start_time_str, 'timeZone': 'Asia/Kolkata'},
#         'end': {'dateTime': end_time_str, 'timeZone': 'Asia/Kolkata'},
#     }
#     event = service.events().insert(calendarId='primary', body=event).execute()
#     return f"Event created: {event.get('htmlLink')}"


# # Get events
# print(get_upcoming_events())

# # print(create_event("Team Meeting", "2025-04-06T10:00:00", "2025-04-06T11:00:00"))


# # # Get events
# # print(get_upcoming_events())