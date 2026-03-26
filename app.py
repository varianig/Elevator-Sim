from flask import Flask, jsonify, render_template
import threading
from main import getState, run_simulation

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state")
def state():
    return jsonify(getState())

# Run simulation in background thread
threading.Thread(target=run_simulation, daemon=True).start()

app.run(host="0.0.0.0", port=5000, debug=True)