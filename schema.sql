CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    area TEXT NOT NULL,
    subject_id INTEGER NOT NULL,
    topic TEXT NOT NULL,
    minutes INTEGER NOT NULL CHECK (minutes > 0),
    date TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);
