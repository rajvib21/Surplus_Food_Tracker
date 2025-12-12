import sqlite3
from pathlib import Path

DB_FILE = Path("data/db.sqlite3")
DB_FILE.parent.mkdir(exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT CHECK(role IN ('admin','user'))
    );

    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        quantity REAL,
        unit TEXT,
        latitude REAL,
        longitude REAL,
        image_path TEXT,
        is_claimed INTEGER DEFAULT 0,
        posted_at TEXT
    );

    CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        saved_kg REAL,
        updated_at TEXT
    );
    """)

    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
                    ("admin", "admin123", "admin"))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database Initialized!")
