from flask import Flask, render_template, request
import subprocess
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Route to serve the test.html page
@app.route('/')
def index():
    return render_template('test.html')

# Route to run the Python script when the form is submitted
@app.route('/run-script', methods=['POST'])
def run_script():
    # This assumes 'python3' is the correct command to run your Python script
    # If you need to use a different Python path, adjust accordingly.
    result = subprocess.run(['python3', 'run_script.py'], capture_output=True, text=True)
    
    # Capture the output from the script
    output = result.stdout
    
    # Return the output to the user (this can be adjusted as needed)
    return f"<h1>Script Output:</h1><pre>{output}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
