import sqlite3
from datetime import datetime


while True:
    try:
        area = input("Enter the area of learning: ").strip()
        if not area:
            raise ValueError("Area of Learning cannot be empty.")
    except ValueError as error_area:
        print(f"Error: {error_area}")
        continue
    break

while True:
    try:
        subject = input("Enter the subject: ").strip()
        if not subject:
            raise ValueError("Subject cannot be empty.")
    except ValueError as error_subject:
        print(f"Error: {error_subject}")
        continue
    break

while True:
    try:
        topic = input("Enter the topic: ").strip()
        if not topic:
            raise ValueError("Topic cannot be empty.")
    except ValueError as error_topic:
        print(f"Error: {error_topic}")
        continue
    break

while True:
    try:
        minutes = int(input("Enter the number of minutes spent: "))
    except ValueError:
        print("Please enter a whole number.")
        continue

    if minutes <= 0:
        print("Minutes must be greater than 0.")
        continue

    break

while True:
    try:
        date = input("Enter the date (YYYY-MM-DD): ").strip()
        if not date:
            raise ValueError("Date cannot be empty.")
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as error_date:
        print(f"Error: {error_date}")
        continue
    break

notes = input("Enter any notes: ").strip()



connection = sqlite3.connect("learning.db")


sql = """CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    area TEXT,
    subject TEXT,
    topic TEXT,
    minutes INTEGER,
    date TEXT,
    notes TEXT
)
"""



insert_sql = """
INSERT INTO sessions (area, subject, topic, minutes, date, notes)
VALUES (?, ?, ?, ?, ?, ?)
"""


connection.execute(sql)

connection.execute(insert_sql, (area, subject, topic, minutes, date, notes))


connection.commit()
print("Session saved successfully!")
connection.close()