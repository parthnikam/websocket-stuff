from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


DB_PATH = Path(__file__).with_name("messages.db")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def create_message(sender: str, content: str) -> dict[str, Any]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO messages (sender, content)
            VALUES (?, ?)
            """,
            (sender, content),
        )
        message_id = cursor.lastrowid
        connection.commit()

        row = connection.execute(
            """
            SELECT id, sender, content, created_at
            FROM messages
            WHERE id = ?
            """,
            (message_id,),
        ).fetchone()

    return dict(row)


def list_messages(limit: int = 100) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, sender, content, created_at
            FROM messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in reversed(rows)]
