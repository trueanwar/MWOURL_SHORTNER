import sqlite3
import config

def connect():
    return sqlite3.connect(config.DATABASE)

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id TEXT PRIMARY KEY,
        url TEXT,
        user_id INTEGER,
        clicks INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

def save_link(id, url, user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO links (id,url,user_id) VALUES (?,?,?)",
        (id, url, user_id)
    )

    conn.commit()
    conn.close()

def get_link(id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT url FROM links WHERE id=?",
        (id,)
    )

    data = cur.fetchone()

    conn.close()

    return data

def add_click(id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE links SET clicks = clicks + 1 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

def user_links(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id,url,clicks FROM links WHERE user_id=?",
        (user_id,)
    )

    data = cur.fetchall()

    conn.close()

    return data
