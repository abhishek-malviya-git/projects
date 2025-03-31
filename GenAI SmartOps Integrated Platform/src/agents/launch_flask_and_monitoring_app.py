import os
import subprocess
import time
import json
import requests  # Validate Flask server


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

FLASK_SERVER_SCRIPT = os.path.join(BASE_DIR, "src", "agents", "flask_alert_receiver_agent.py")
MONITORING_SCRIPT = os.path.join(BASE_DIR, "scripts", "monitoring_scripts", "m_temp_files_size_monitoring.py")
FLASK_SERVER_URL = "http://127.0.0.1:5006/health"  # Ensure Flask server has this endpoint!

def start_process(script_path):
    """Start a script as a separate process."""
    return subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Start the Monitoring App
print("Starting Monitoring App...")
monitoring_process = start_process(MONITORING_SCRIPT)
time.sleep(2)  # Allow monitoring to initialize
print("Folder Monitoring Start...")
# Start the Flask Server
print("Starting Flask Server...")
flask_process = start_process(FLASK_SERVER_SCRIPT)

time.sleep(10)

url = "http://127.0.0.1:5006/alert"
headers = {"Content-Type": "application/json"}
data = {"status": "firing", "message": "What is my system memory usage?!"}

response = requests.post(url, headers=headers, data=json.dumps(data))

#print("Response Code:", response.status_code)
#print("Response Body:", response.json())

# Validate Flask server startup
if response.status_code==200:
    print("Flask Server is running at http://127.0.0.1:5006/ and is ready to receive requests!")
else:
    print("Flask Server did not start properly. Check logs for issues.")

# Keep the processes running
try:
    flask_process.wait()
    monitoring_process.wait()
except KeyboardInterrupt:
    print(" Stopping processes...")
    flask_process.terminate()
    monitoring_process.terminate()