import sqlite3
import os

# ---------------------------------------------------------
# DATABASE PATH
# ---------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


# ---------------------------------------------------------
# CONNECT TO DATABASE
# ---------------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # return dictionary-like rows
    return conn


# ---------------------------------------------------------
# INITIALIZE DATABASE (CREATE TABLES IF NOT EXISTS)
# ---------------------------------------------------------
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # ----------------------------
    # USERS TABLE
    # ----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)

    # ----------------------------
    # CHAT HISTORY TABLE
    # ----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# RUN INIT WHEN FILE IMPORTS
# ---------------------------------------------------------
init_db()
