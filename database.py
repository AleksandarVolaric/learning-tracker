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



def get_sessions_by_subject(connection, subject):
    where_sql_subject = """
    SELECT id, area, subject, topic, minutes, date, notes
    FROM sessions
    WHERE subject = ?
    """
    cursor = connection.execute(where_sql_subject, (subject,))
    return cursor.fetchall()

def get_sessions_by_area(connection, area):
    where_sql_area = """
    SELECT id, area, subject, topic, minutes, date, notes
    FROM sessions
    WHERE area = ?
    """
    cursor = connection.execute(where_sql_area, (area,))
    return cursor.fetchall()

def get_sessions_by_date(connection, date):
    where_sql_date = """
    SELECT id, area, subject, topic, minutes, date, notes
    FROM sessions
    WHERE date = ?
    """
    cursor = connection.execute(where_sql_date, (date,))
    return cursor.fetchall()


def get_sessions_oldest_first(connection):
    select_sql_asc = """
    SELECT id, area, subject, topic, minutes, date, notes
    FROM sessions
    ORDER BY date ASC
    """
    cursor = connection.execute(select_sql_asc)
    return cursor.fetchall()

def get_sessions_newest_first(connection):
    select_sql_desc = """
    SELECT id, area, subject, topic, minutes, date, notes
    FROM sessions
    ORDER BY date DESC
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
    SELECT subject, SUM(minutes), COUNT(*)
    FROM sessions
    GROUP BY subject
    ORDER BY SUM(minutes) DESC
    """
    cursor = connection.execute(select_sql_subjects)
    return cursor.fetchall()

