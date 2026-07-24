import sqlite3

def create_database():
    conn = sqlite3.connect("monitor.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT,
        url TEXT,
        status TEXT,
        code INTEGER,
        message TEXT,
        date TEXT
    )
    """)
    conn.commit()
    conn.close()

def guardar_en_database(log):
    conn = sqlite3.connect("monitor.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO logs
    (service, url, status, code, message, date)
    VALUES(?, ?, ?, ?, ?, ?)
    """, (
        log.get("service"),
        log.get("url"),
        log.get("status"),
        log.get("code"),
        log.get("message"),
        log.get("date")
    ))
    conn.commit()
    conn.close()