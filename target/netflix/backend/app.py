from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/download')
def download():
    return jsonify({"message": "File downloaded successfully."})

if __name__ == '__main__':
    app.run(debug=True)
