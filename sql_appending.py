import sqlite3

PATH = r"C:\Users\micro\Documents\ABTalksAI-Cohort\data"
db_path = PATH + r"\coverage.db"

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            session_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp DATETIME
        )
    """)

    conn.commit()