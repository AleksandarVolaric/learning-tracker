import sqlite3


def connect_db():
    connection = sqlite3.connect("learning.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(connection):
    with open("schema.sql", encoding="utf-8") as schema_file:
        connection.executescript(schema_file.read())


def get_all_subjects(connection):
    select_sql = """
    SELECT id, name
    FROM subjects
    ORDER BY name
    """
    cursor = connection.execute(select_sql)
    return cursor.fetchall()


def get_or_create_subject(connection, name):
    select_sql = "SELECT id FROM subjects WHERE name = ?"
    subject = connection.execute(select_sql, (name,)).fetchone()
    if subject is not None:
        return subject[0]

    insert_sql = "INSERT INTO subjects (name) VALUES (?)"
    cursor = connection.execute(insert_sql, (name,))
    connection.commit()
    return cursor.lastrowid


def add_session(connection, area, subject_id, topic, minutes, date, notes):
    insert_sql = """
    INSERT INTO sessions (area, subject_id, topic, minutes, date, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    connection.execute(insert_sql, (area, subject_id, topic, minutes, date, notes))
    connection.commit()


def get_all_sessions(connection):
    select_sql = """
    SELECT sessions.id, sessions.area, subjects.name, sessions.topic,
           sessions.minutes, sessions.date, sessions.notes
    FROM sessions
    JOIN subjects ON sessions.subject_id = subjects.id
    """
    cursor = connection.execute(select_sql)
    return cursor.fetchall()


def get_session_by_id(connection, session_id):
    select_sql = """
    SELECT sessions.id, sessions.area, subjects.name, sessions.topic,
           sessions.minutes, sessions.date, sessions.notes
    FROM sessions
    JOIN subjects ON sessions.subject_id = subjects.id
    WHERE sessions.id = ?
    """
    cursor = connection.execute(select_sql, (session_id,))
    return cursor.fetchone()


def update_session_field(connection, field, value, session_id):
    columns = {
        "area": "area",
        "subject": "subject_id",
        "topic": "topic",
        "minutes": "minutes",
        "date": "date",
        "notes": "notes",
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


def get_sessions_by_subject(connection, subject_id):
    where_sql_subject = """
    SELECT sessions.id, sessions.area, subjects.name, sessions.topic,
           sessions.minutes, sessions.date, sessions.notes
    FROM sessions
    JOIN subjects ON sessions.subject_id = subjects.id
    WHERE sessions.subject_id = ?
    """
    cursor = connection.execute(where_sql_subject, (subject_id,))
    return cursor.fetchall()


def get_sessions_by_area(connection, area):
    where_sql_area = """
    SELECT sessions.id, sessions.area, subjects.name, sessions.topic,
           sessions.minutes, sessions.date, sessions.notes
    FROM sessions
    JOIN subjects ON sessions.subject_id = subjects.id
    WHERE sessions.area = ?
    """
    cursor = connection.execute(where_sql_area, (area,))
    return cursor.fetchall()


def get_sessions_by_date(connection, date):
    where_sql_date = """
    SELECT sessions.id, sessions.area, subjects.name, sessions.topic,
           sessions.minutes, sessions.date, sessions.notes
    FROM sessions
    JOIN subjects ON sessions.subject_id = subjects.id
    WHERE sessions.date = ?
    """
    cursor = connection.execute(where_sql_date, (date,))
    return cursor.fetchall()


def get_sessions_oldest_first(connection):
    select_sql_asc = """
    SELECT sessions.id, sessions.area, subjects.name, sessions.topic,
           sessions.minutes, sessions.date, sessions.notes
    FROM sessions
    JOIN subjects ON sessions.subject_id = subjects.id
    ORDER BY sessions.date ASC
    """
    cursor = connection.execute(select_sql_asc)
    return cursor.fetchall()


def get_sessions_newest_first(connection):
    select_sql_desc = """
    SELECT sessions.id, sessions.area, subjects.name, sessions.topic,
           sessions.minutes, sessions.date, sessions.notes
    FROM sessions
    JOIN subjects ON sessions.subject_id = subjects.id
    ORDER BY sessions.date DESC
    """
    cursor = connection.execute(select_sql_desc)
    return cursor.fetchall()


def get_learning_totals(connection):
    select_sql_totals = """
    SELECT COUNT(*), COALESCE(SUM(minutes), 0)
    FROM sessions
    """
    cursor = connection.execute(select_sql_totals)
    return cursor.fetchone()


def get_subject_statistics(connection):
    select_sql_subjects = """
    SELECT subjects.name, SUM(sessions.minutes), COUNT(*)
    FROM sessions
    JOIN subjects ON sessions.subject_id = subjects.id
    GROUP BY subjects.id, subjects.name
    ORDER BY SUM(sessions.minutes) DESC, subjects.name ASC
    """
    cursor = connection.execute(select_sql_subjects)
    return cursor.fetchall()
