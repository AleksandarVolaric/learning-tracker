# Personal Learning Tracker

A small command-line project for learning how Python communicates with SQLite.
This project is being built one version at a time as a learning exercise.

## Current version: v0.7.0

The program uses a local SQLite database named `learning.db`. Its numbered
menu lets you add a learning session, view all saved sessions, edit any field
of an existing session, delete a session, filter or sort sessions, view
statistics, or exit.

The code is organized by responsibility: `main.py` handles the menu and
user-facing flows, `database.py` contains SQLite operations, `validation.py`
contains reusable input checks, and `schema.sql` defines the database tables.

When adding a session, it collects:

- Area (for example, School or Private)
- A subject selected from a numbered list
- Topic
- Minutes spent
- Date in `YYYY-MM-DD` format
- Optional notes

If the subject is not listed, the user can choose the final numbered option to
add it. An existing subject name is reused rather than added a second time.
The program checks that required text fields are not blank, minutes is a
positive whole number, and the date is valid. It then inserts the session
using parameterized SQL, commits the change, and closes the database
connection.

## Database structure

`schema.sql` defines two relational tables:

- `subjects`: one row per subject, with an integer primary key and a unique,
  required name.
- `sessions`: one row per learning session. Its `subject_id` is a required
  foreign key that references `subjects.id`.

This is a one-to-many relationship: one subject can be referenced by many
sessions. For example, several session rows can store the same `subject_id`
for Python, while the name `Python` is stored only once in `subjects`.

Session queries use a SQL `JOIN` between `sessions.subject_id` and
`subjects.id`. This lets the database store a subject ID while the CLI
continues to display its readable name. SQLite foreign-key enforcement is
enabled on every connection in `database.py`.

The application creates the tables from `schema.sql` when it starts. It does
not migrate older database formats. If you have a v0.6.0 database, back it up
if needed, then delete it before starting v0.7.0; this creates a fresh
relational database.

When viewing sessions, the program uses SQL `SELECT` to retrieve all rows,
`fetchall()` to return them to Python, and a loop to display each session in
the terminal. If there are no saved sessions, it displays a message.

When editing a session, the program asks for its ID and uses `fetchone()` to
check whether that session exists. If found, the user can choose to update its
area, subject, topic, minutes, date, or notes. Choosing a subject displays
numbered subject names; the application stores the chosen subject ID. Each
change uses a parameterized SQL `UPDATE` with `WHERE id = ?` so only the
selected session is changed. The update is committed to the database. The
numbered edit menu also offers a cancel option.

When deleting a session, the program asks for its ID and checks whether it
exists. If found, it displays the session and asks for confirmation. A
confirmed deletion uses parameterized SQL `DELETE` with `WHERE id = ?` so only
the selected session is removed. The change is committed; if the ID does not
exist or the user cancels, no session is deleted.

When filtering and sorting, the program can show sessions by subject, area, or
date using SQL `WHERE` queries. Subject filtering uses a numbered subject
choice and filters by its ID. It can also show newest-first or oldest-first
using SQL `ORDER BY date DESC` or `ORDER BY date ASC`.

When viewing statistics, the program shows the total number of sessions and
the total time spent learning. It also uses a `JOIN` and `GROUP BY` to show
the time spent and session count for each subject, ordered by total time, and
labels the most-studied subject.

## Run the program

Python 3 is required. SQLite support is included with Python's standard
library, so no additional database package is needed.

From this project folder, run:

```text
python main.py
```

Choose an action by entering its menu number: 1 to add, 2 to view, 3 to edit,
4 to delete, 5 to filter/sort, 6 to view statistics, or 7 to exit. The
filter/sort submenu offers filters by subject, area, and date, plus
newest-first and oldest-first sorting.

The `learning.db` file is created in the current working directory if it does
not already exist. Use a SQLite database viewer, such as DB Browser for SQLite,
to view the rows in the `sessions` table.

## Learning goals

This project practices the Python-to-SQLite flow:

1. Collect values with Python's `input()`.
2. Open a database connection with `sqlite3.connect()`.
3. Execute SQL to create a table, insert, select, update, and delete rows.
4. Use `WHERE` to filter rows and target specific rows during updates/deletes.
5. Use `ORDER BY` with `ASC` and `DESC` to sort dates.
6. Pass values separately using SQL `?` placeholders.
7. Use `fetchone()` and `fetchall()` to retrieve rows, and loop through results.
8. Save changes with `commit()` and close the connection cleanly on exit.
9. Use SQL aggregate functions such as `COUNT()` and `SUM()` with `GROUP BY`
   to summarize learning sessions.
10. Use primary keys, foreign keys, and a one-to-many relationship to
    normalize related data.
11. Use SQL `JOIN` to retrieve readable subject names from related tables.
