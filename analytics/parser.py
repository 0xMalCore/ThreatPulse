import sqlite3
from datetime import datetime
from analytics.geoip import get_country
import os

# 🔥 Use absolute path like dashboard
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "attackers.db")

print("Parser DB Path:", DB_PATH)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        username TEXT,
        password TEXT,
        protocol TEXT,
        country TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_attack(ip, username, password, protocol):
    try:
        print(f"[LOGGING] {ip} | {username} | {protocol}")

        country = get_country(ip)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO attacks (ip, username, password, protocol, country, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            ip,
            username,
            password,
            protocol,
            country,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

        print("[SUCCESS] Attack stored")

    except Exception as e:
        print(f"[ERROR] Failed to log attack: {e}")