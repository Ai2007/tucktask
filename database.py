import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path("analysis.db")


def init_db() -> None:
    """Create the analysis table if it does not already exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis (
                id      INTEGER PRIMARY KEY CHECK (id = 1),
                content TEXT    NOT NULL,
                updated_at TEXT DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()


def get_content() -> Optional[str]:
    """Return the stored markdown string, or None if the table is empty."""
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT content FROM analysis WHERE id = 1"
        ).fetchone()
    return row[0] if row else None


def set_content(content: str) -> None:
    """
    Insert or replace the single analysis row.
    SQLite's UPSERT keeps the table to exactly one row at all times.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO analysis (id, content, updated_at)
            VALUES (1, ?, datetime('now'))
            ON CONFLICT(id) DO UPDATE SET
                content    = excluded.content,
                updated_at = excluded.updated_at
            """,
            (content,),
        )
        conn.commit()
