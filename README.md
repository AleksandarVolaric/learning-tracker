# Personal Learning Tracker

A small command-line project for learning how Python communicates with SQLite.
This project is being built one version at a time as a learning exercise.

## Current version: v0.2.0

The program lets you choose to add a learning session or view all saved
sessions. It uses a local SQLite database named `learning.db`.

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

## Run the program

Python 3 is required. SQLite support is included with Python's standard
library, so no additional database package is needed.

From this project folder, run:

```text
python main.py
```

The `learning.db` file is created in the current working directory if it does
not already exist. Use a SQLite database viewer, such as DB Browser for SQLite,
to view the rows in the `sessions` table.

## Learning goals

This project practices the Python-to-SQLite flow:

1. Collect values with Python's `input()`.
2. Open a database connection with `sqlite3.connect()`.
3. Execute SQL to create a table, insert a row, and select rows.
4. Pass insert values separately using SQL `?` placeholders.
5. Use `fetchall()` and a Python loop to display database rows.
6. Save changes with `commit()` and close the connection.

Update, delete, filtering, sorting, statistics, and relational tables are not
implemented yet.
