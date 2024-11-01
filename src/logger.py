import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_dir = os.path.join(os.getcwd(), "logs")
try:
    os.makedirs(logs_dir, exist_ok=True)
    print(f"Logs directory created at: {logs_dir}")
except Exception as e:
    print(f"Error creating logs directory: {e}")

LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)
print(f"Log file will be created at: {LOG_FILE_PATH}")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

if __name__ == "__main__":
    logging.info("Logging is started")
    print("Logging setup is complete. Check the logs directory for the log file.")
