import sqlite3, datetime, re

def init_db():
    conn = sqlite3.connect("reminders.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reminders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  message TEXT,
                  remind_time TEXT)''')
    conn.commit()
    conn.close()


def add_reminder(text):
    text = text.lower()
    # Extract time pattern like "3 pm" or "14:30"
    time_match = re.search(r'(\d{1,2}(:\d{2})?\s*(am|pm)?)', text)
    remind_time = None
    if time_match:
        remind_time = time_match.group(1)
    message = re.sub(r'(\d{1,2}(:\d{2})?\s*(am|pm)?)', '', text)
    message = message.replace("remind me", "").replace("set a reminder", "").strip()

    conn = sqlite3.connect("reminders.db")
    c = conn.cursor()
    c.execute("INSERT INTO reminders (message, remind_time) VALUES (?, ?)", (message, remind_time))
    conn.commit()
    conn.close()

    if remind_time:
        return f"Reminder set for {message} at {remind_time}."
    else:
        return f"Reminder noted: {message}."


def check_due_reminders():
    conn = sqlite3.connect("reminders.db")
    c = conn.cursor()
    c.execute("SELECT message, remind_time FROM reminders")
    rows = c.fetchall()
    conn.close()

    now = datetime.datetime.now().strftime("%I:%M %p").lower()
    due = [f"Reminder: {msg}" for msg, t in rows if t and t.lower() == now]
    return due if due else []
