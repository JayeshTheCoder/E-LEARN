from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess  # To run the external Python script

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/run_script", methods=["POST"])
def run_script():
    # Run the external script and capture its output
    result = subprocess.run(['python', 'run_script.py'], capture_output=True, text=True)

    # Prepare the response data
    response = {
        "message": result.stdout.strip()  # Get the output from the script
    }

    return jsonify(response)  # Return a JSON response

if __name__ == "__main__":
    app.run(debug=True)
