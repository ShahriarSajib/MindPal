# database.py
import sqlite3
from langchain_core.messages import HumanMessage, AIMessage

DB_NAME = "mindpal_history.db"

def init_db():
    """Initializes schema to handle multi-session tracking persistently."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions (session_id) ON DELETE CASCADE
            )
        """)
        conn.commit()

def save_message(session_id: str, role: str, content: str):
    """Saves an incoming dialog entry permanently."""
    init_db()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO sessions (session_id) VALUES (?)", (session_id,))
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        conn.commit()

def load_all_sessions():
    """Builds the session history state array directly out of SQLite logs."""
    init_db()
    data = {}
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT session_id FROM sessions")
        for (sid,) in cursor.fetchall():
            cursor.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC", (sid,))
            langchain_msgs = []
            for role, content in cursor.fetchall():
                if role == "assistant":
                    langchain_msgs.append(AIMessage(content=content))
                else:
                    langchain_msgs.append(HumanMessage(content=content))
            data[sid] = langchain_msgs
    return data

def delete_session_from_db(session_id: str):
    """Deletes an isolated session thread completely."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        conn.commit()

def clear_all_db():
    """Wipes the database cleanly."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages")
        cursor.execute("DELETE FROM sessions")
        conn.commit()