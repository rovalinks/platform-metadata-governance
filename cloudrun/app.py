from flask import Flask

from dispatcher import Dispatcher

app = Flask(__name__)


@app.get("/")
def root():
    return Dispatcher.dispatch("health")


@app.get("/health")
def health():
    return Dispatcher.dispatch("health")


@app.get("/discover")
def discover():
    return Dispatcher.dispatch("discover")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)