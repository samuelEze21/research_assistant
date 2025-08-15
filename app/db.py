import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "research.db")  # fallback if not in .env

def init_db():
    conn = sqlite3.connect(DB_URL)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            output TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_result(query, output):
    conn = sqlite3.connect(DB_URL)
    conn.execute(
        "INSERT INTO searches (query, output, timestamp) VALUES (?, ?, ?)",
        (query, output, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
