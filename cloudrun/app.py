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

@app.get("/compliance")
def compliance_endpoint():
    return Dispatcher.dispatch("compliance")

@app.get("/enforce")
def enforce_endpoint():

    return Dispatcher.dispatch("enforce")

@app.get("/verify")
def verify_endpoint():

    return Dispatcher.dispatch("verify")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)