import os
from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route("/")
def home():
    return "Telegram Bot is running!"


def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    Thread(target=run).start()
