from flask import Flask, jsonify
from flask_cors import CORS
import subprocess  # To run the external Python script
import json  # To parse the JSON output

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/run_script", methods=["POST"])
def run_script():
    # Run the external script and capture its output
    result = subprocess.run(['python', 'run_script.py'], capture_output=True, text=True)

    try:
        # Parse the JSON output from the script
        output = json.loads(result.stdout)
        return jsonify(output)  # Return the parsed JSON as a response
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode the script output as JSON"})

if __name__ == "__main__":
    app.run(debug=True)
