import sqlite3
from pathlib import Path
from typing import Dict

DB_PATH = Path("database") / "app.db"


def get_connection() -> sqlite3.Connection:
    db_path = Path(DB_PATH)

    # Ensure directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))  # str() improves Windows compatibility
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            experience_level TEXT,
            score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def save_analysis(analysis: Dict, score: int) -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO analyses (role, experience_level, score)
        VALUES (?, ?, ?)
        """,
        (
            analysis.get("role"),
            analysis.get("experience_level"),
            score,
        ),
    )

    conn.commit()
    conn.close()
