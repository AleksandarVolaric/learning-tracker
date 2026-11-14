# Personal Learning Tracker

A small command-line project for learning how Python communicates with SQLite.
This project is being built one version at a time as a learning exercise.

## Current version: v0.4.1

The program uses a local SQLite database named `learning.db`. Its numbered
menu lets you add a learning session, view all saved sessions, edit any field
of an existing session, delete a session, or exit.

The code is organized by responsibility: `main.py` handles the menu and
user-facing flows, `database.py` contains SQLite operations, and
`validation.py` contains reusable input checks.

When adding a session, it collects:

- Area (for example, School or Private)
- Subject
- Topic
- Minutes spent
- Date in `YYYY-MM-DD` format
- Optional notes

The program creates the `sessions` table if it does not already exist. It
checks that the required text fields are not blank, that minutes is a positive
whole number, and that the date is valid. It then inserts the session using
parameterized SQL, commits the change, and closes the database connection.

When viewing sessions, the program uses SQL `SELECT` to retrieve all rows,
`fetchall()` to return them to Python, and a loop to display each session in
the terminal. If there are no saved sessions, it displays a message.

When editing a session, the program asks for its ID and uses `fetchone()` to
check whether that session exists. If found, the user can choose to update its
area, subject, topic, minutes, date, or notes. Each change uses a parameterized
SQL `UPDATE` with `WHERE id = ?` so only the selected session is changed. The
update is committed to the database. The numbered edit menu also offers a
cancel option.

When deleting a session, the program asks for its ID and checks whether it
exists. If found, it displays the session and asks for confirmation. A
confirmed deletion uses parameterized SQL `DELETE` with `WHERE id = ?` so only
the selected session is removed. The change is committed; if the ID does not
exist or the user cancels, no session is deleted.

## Run the program

Python 3 is required. SQLite support is included with Python's standard
library, so no additional database package is needed.

From this project folder, run:

```text
python main.py
```

Choose an action by entering its menu number: 1 to add, 2 to view, 3 to edit,
4 to delete, or 5 to exit.

The `learning.db` file is created in the current working directory if it does
not already exist. Use a SQLite database viewer, such as DB Browser for SQLite,
to view the rows in the `sessions` table.

## Learning goals

This project practices the Python-to-SQLite flow:

1. Collect values with Python's `input()`.
2. Open a database connection with `sqlite3.connect()`.
3. Execute SQL to create a table, insert, select, update, and delete rows.
4. Use `WHERE` conditions to target a specific row during updates and deletes.
5. Pass values separately using SQL `?` placeholders.
6. Use `fetchone()` and `fetchall()` to retrieve rows, and loop through results.
7. Save changes with `commit()` and close the connection cleanly on exit.

Filtering, sorting, statistics, and relational tables are not implemented yet.
