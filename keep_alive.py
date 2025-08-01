from flask import Flask, request
from threading import Thread

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200

def keep_alive():
    # t = Thread(target=run)
    # t.start()

    thread = Thread(target=lambda: app.run(host='0.0.0.0', port=8080))
    thread.start()