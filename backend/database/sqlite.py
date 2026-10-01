"""
SQLite Database Layer for OIBTC
Local, zero-dependency persistence for student tutoring sessions and chat history.
"""

import json
import os
import sqlite3
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "oibtc.db")


def get_connection() -> sqlite3.Connection:
    """Ensure database directory exists and return an active SQLite connection."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize SQLite database tables with proper indexing."""
    conn = get_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                grade_level INTEGER NOT NULL DEFAULT 9,
                subject_code TEXT NOT NULL DEFAULT 'ICT',
                subject_name_bn TEXT NOT NULL DEFAULT 'তথ্য ও যোগাযোগ প্রযুক্তি',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                query_text TEXT,
                response_text TEXT,
                sources_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_chat_messages_session 
            ON chat_messages(session_id, created_at);
        """)
    conn.close()
    print(f"SQLite database initialized successfully at: {DB_PATH}")


def create_session(grade: int = 9, subject: str = "ICT", subject_bn: str = "তথ্য ও যোগাযোগ প্রযুক্তি") -> str:
    """Create a new tutoring session and return its UUID."""
    session_id = str(uuid.uuid4())
    conn = get_connection()
    with conn:
        conn.execute(
            "INSERT INTO sessions (id, grade_level, subject_code, subject_name_bn) VALUES (?, ?, ?, ?)",
            (session_id, grade, subject, subject_bn)
        )
    conn.close()
    return session_id


def add_message(
    session_id: str,
    sender: str,
    query_text: str,
    response_text: str,
    sources: Optional[List[Dict[str, Any]]] = None
) -> str:
    """Store a conversational turn (question + answer + citation sources)."""
    msg_id = str(uuid.uuid4())
    sources_str = json.dumps(sources or [], ensure_ascii=False)
    conn = get_connection()
    with conn:
        conn.execute(
            """
            INSERT INTO chat_messages (id, session_id, sender, query_text, response_text, sources_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (msg_id, session_id, sender, query_text, response_text, sources_str)
        )
    conn.close()
    return msg_id


def get_history(session_id: str) -> List[Dict[str, Any]]:
    """Retrieve full conversation history for a given session."""
    conn = get_connection()
    cursor = conn.execute(
        """
        SELECT id, sender, query_text, response_text, sources_json, created_at
        FROM chat_messages
        WHERE session_id = ?
        ORDER BY created_at ASC
        """,
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    history = []
    for r in rows:
        history.append({
            "id": r["id"],
            "sender": r["sender"],
            "query": r["query_text"],
            "response": r["response_text"],
            "sources": json.loads(r["sources_json"]) if r["sources_json"] else [],
            "created_at": r["created_at"]
        })
    return history


if __name__ == "__main__":
    init_db()
    s_id = create_session(9, "ICT", "তথ্য ও যোগাযোগ প্রযুক্তি")
    add_message(s_id, "student", "পাসওয়ার্ড কী?", "পাসওয়ার্ড হলো গোপনীয় সংকেত।", [{"book": "ICT", "page": 20}])
    hist = get_history(s_id)
    print(f"Verified test session {s_id}: retrieved {len(hist)} turns.")
