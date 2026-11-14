import sqlite3


def connect_db():
    return sqlite3.connect("learning.db")


def create_sessions_table(connection):
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


def add_session(connection, area, subject, topic, minutes, date, notes):
    insert_sql = """
    INSERT INTO sessions (area, subject, topic, minutes, date, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    connection.execute(insert_sql, (area, subject, topic, minutes, date, notes))
    connection.commit()


def get_all_sessions(connection):
    select_sql = """
    SELECT id, area, subject, topic, minutes, date, notes
    FROM sessions
    """
    cursor = connection.execute(select_sql)
    return cursor.fetchall()


def get_session_by_id(connection, session_id):
    select_sql = """
    SELECT id, area, subject, topic, minutes, date, notes
    FROM sessions
    WHERE id = ?
    """
    cursor = connection.execute(select_sql, (session_id,))
    return cursor.fetchone()


def update_session_field(connection, field, value, session_id):
    columns = {
        "area": "AREA",
        "subject": "SUBJECT",
        "topic": "TOPIC",
        "minutes": "MINUTES",
        "date": "DATE",
        "notes": "NOTES",
    }
    column = columns[field]
    update_sql = f"""
    UPDATE sessions
    SET {column} = ?
    WHERE id = ?
    """
    connection.execute(update_sql, (value, session_id))
    connection.commit()


def delete_session(connection, session_id):
    delete_sql = "DELETE FROM sessions WHERE id = ?"
    connection.execute(delete_sql, (session_id,))
    connection.commit()