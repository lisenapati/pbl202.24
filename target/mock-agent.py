import requests
import random
import time
import uuid
from datetime import datetime, timedelta, timezone

HOST = "http://127.0.0.1:5000"

BROWSERS = ["chrome", "firefox", "edge"]
OS_OPTIONS = ["Windows 10", "Windows 11", "Linux Mint", "Ubuntu 22.04", "macOS Ventura", "macOS Sonoma"]
SITES = [
    ("https://facebook.com", "Facebook"),
    ("https://gmail.com", "Gmail"),
    ("https://github.com", "GitHub"),
    ("https://linkedin.com", "LinkedIn"),
    ("https://youtube.com", "YouTube"),
    ("https://reddit.com", "Reddit"),
    ("https://twitter.com", "Twitter"),
]

def random_history():
    now = datetime.now(timezone.utc)
    return [
        {
            "url": url,
            "title": title,
            "visit_time": (now - timedelta(minutes=random.randint(1, 500))).isoformat(),
            "browser_type": random.choice(BROWSERS)
        } for url, title in random.sample(SITES, k=random.randint(2, 5))
    ]

def random_credentials():
    return [
        {
            "website": url,
            "username": f"user{random.randint(1000,9999)}",
            "password": f"{random.choice(['hunter2', 'pass123', 'qwerty', 'letmein'])}{random.randint(0,99)}",
            "browser_type": random.choice(BROWSERS)
        } for url, _ in random.sample(SITES, k=random.randint(1, 4))
    ]

def simulate_agent():
    machine_id = str(uuid.uuid4())
    hostname = f"lab-{random.randint(1000,9999)}"
    ip_address = f"192.168.1.{random.randint(10, 200)}"
    os_info = random.choice(OS_OPTIONS)

    # Register
    reg_payload = {
        "machine_id": machine_id,
        "hostname": hostname,
        "ip_address": ip_address,
        "os_info": os_info
    }
    try:
        r1 = requests.post(f"{HOST}/register", json=reg_payload)
        print(f"[+] {hostname} registered: {r1.status_code}")

        time.sleep(0.5)

        # Send History
        hist_payload = {
            "machine_id": machine_id,
            "history": random_history()
        }
        r2 = requests.post(f"{HOST}/submit/history", json=hist_payload)
        print(f"[+] {hostname} sent history: {r2.status_code}")

        time.sleep(0.5)

        # Send Credentials
        cred_payload = {
            "machine_id": machine_id,
            "credentials": random_credentials()
        }
        r3 = requests.post(f"{HOST}/submit/credentials", json=cred_payload)
        print(f"[+] {hostname} sent credentials: {r3.status_code}")

    except requests.RequestException as e:
        print(f"[!] Error with {hostname}: {e}")

if __name__ == "__main__":
    AGENTS = 5  # Number of mock agents to simulate

    for _ in range(AGENTS):
        simulate_agent()
        time.sleep(random.uniform(0.3, 1.0))
