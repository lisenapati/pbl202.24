import requests
import random
import time
import uuid

HOST = "http://127.0.0.1:5000"
MACHINE_ID = str(uuid.uuid4())

def register():
    payload = {
        "machine_id": MACHINE_ID,
        "hostname": f"lab-{random.randint(1000,9999)}",
        "ip_address": f"192.168.1.{random.randint(10,200)}",
        "os_info": random.choice(["Linux", "Windows 11", "macOS Ventura"])
    }
    r = requests.post(f"{HOST}/register", json=payload)
    print("Registered:", r.status_code)

def submit_history():
    payload = {
        "machine_id": MACHINE_ID,
        "history": [
            {"url": "https://example.com", "title": "Example", "visit_time": "2025-04-06T12:00:00", "browser_type": "chrome"},
            {"url": "https://github.com", "title": "GitHub", "visit_time": "2025-04-06T12:05:00", "browser_type": "firefox"}
        ]
    }
    r = requests.post(f"{HOST}/submit/history", json=payload)
    print("History:", r.status_code)

def submit_credentials():
    payload = {
        "machine_id": MACHINE_ID,
        "credentials": [
            {"website": "https://facebook.com", "username": "john.doe", "password": "hunter2", "browser_type": "chrome"},
            {"website": "https://gmail.com", "username": "jane.doe", "password": "pass1234", "browser_type": "firefox"}
        ]
    }
    r = requests.post(f"{HOST}/submit/credentials", json=payload)
    print("Credentials:", r.status_code)

if __name__ == "__main__":
    register()
    time.sleep(1)
    submit_history()
    time.sleep(1)
    submit_credentials()
