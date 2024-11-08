import sqlite3
from flask import g

DATABASE = 'audio_data.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with open('schema.sql') as f:
        db.executescript(f.read())

def save_audio_url(audio_url):
    db = get_db()
    db.execute('INSERT INTO audio (url) VALUES (?)', (audio_url,))
    db.commit()