# Personal Learning Tracker

A small command-line project for learning how Python communicates with SQLite.
This project is being built one version at a time as a learning exercise.

## Current version: v0.1.0

The program asks for one learning session and saves it to a local SQLite
database named `learning.db`. It collects:

- Area (for example, School or Private)
- Subject
- Topic
- Minutes spent
- Date in `YYYY-MM-DD` format
- Optional notes

The program creates the `sessions` table if it does not already exist. It
checks that the required text fields are not blank, that minutes is a positive
whole number, and that the date is valid. It then inserts the session, commits
the change, and closes the database connection.

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

This version practices the basic Python-to-SQLite flow:

1. Collect values with Python's `input()`.
2. Open a database connection with `sqlite3.connect()`.
3. Execute SQL to create a table and insert a row.
4. Pass values separately using SQL `?` placeholders.
5. Save the transaction with `commit()`.
6. Close the connection.

Later roadmap items are not implemented yet.
