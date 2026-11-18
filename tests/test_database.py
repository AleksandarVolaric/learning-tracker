import sqlite3

import pytest

from database import (
    add_session,
    delete_session,
    get_all_sessions,
    get_learning_totals,
    get_or_create_subject,
    get_session_by_id,
    get_sessions_by_area,
    get_sessions_by_date,
    get_sessions_by_subject,
    get_sessions_newest_first,
    get_sessions_oldest_first,
    get_subject_statistics,
    initialize_database,
    update_session_field,
)


@pytest.fixture
def connection():
    test_connection = sqlite3.connect(":memory:")
    test_connection.execute("PRAGMA foreign_keys = ON")
    initialize_database(test_connection)
    yield test_connection
    test_connection.close()


def test_subject_is_created_once_and_names_are_unique(connection):
    subject_id = get_or_create_subject(connection, "Python")
    same_subject_id = get_or_create_subject(connection, "Python")

    subject_count = connection.execute(
        "SELECT COUNT(*) FROM subjects"
    ).fetchone()[0]

    assert subject_id == same_subject_id
    assert subject_count == 1

    with pytest.raises(sqlite3.IntegrityError):
        connection.execute("INSERT INTO subjects (name) VALUES (?)", ("Python",))


def test_add_and_read_session_returns_subject_name(connection):
    subject_id = get_or_create_subject(connection, "Python")
    add_session(
        connection,
        "Private",
        subject_id,
        "SQLite joins",
        45,
        "2026-11-18",
        "Practiced JOIN queries",
    )

    sessions = get_all_sessions(connection)
    session_id = sessions[0][0]

    assert len(sessions) == 1
    assert sessions[0] == (
        session_id,
        "Private",
        "Python",
        "SQLite joins",
        45,
        "2026-11-18",
        "Practiced JOIN queries",
    )
    assert get_session_by_id(connection, session_id) == sessions[0]
    assert get_session_by_id(connection, -1) is None


def test_update_changes_only_the_selected_session(connection):
    python_id = get_or_create_subject(connection, "Python")
    sql_id = get_or_create_subject(connection, "SQL")
    add_session(connection, "Private", python_id, "First topic", 30, "2026-11-18", "")
    add_session(connection, "School", sql_id, "Second topic", 60, "2026-11-17", "")

    sessions = get_all_sessions(connection)
    first_session_id = next(row[0] for row in sessions if row[3] == "First topic")
    second_session_id = next(row[0] for row in sessions if row[3] == "Second topic")

    update_session_field(connection, "minutes", 90, first_session_id)
    update_session_field(connection, "subject", sql_id, first_session_id)

    first_session = get_session_by_id(connection, first_session_id)
    second_session = get_session_by_id(connection, second_session_id)

    assert first_session[2] == "SQL"
    assert first_session[4] == 90
    assert second_session[2] == "SQL"
    assert second_session[4] == 60
    assert second_session[1] == "School"


def test_delete_removes_selected_session(connection):
    subject_id = get_or_create_subject(connection, "Python")
    add_session(connection, "Private", subject_id, "Keep", 30, "2026-11-18", "")
    add_session(connection, "School", subject_id, "Delete", 60, "2026-11-17", "")
    sessions = get_all_sessions(connection)
    deleted_session_id = next(row[0] for row in sessions if row[3] == "Delete")

    delete_session(connection, deleted_session_id)

    assert get_session_by_id(connection, deleted_session_id) is None
    assert len(get_all_sessions(connection)) == 1
    assert get_all_sessions(connection)[0][3] == "Keep"


def test_filters_and_date_sorting(connection):
    python_id = get_or_create_subject(connection, "Python")
    sql_id = get_or_create_subject(connection, "SQL")
    add_session(connection, "Private", python_id, "Newer", 30, "2026-11-18", "")
    add_session(connection, "School", sql_id, "Older", 60, "2026-11-16", "")
    add_session(connection, "Private", python_id, "Middle", 45, "2026-11-17", "")

    assert {
        row[3] for row in get_sessions_by_subject(connection, python_id)
    } == {"Newer", "Middle"}
    assert {row[3] for row in get_sessions_by_area(connection, "Private")} == {
        "Newer",
        "Middle",
    }
    assert [row[3] for row in get_sessions_by_date(connection, "2026-11-16")] == [
        "Older"
    ]
    assert [row[3] for row in get_sessions_oldest_first(connection)] == [
        "Older",
        "Middle",
        "Newer",
    ]
    assert [row[3] for row in get_sessions_newest_first(connection)] == [
        "Newer",
        "Middle",
        "Older",
    ]


def test_learning_totals_and_subject_statistics(connection):
    python_id = get_or_create_subject(connection, "Python")
    sql_id = get_or_create_subject(connection, "SQL")
    add_session(connection, "Private", python_id, "Basics", 120, "2026-11-18", "")
    add_session(connection, "Private", python_id, "SQLite", 90, "2026-11-17", "")
    add_session(connection, "School", sql_id, "SELECT", 60, "2026-11-16", "")

    assert get_learning_totals(connection) == (3, 270)
    assert get_subject_statistics(connection) == [
        ("Python", 210, 2),
        ("SQL", 60, 1),
    ]


def test_foreign_key_rejects_missing_subject_and_join_returns_name(connection):
    python_id = get_or_create_subject(connection, "Python")
    add_session(connection, "Private", python_id, "JOIN", 45, "2026-11-18", "")

    session = get_all_sessions(connection)[0]
    assert session[2] == "Python"
    assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1

    with pytest.raises(sqlite3.IntegrityError):
        add_session(connection, "Private", -1, "Invalid subject", 30, "2026-11-18", "")
