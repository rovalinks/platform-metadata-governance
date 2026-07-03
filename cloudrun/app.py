from flask import (
    Flask,
    request,
)

from dispatcher import Dispatcher

app = Flask(__name__)


@app.post("/")
def greenfield_endpoint():
    return Dispatcher.dispatch(
        "greenfield",
        request.get_json(),
    )


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


@app.get("/runs")
def runs_endpoint():
    return Dispatcher.dispatch("runs")
    
    
@app.get("/plan")
def plan_endpoint():
    return Dispatcher.dispatch("plan")


@app.get("/execute")
def execute_endpoint():
    return Dispatcher.dispatch("execute")


@app.get("/enforce")
def enforce_endpoint():
    return Dispatcher.dispatch("enforce")


@app.get("/verify")
def verify_endpoint():
    return Dispatcher.dispatch("verify")


@app.get("/report")
def report_endpoint():
    return Dispatcher.dispatch("report")


@app.get("/history")
def history_endpoint():
    return Dispatcher.dispatch("history")


@app.get("/dashboard")
def dashboard_endpoint():
    return Dispatcher.dispatch("dashboard")


@app.get("/metrics")
def metrics_endpoint():
    return Dispatcher.dispatch("metrics")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
    )