from flask import Flask, request, jsonify
import logging
import os
import sys
from gen_ai_script_executer_agent import gen_ai_script_executer
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("openai_api_key")

if not api_key:
    raise ValueError("API key is missing! Set it in the .env file.")

app = Flask(__name__)

# Define log directory and log file path
LOG_DIR = "./logs/alert_handler_scripts"
LOG_FILE = os.path.join(LOG_DIR, "webhook_alerts.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Setup logging to write logs to the new path
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize the script executor agent with the API key
script_executor = gen_ai_script_executer(api_key=api_key)

@app.route("/", methods=["GET"])
def home():
    return "Flask Alert Receiver is running!"

@app.route('/alert', methods=['POST'])
def handle_alert():
    """Receive alerts and trigger the GenAI Script Executor Agent."""
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({"error": "Invalid request. Expected JSON with 'message' key"}), 400  

    alert_message = data["message"]
    
    # Log received alert
    logging.info(f"Received Alert: {alert_message}")

    # Trigger the GenAI script execution
    try:
        execution_result = script_executor.execute_script(alert_message)

        # Log execution details
        logging.info(f"Execution Output: {execution_result}")

        response = {
            "status": "success",
            "alert_message": alert_message,
            "execution_result": execution_result
        }
    except Exception as e:
        logging.error(f"Error executing script: {e}")
        response = {
            "status": "error",
            "alert_message": alert_message,
            "error": str(e)
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5006, debug=True)
