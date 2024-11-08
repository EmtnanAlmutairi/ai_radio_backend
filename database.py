import os
import psycopg2
from flask import g
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with open('schema.sql') as f:
        db.cursor().execute(f.read())
        db.commit()

def save_audio_data(generated_text, audio_url):
    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO audio (generated_text, audio_url) VALUES (%s, %s)', (generated_text, audio_url))
    db.commit()

def fetch_prompts():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT prompt FROM prompts')  # جدول "prompts" في قاعدة البيانات
    rows = cur.fetchall()
    return [row[0] for row in rows]  # ارجع قائمة بالنصوص