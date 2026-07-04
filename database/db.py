import sqlite3
import datetime
from config.settings import STORAGE_CHANNEL

DB_PATH = "mars_cloud.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            joined TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS files (
            token TEXT PRIMARY KEY,
            user_id INTEGER,
            username TEXT,
            file_id TEXT,
            message_id INTEGER,
            channel_id INTEGER,
            file_name TEXT,
            file_size INTEGER,
            upload_time TEXT,
            download_count INTEGER DEFAULT 0
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS banned (
            user_id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------- USER FUNCTIONS ----------
def add_user(user_id, username):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (user_id, username, joined) VALUES (?, ?, ?)",
                    (user_id, username, datetime.datetime.now().isoformat()))
        conn.commit()
    conn.close()

# ---------- FILE FUNCTIONS ----------
def save_file(user_id, username, token, file_id, message_id, file_name, file_size):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO files (token, user_id, username, file_id, message_id, channel_id, file_name, file_size, upload_time, download_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    ''', (token, user_id, username, file_id, message_id, STORAGE_CHANNEL, file_name, file_size, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_file_by_token(token):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM files WHERE token = ?", (token,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_files(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM files WHERE user_id = ? ORDER BY upload_time DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def increment_download(token):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE files SET download_count = download_count + 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def delete_file_by_token(token):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM files WHERE token = ?", (token,))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def search_files(query):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT token, file_name, user_id, upload_time FROM files WHERE file_name LIKE ? ORDER BY upload_time DESC", ('%' + query + '%',))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ---------- STATS FUNCTIONS ----------
def get_total_users():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_total_files():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM files")
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_today_uploads():
    today = datetime.datetime.now().date().isoformat()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM files WHERE upload_time LIKE ?", (today + '%',))
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_total_storage():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT SUM(file_size) FROM files")
    row = cur.fetchone()
    total = row[0] if row[0] else 0
    conn.close()
    return total

# ---------- BAN FUNCTIONS ----------
def ban_user(user_id):
    conn = get_db()
    conn.execute("INSERT OR IGNORE INTO banned (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def unban_user(user_id):
    conn = get_db()
    conn.execute("DELETE FROM banned WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def is_banned(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM banned WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row is not None

def get_banned_users():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM banned")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]

def get_all_users(limit=50, offset=0):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, joined FROM users ORDER BY joined DESC LIMIT ? OFFSET ?", (limit, offset))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]
