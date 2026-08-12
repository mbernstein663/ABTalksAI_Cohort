

import sqlite3
from pathlib import Path


db_path = Path(
    r"C:\Users\micro\Documents\ABTalksAI-Cohort\data\coverage.db"
)


with sqlite3.connect(db_path) as conn:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS token_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            input_tokens INTEGER NOT NULL,
            output_tokens INTEGER NOT NULL,
            estimated_cost REAL NOT NULL
        );
        """)