import logging

from flask import Flask, render_template, jsonify
from threading import Timer
from workflow import WorkflowState
from workflow.core.pipelines import Pipeline

# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.workflow = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["GET", "POST"])
def start_pipeline():
    app.workflow = Pipeline()
    if app.workflow._current_state is not WorkflowState.RUNNING:
        Timer(1, app.workflow.run).start()
    return jsonify(app.workflow.info())

@app.route("/state", methods=["GET", "POST"])
def state_pipeline():
    return jsonify(app.workflow.info())

if __name__ == "__main__":
    app.run(debug=True)