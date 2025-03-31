# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 21:24:29 2025

@author: Dell
"""

import os
import subprocess
import time

# Resolve base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# # Define script paths
FLASK_SERVER_SCRIPT = os.path.join(BASE_DIR, "src", "agents", "flask_alert_receiver_agent.py")  # Flask Server
MONITORING_SCRIPT = os.path.join(BASE_DIR, "scripts", "monitoring_scripts", "m_temp_files_size_monitoring.py")  # Monitoring App
GRADIO_APP_SCRIPT = os.path.join(BASE_DIR, "src", "agents", "GenAI_SmartOps_Integrated_Platform.py")  # Gradio App

# Function to start a script as a background process
def start_script(script_path, name):
    """Starts a Python script as a background process."""
    if not os.path.exists(script_path):
        print(f" Error: {name} script not found at {script_path}")
        return None
    
    if script_path == GRADIO_APP_SCRIPT:
        print(f" Starting {name}...")
        return subprocess.run(["python", GRADIO_APP_SCRIPT], check=True)
    else:
        print(f" Starting {name}...")
        return subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


#  Start Monitoring App
monitoring_process = start_script(MONITORING_SCRIPT, "Monitoring App")
time.sleep(5)  # Give some time to start

 # Start Flask server
flask_process = start_script(FLASK_SERVER_SCRIPT, "Flask Server")
time.sleep(15)  # Wait for Flask to initialize

# Start Gradio App
gradio_process = start_script(GRADIO_APP_SCRIPT, "Gradio App")


#print("\n All applications have been launched successfully!\n")

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down all processes...")

    # Terminate all processes
    for process in [monitoring_process,flask_process,gradio_process]:
        if process:
            process.terminate()
            process.wait()

    print(" All processes stopped.")
