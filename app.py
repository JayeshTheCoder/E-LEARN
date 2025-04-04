from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Course Recommendation Route
@app.route("/run_script", methods=["POST"])
def run_script():
    """
    Run the external script for course recommendations.
    """
    # Run the external script and capture its output
    result = subprocess.run(['python', 'run_script.py'], capture_output=True, text=True)

    try:
        # Parse the JSON output from the script
        output = json.loads(result.stdout)
        return jsonify(output)  # Return the parsed JSON as a response
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode the script output as JSON"})

# Chat Route
@app.route('/chat', methods=['POST'])
def chat():
    """
    Delegate chatbot functionality to chatbot.py.
    """
    from chatbot import handle_chat
    return handle_chat(request)

# Main Entry Point
if __name__ == "__main__":
    app.run(debug=True)