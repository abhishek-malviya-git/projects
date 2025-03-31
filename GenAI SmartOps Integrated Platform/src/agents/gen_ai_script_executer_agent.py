import os
import re
import faiss
import subprocess
import numpy as np
import logging
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from script_intent_matcher_agent import ScriptIntentMatcher

# Load API key from .env
load_dotenv()
api_key = os.getenv("openai_api_key")

if not api_key:
    raise ValueError("API key is missing! Set it in the .env file.")

try:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
except NameError:
    # Fallback for interactive environments like Jupyter
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "../.."))

# Update log directory path
LOG_DIR = os.path.join(BASE_DIR, "logs", "gen_ai_script_executer_agent_scripts")
LOG_FILE = os.path.join(LOG_DIR, "gen_ai_script_executer_agent.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class gen_ai_script_executer:
    """Agent to execute scripts dynamically based on AI-powered intent matching."""

    def __init__(self, api_key):
        self.scripts_path = os.path.join(BASE_DIR, "scripts", "execution_scripts")
        self.matcher = ScriptIntentMatcher(api_key)  # Use FAISS for script matching
  
    def execute_script(self, query):
        """Determines the best script based on query intent using FAISS."""
        script_name = self.matcher.find_best_script(query)
        logging.info(f" Query: {query}")
        logging.info(f" Relevant script found in script_intent_matcher_agent.py : {script_name}")
        print("Script Name - ", script_name)

        if script_name == "No relevant script found.":
            logging.warning(" No relevant script found for the query.")
            return " No relevant script found for the query."

        return self.run_script_with_query_params(script_name, query)

    def run_script_with_query_params(self, script_name, query):
        """Execute the Ansible script with query parameters."""
        script_path = os.path.join(self.scripts_path, script_name)
        logging.info(f" Execution Script_path: {script_path}")

        # Check if the script exists
        if not os.path.exists(script_path):
            logging.error(f" Error: Script '{script_name}' not found at {script_path}")
            return f" Error: Script '{script_name}' not found."

        try:
            logging.info(f" Executing Script: {script_path}")       
            result = subprocess.run(
                ["python", script_path, query],
                capture_output=True,
                text=True,
                check=True
            )

            logging.info(f" Script Execution Output:\n{result.stdout}")
            return result.stdout.strip() if result.stdout else " No output generated."

        except subprocess.CalledProcessError as e:
            logging.error(f" Subprocess Error: {e}\nstderr Output: {e.stderr}")
            return f" Error executing script: {e}"

        except Exception as e:
            logging.error(f" Unexpected Error: {str(e)}")
            return f" Error executing script: {str(e)}"

# ---  MAIN FUNCTION TO TEST THE SCRIPT EXECUTOR ---
def main():
    """Tests the AI-powered script executor with different queries."""
    agent = gen_ai_script_executer(api_key)

    test_queries = [
         "Can you troubleshoot server WIN1234YATS? "
    ]

    for query in test_queries:
        print("\n==============================")
        print(f" Query: {query}")
        result = agent.execute_script(query)
        print(f" Matched Script Execution Output:\n{result}")
        print("==============================")

if __name__ == "__main__":
    main()
