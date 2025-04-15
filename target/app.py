from flask import Flask, render_template, send_from_directory

SCRIPT_DIR = 'installer/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = SCRIPT_DIR

@app.route("/")
def notnetflix():
    return render_template("")

@app.route("/download")
def download_page():
    return render_template("")

@app.route("/download/<name>")
def download_scripts(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

if __name__ == "__main__":
    with app.app_context():
        app.run(host="0.0.0.0", port=5000)
