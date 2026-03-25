from flask import Flask, request, render_template, send_from_directory
import json
from datetime import datetime
import os

app = Flask(__name__, template_folder='.', static_folder='.')

DATA_FILE = "storage/data.json"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "GET":
        return render_template("message.html")

    data = {
        "username": request.form.get("username"),
        "message": request.form.get("message")
    }

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            all_messages = json.load(f)
    else:
        all_messages = {}

    timestamp = str(datetime.now())
    all_messages[timestamp] = data

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_messages, f, indent=2, ensure_ascii=False)

    return "Message saved!"


@app.route("/read")
def read():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)
    return render_template("read.html", messages=messages)


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html"), 404


@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory(".", path)


app.run(port=3000)