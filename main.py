import sqlite3
from datetime import datetime



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
connection.execute(sql)


# Decision loop
while True:
    decision = input("Select your action: (add/view/edit/delete): ").strip().lower()
    print(f"You selected: {decision}")
    if decision not in ['add', 'view', 'edit', 'delete']:
        print("Invalid input. Please enter 'add', 'view', 'edit' or 'delete'.")
        continue
    break

# ADD loop
if decision == "add":
    while True:
        try:
            area = input("Enter the area of learning: ").strip()
            if not area:
                raise ValueError("Area of learning cannot be empty.")
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


    insert_sql = """
    INSERT INTO sessions (area, subject, topic, minutes, date, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    connection.execute(insert_sql, (area, subject, topic, minutes, date, notes))
    connection.commit()
    print("Session saved successfully!")


# VIEW loop
elif decision == "view":
    select_sql = """
    SELECT id, area, subject, topic, minutes, date, notes
    FROM sessions
    """
    cursor = connection.execute(select_sql)
    sessions = cursor.fetchall()
    if sessions:
        for session in sessions:
            print(
                f"ID: {session[0]} | Area: {session[1]} | "
                f"Subject: {session[2]} | Topic: {session[3]} | "
                f"Minutes: {session[4]} | Date: {session[5]} | Notes: {session[6]}"
            )
    else:
        print("No sessions found.")

# EDIT LOOP
elif decision == "edit":
    while True:
        try:
            session_id = int(input("Enter the ID of the session you want to edit: "))
        except ValueError:
            print("Please enter a valid session ID.")
            continue
        break


    select_sql = """
    SELECT id, area, subject, topic, minutes, date, notes
    FROM sessions
    WHERE id = ?
    """
    cursor = connection.execute(select_sql, (session_id,))
    session = cursor.fetchone()


    if session is None:
        print(f"No session found with ID {session_id}.")
    else:
        print("Found session:")
        print(
            f"ID: {session[0]} | Area: {session[1]} | "
            f"Subject: {session[2]} | Topic: {session[3]} | "
            f"Minutes: {session[4]} | Date: {session[5]} | Notes: {session[6]}"
        )

        while True:
            choice = input("Choose your edit: (area/subject/topic/minutes/date/notes): "
            ).strip().lower()
            if choice not in ['area', 'subject', 'topic', 'minutes', 'date', 'notes']:
                print("Invalid choice. Please enter 'area', 'subject', 'topic', 'minutes',"
                " 'date' or 'notes'.")
                continue
            break

        if choice == "area":
            update_sql = """
            UPDATE sessions
            SET AREA = ?
            WHERE id = ?
            """
            while True:
                try:
                    new_area = input("Enter the area of learning: ").strip()
                    if not new_area:
                        raise ValueError("Area of learning cannot be empty.")
                except ValueError as error_area:
                    print(f"Error: {error_area}")
                    continue
                break
            connection.execute(update_sql, (new_area, session_id))
            connection.commit()
            print("Area updated successfully!")

        if choice == "subject":
            update_sql = """
            UPDATE sessions
            SET SUBJECT = ?
            WHERE id = ?
            """
            while True:
                try:
                    new_subject = input("Enter the new subject: ").strip()
                    if not new_subject:
                        raise ValueError("The new subject cannot be empty.")
                except ValueError as error_subject:
                    print(f"Error: {error_subject}")
                    continue
                break
            connection.execute(update_sql, (new_subject, session_id))
            connection.commit()
            print("Subject updated successfully!")

        if choice == "topic":
            update_sql = """
            UPDATE sessions
            SET TOPIC = ?
            WHERE id = ?
            """
            while True:
                try:
                    new_topic = input("Enter the new topic: ").strip()
                    if not new_topic:
                        raise ValueError("The new topic cannot be empty.")
                except ValueError as error_topic:
                    print(f"Error: {error_topic}")
                    continue
                break
            connection.execute(update_sql, (new_topic, session_id))
            connection.commit()
            print("Topic updated successfully!")

        if choice == "minutes":
            update_sql = """
            UPDATE sessions
            SET MINUTES = ?
            WHERE id = ?
            """
            while True:
                try:
                    new_minutes = int(input("Enter the new number of minutes spent: "))
                except ValueError:
                    print("Please enter a whole number.")
                    continue
                if new_minutes <= 0:
                    print("Minutes must be greater than 0.")
                    continue
                break
            connection.execute(update_sql, (new_minutes, session_id))
            connection.commit()
            print("Minutes updated successfully!")

        if choice == "date":
            update_sql = """
            UPDATE sessions
            SET DATE = ?
            WHERE id = ?
            """
            while True:
                try:
                    new_date = input("Enter the new date (YYYY-MM-DD): ").strip()
                    if not new_date:
                        raise ValueError("Date cannot be empty.")
                    datetime.strptime(new_date, "%Y-%m-%d")
                except ValueError as error_date:
                    print(f"Error: {error_date}")
                    continue
                break
            connection.execute(update_sql, (new_date, session_id))
            connection.commit()
            print("Date updated successfully!")

        if choice == "notes":
            update_sql = """
            UPDATE sessions
            SET NOTES = ?
            WHERE id = ?
            """
            new_notes = input("Enter the updated notes: ").strip()
            connection.execute(update_sql, (new_notes, session_id))
            connection.commit()
            print("Notes updated successfully!")

# DELETE LOOP
elif decision == "delete":
    while True:
        try:
            session_id = int(input("Enter the ID of the session you want to delete: "))
        except ValueError:
            print("Please enter a valid session ID.")
            continue
        break
    
    select_sql = """
    SELECT id, area, subject, topic, minutes, date, notes
    FROM sessions
    WHERE id = ?
    """
    cursor = connection.execute(select_sql, (session_id,))
    session = cursor.fetchone()

    if session is None:
        print(f"No session found with ID {session_id}.")
    else:
        print("Found session:")
        print(
            f"ID: {session[0]} | Area: {session[1]} | "
            f"Subject: {session[2]} | Topic: {session[3]} | "
            f"Minutes: {session[4]} | Date: {session[5]} | Notes: {session[6]}"
        )
        while True:
            confirmation = input("Delete this session? (y/n): ").strip().lower()
            if confirmation in ("y", "n"):
                break
            print("Please enter y or n.")

        if confirmation == "y":
            delete_sql = "DELETE FROM sessions WHERE id = ?"
            connection.execute(delete_sql, (session_id,))
            connection.commit()
            print("Session deleted successfully!")
        else:
            print("Deletion canceled.")



connection.close()