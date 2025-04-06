import os
import csv
import datetime
from fuzzywuzzy import fuzz
from PyQt6 import QtWidgets
import sys
import pyttsx3
import pandas as pd
from data import engine, speak  # Assuming you defined engine/speak in data.py

# Function to handle memory storage and retrieval
def memory_feature(query):
    query = query.lower()
    memory_file = "memory_log.csv"
    
    # Check for retrieval command
    retrieval_keywords = ["show", "what did", "retrieve", "display", "list", "recall"]
    is_retrieval = any(fuzz.partial_ratio(word, query) > 80 for word in retrieval_keywords)
    
    # Create the memory file if it doesn't exist
    if not os.path.exists(memory_file):
        with open(memory_file, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Note"])
    
    if is_retrieval:
        try:
            df = pd.read_csv(memory_file)
            speak("Here are your saved memories.")
            show_memory_tab(df)
        except Exception as e:
            speak("Sorry, I couldn't retrieve your memories.")
            print(e)
    else:
        # Save memory
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cleaned_note = clean_memory_query(query)
        
        if cleaned_note.strip():
            with open(memory_file, "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, cleaned_note])
            speak("Got it. I’ve saved that to memory.")
        else:
            speak("Sorry, I couldn't understand what you want me to remember.")

# Extract the actual content from the user's query
def clean_memory_query(query):
    memory_prefixes = [
        "remember that", "note that", "store this", "save this", "don't forget", 
        "keep in memory", "save that", "note this down", "please remember", "add this to memory", 
        "can you remember"
    ]
    
    for prefix in memory_prefixes:
        if prefix in query:
            return query.split(prefix)[-1].strip().capitalize()
    
    return query.strip().capitalize()

def show_memory_tab(df):
    class MemoryWindow(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Memory Log")
            self.setGeometry(100, 100, 800, 600)
            layout = QtWidgets.QVBoxLayout()

            table = QtWidgets.QTableWidget()
            table.setRowCount(len(df))
            table.setColumnCount(len(df.columns))
            table.setHorizontalHeaderLabels(df.columns)

            for row in range(len(df)):
                for col in range(len(df.columns)):
                    item = QtWidgets.QTableWidgetItem(str(df.iat[row, col]))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)  # Make it non-editable
                    item.setToolTip(str(df.iat[row, col]))  # Optional: show full content on hover
                    table.setItem(row, col, item)

            table.resizeColumnsToContents()
            table.resizeRowsToContents()
            table.setWordWrap(True)

            layout.addWidget(table)
            self.setLayout(layout)

    from PyQt6 import QtCore  # Ensure QtCore is imported
    app = QtWidgets.QApplication(sys.argv)
    window = MemoryWindow()
    window.show()
    app.exec()


# user_query = "Remember that you should go away now"
# memory_feature(user_query)
# user_query =  
# user_query = "Show me my saved memories"
# memory_feature(user_query)
