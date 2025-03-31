# -*- coding: utf-8 -*-
"""
Folder Monitoring Script

Monitors a folder and triggers an alert if the size exceeds a set threshold.
"""

import os
import requests
import logging
import time
import configparser

# Resolve BASE_DIR (move up two directories from script location)
try:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
except NameError:
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "../.."))  # Fallback for Jupyter

# Define log directory and file path relative to BASE_DIR
LOG_DIR = os.path.join(BASE_DIR, "logs", "monitoring_scripts")
LOG_FILE = os.path.join(LOG_DIR, "m_temp_files_size_monitoring.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE, 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load configurations from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, "config.ini"))

# ✅ **Updated TEMP_FOLDER path to point to `data/temp`**
TEMP_FOLDER = os.path.join(BASE_DIR, "data", "temp")

# Ensure temp folder exists
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Log the resolved paths for debugging
logging.info(f"Resolved TEMP_FOLDER path: {TEMP_FOLDER}")
logging.info(f"Resolved LOG_DIR path: {LOG_DIR}")

# Load threshold and alert URL from config.ini
SIZE_LIMIT_MB = config.getfloat("Settings", "SIZE_LIMIT_MB", fallback=5)  # Default 5 MB
FLASK_ALERT_URL = config.get("Settings", "FLASK_ALERT_URL", fallback="http://localhost:5006/alert")  # Updated port to 5006

def get_folder_size(folder):
    """Calculate folder size in MB."""
    try:
        total_size = sum(os.path.getsize(os.path.join(folder, f)) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)))
        return total_size / (1024 * 1024)  # Convert bytes to MB
    except Exception as e:
        logging.error(f"Error calculating folder size: {e}")
        return 0

def monitor_folder():
    print(f"🚀 Folder monitoring script started... Watching: {TEMP_FOLDER}")
    logging.info(f"🚀 Folder monitoring script started... Watching: {TEMP_FOLDER}")

    """Continuously monitor the folder size."""
    if not os.path.exists(TEMP_FOLDER):
        logging.error(f"Folder does not exist: {TEMP_FOLDER}")
        return

    logging.info(f"Monitoring folder: {TEMP_FOLDER}")

    while True:
        folder_size = get_folder_size(TEMP_FOLDER)
        logging.info(f"Current folder size: {folder_size:.2f} MB")

        if folder_size > SIZE_LIMIT_MB:
            logging.warning(f"Folder size exceeded {SIZE_LIMIT_MB} MB! Sending alert...")

            # Send alert to Flask server
            alert_data = {
                "status": "firing",
                "message": f"Temp folder size exceeded {SIZE_LIMIT_MB} MB"
            }
            try:
                response = requests.post(FLASK_ALERT_URL, json=alert_data, timeout=5)
                if response.status_code == 200:
                    logging.info(f"Alert sent successfully: {response.json()}")
                else:
                    logging.error(f"Alert failed. Status Code: {response.status_code}, Response: {response.text}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to send alert: {e}")

        time.sleep(20)  # Check every 20 seconds

if __name__ == "__main__":
    monitor_folder()
