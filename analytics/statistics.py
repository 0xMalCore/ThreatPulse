import sqlite3
from datetime import datetime, timedelta

DB_PATH = "data/attackers.db"

def get_attack_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ip, timestamp FROM attacks")
    rows = cursor.fetchall()
    conn.close()
    return rows

def detect_bruteforce(window_minutes=1, threshold=5):
    rows = get_attack_data()
    suspicious_ips = {}

    now = datetime.now()

    for ip, timestamp in rows:
        attack_time = datetime.fromisoformat(timestamp)
        if now - attack_time <= timedelta(minutes=window_minutes):
            suspicious_ips[ip] = suspicious_ips.get(ip, 0) + 1

    flagged = {ip: count for ip, count in suspicious_ips.items() if count >= threshold}
    return flagged

def risk_score(attempts):
    if attempts >= 8:
        return "HIGH"
    elif attempts >= 5:
        return "MEDIUM"
    else:
        return "LOW"
