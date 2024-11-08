-- schema.sql
DROP TABLE IF EXISTS audio;

CREATE TABLE audio (
    id SERIAL PRIMARY KEY,
    generated_text TEXT NOT NULL,
    audio_url TEXT NOT NULL
);