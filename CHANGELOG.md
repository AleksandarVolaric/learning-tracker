# Changelog

## v0.7.0

- Added a `subjects` table and linked sessions to subjects with a foreign key.
- Added `schema.sql` and enabled SQLite foreign-key enforcement per connection.
- Updated session queries and subject statistics to use SQL `JOIN`.
- Added numbered subject selection and an option to add a subject when needed.
- Simplified database initialization and added numbered subject filtering.

## v0.6.0

- Added overall statistics for total learning sessions and total minutes.
- Added per-subject statistics for total time and session count.

## v0.5.0

- Added session filters by subject, area, and date using SQL `WHERE`.
- Added newest-first and oldest-first session ordering using SQL `ORDER BY`.

## v0.4.1

- Organized the application into `main.py`, `database.py`, and `validation.py`.
- Added a numbered main menu and numbered edit-field menu.

## v0.4.0

- Added confirmed session deletion using SQL `DELETE`.

## v0.3.0

- Added editing of session fields using SQL `UPDATE`.

## v0.2.0

- Added viewing saved sessions using SQL `SELECT`.

## v0.1.0

- Added and persistently saved learning sessions using SQLite.
