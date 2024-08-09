import sqlite3
import os
import tempfile
from flask import current_app
from contextlib import contextmanager

def get_db_path():
    # Use the system's temp directory
    db_dir = tempfile.gettempdir()
    return os.path.join(db_dir, 'residents.db')

@contextmanager
def get_db_connection():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

class ResidentBehavior:
    @staticmethod
    def create_db_if_not_exists():
        db_path = get_db_path()
        if not os.path.exists(db_path):
            open(db_path, 'w').close()
        ResidentBehavior.init_db()

    @staticmethod
    def init_db():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS resident_behavior (
                resident_id TEXT PRIMARY KEY,
                current_date TEXT NOT NULL,
                original_care_note TEXT NOT NULL,
                behavior_summary TEXT NOT NULL,
                behavior_intensity INTEGER NOT NULL
            )
            ''')
            conn.commit()

    @staticmethod
    def update_behavior(resident_id, current_date, original_care_note, behavior_summary, behavior_intensity):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT OR REPLACE INTO resident_behavior 
            (resident_id, current_date, original_care_note, behavior_summary, behavior_intensity)
            VALUES (?, ?, ?, ?, ?)
            ''', (resident_id, current_date, original_care_note, behavior_summary, behavior_intensity))
            conn.commit()

    @staticmethod
    def get_behavior(resident_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM resident_behavior WHERE resident_id = ?', (resident_id,))
            return cursor.fetchone()