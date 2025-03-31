import os
import logging
import json
import sys

# Define BASE_DIR (move two folders up from src/agents/)
try:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
except NameError:
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "../.."))  # Fallback for Jupyter

# Update log directory path
LOG_DIR = os.path.join(BASE_DIR, "logs", "execution_scripts", "e_delete_temp_files")
LOG_FILE = os.path.join(LOG_DIR, "e_delete_temp_files.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# Update TEMP_FOLDER path (Assuming it's inside `data/temp/`)
TEMP_FOLDER = os.path.join(BASE_DIR, "data", "temp")

# Ensure TEMP_FOLDER exists
os.makedirs(TEMP_FOLDER, exist_ok=True)

def format_response(query, folder_path, deleted_files):
    """Format the response message for better readability."""
    if not deleted_files:
        return f"Temporary folder is already empty, No Action Taken.\n\nFolder Path: {folder_path}\n"

    formatted_message = (
        f" Temporary Folder Cleanup Completed\n\n"
        f" Folder Path: {folder_path}\n"
        f" Total Files Deleted: {len(deleted_files)}\n\n"
        f" Deleted Files:\n" +
        "\n".join([f"   {index + 1}. {file}" for index, file in enumerate(deleted_files)])  # Adding numbering
    )

    return formatted_message

def delete_temp_files(query):
    """Delete files in the temp folder and return formatted details."""
    if not os.path.exists(TEMP_FOLDER):
        logging.error(f"Folder not found: {TEMP_FOLDER}")
        return {"status": "error", "message": f"Folder `{TEMP_FOLDER}` not found."}

    deleted_files = []
    for filename in os.listdir(TEMP_FOLDER):
        file_path = os.path.join(TEMP_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_files.append(filename)
        except Exception as e:
            logging.error(f"Error deleting {filename}: {e}")

    # Prepare formatted response
    response = format_response(query, TEMP_FOLDER, deleted_files)
    logging.info(json.dumps(response, indent=2, ensure_ascii=False))

    return response

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "No query provided"
    result = delete_temp_files(query)
    print(result)
