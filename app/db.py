import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

DB_PATH = os.getenv("DB_PATH", "/app/data/chat.db")


def _conn():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with _conn() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                title      TEXT    NOT NULL,
                created_at TEXT    NOT NULL
            );
            CREATE TABLE IF NOT EXISTS messages (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL REFERENCES sessions(id),
                role       TEXT    NOT NULL,
                content    TEXT    NOT NULL,
                sources    TEXT    NOT NULL DEFAULT '[]',
                created_at TEXT    NOT NULL
            );
        """)


def create_session(title: str) -> int:
    with _conn() as con:
        cur = con.execute(
            "INSERT INTO sessions (title, created_at) VALUES (?, ?)",
            (title[:80], datetime.utcnow().isoformat()),
        )
        return cur.lastrowid


def get_sessions() -> list[dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT id, title, created_at FROM sessions ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def rename_session(session_id: int, title: str):
    with _conn() as con:
        con.execute("UPDATE sessions SET title = ? WHERE id = ?", (title[:80], session_id))


def delete_session(session_id: int):
    with _conn() as con:
        con.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        con.execute("DELETE FROM sessions WHERE id = ?", (session_id,))


def save_message(session_id: int, role: str, content: str, sources: list):
    with _conn() as con:
        con.execute(
            "INSERT INTO messages (session_id, role, content, sources, created_at) VALUES (?, ?, ?, ?, ?)",
            (session_id, role, content, json.dumps(sources), datetime.utcnow().isoformat()),
        )


def get_messages(session_id: int) -> list[dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT role, content, sources FROM messages WHERE session_id = ? ORDER BY id",
            (session_id,),
        ).fetchall()
        return [
            {"role": r["role"], "content": r["content"], "sources": json.loads(r["sources"])}
            for r in rows
        ]
