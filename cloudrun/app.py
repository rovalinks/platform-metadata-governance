from flask import Flask

from dispatcher import Dispatcher

app = Flask(__name__)


@app.get("/")
def root():

    return Dispatcher.dispatch()


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8080)