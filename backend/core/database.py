import os
import sqlite3
from typing import List, Tuple
from dotenv import load_dotenv
# We are using sqlite3 with vector extension theoretically provided by libsql.
# Since we are setting up locally, standard sqlite3 won't have vector by default unless loaded.
# For this MVP, we'll use a mocked vector DB or setup a basic sqlite implementation if using libsql-experimental

load_dotenv()

LIBSQL_URL = os.getenv("LIBSQL_URL", "file:./local.db")
LIBSQL_AUTH_TOKEN = os.getenv("LIBSQL_AUTH_TOKEN", "")

def get_connection():
    """
    Returns a connection to either a remote Turso database or a local SQLite file.
    """
    is_remote = LIBSQL_URL.startswith("libsql://") or LIBSQL_URL.startswith("https://") or LIBSQL_URL.startswith("wss://")
    
    if is_remote:
        import libsql_experimental
        # Use Turso remote connection
        conn = libsql_experimental.connect(
            database=LIBSQL_URL, 
            auth_token=LIBSQL_AUTH_TOKEN
        )
    else:
        # Strip file:./ if present for local sqlite usage
        db_path = LIBSQL_URL.replace("file:./", "") if "file:./" in LIBSQL_URL else LIBSQL_URL
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        
    return conn
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create visitors table for lead capture
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create a table for scraped knowledge
    # Note: In a real Turso DB, you would create a vector index. 
    # Here we simulate the structure.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def record_visitor_email(email: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO visitors (email) VALUES (?)", (email,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error recording email: {e}")
        return False

# Initialize the DB on import
init_db()
