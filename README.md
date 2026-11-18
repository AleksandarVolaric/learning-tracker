# Personal Learning Tracker

A beginner-friendly command-line project for practicing Python and SQLite.
Record learning sessions, organize them by subject, and review your learning
time from a local database.

## Features

- Add, view, edit, and delete learning sessions (full CRUD).
- Choose subjects from numbered lists, or add a new subject when needed.
- Filter sessions by subject, area, or date.
- Sort sessions by date, oldest first or newest first.
- View total sessions, total learning time, and time spent per subject.
- See which subject has the most recorded learning time.
- Use a relational SQLite schema with visible SQL `JOIN` queries.

## Database structure

The database has two tables, defined in `schema.sql`:

- `subjects`: stores each subject once. `id` is the primary key and `name` is
  required and unique.
- `sessions`: stores each learning session. `id` is its primary key, and
  `subject_id` is a required foreign key referencing `subjects.id`.

This is a one-to-many relationship: one subject can be linked to many
sessions. A session stores the subject ID, while queries use a SQL `JOIN` to
show the subject name in the application. SQLite foreign-key enforcement is
enabled when the application opens its database connection.

The application creates missing tables from `schema.sql` at startup. It does
not migrate older database formats. If upgrading a database from before
v0.7.0, back it up and create a fresh database before using this version.

## Project structure

```text
main.py          Numbered menu and application flows
database.py      SQLite connection and database queries
validation.py    Reusable checks for user input
schema.sql       Subjects and sessions table definitions
tests/
  test_database.py  Automated database tests
learning.db      Local database created when the application runs (ignored)
```

## Requirements

- Python 3
- Pytest to run the automated tests

The application uses Python's built-in `sqlite3` module; it has no external
runtime dependencies. Install pytest if it is not already available:

```text
python -m pip install pytest
```

## Run the application

From the project folder, run:

```text
python main.py
```

The numbered main menu lets you add, view, edit, delete, filter/sort sessions,
view statistics, or exit. For example, choose **1** to add a session, enter its
area, select a numbered subject (or add one), then enter the topic, minutes,
date, and optional notes. The application creates `learning.db` in the
project's current working directory if it does not exist.

## Run the tests

From the project folder, run:

```text
python -m pytest
```

The tests use a fresh in-memory SQLite database for each test. They do not
open, modify, or delete your personal `learning.db`.

## Technologies and learning goals

This project uses Python, SQLite, SQL, and pytest. It practices:

- Python functions, input handling, and a numbered command-line menu.
- SQL `INSERT`, `SELECT`, `UPDATE`, and `DELETE`.
- Parameterized queries, `WHERE`, and `ORDER BY`.
- Aggregate functions such as `COUNT()` and `SUM()`, with `GROUP BY`.
- Primary keys, foreign keys, and one-to-many relationships.
- SQL `JOIN` to retrieve readable data from related tables.
- Testing database functions with an isolated in-memory database.

## Privacy

`learning.db` is a local file containing your learning data and is ignored by
Git. The automated tests use only in-memory databases. Check `git status`
before publishing to ensure no personal database or other private data is
included.
