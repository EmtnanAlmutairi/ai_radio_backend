-- schema.sql
DROP TABLE IF EXISTS audio;

CREATE TABLE audio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL
);