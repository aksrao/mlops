import logging
import os
from datetime import datetime

# Creating the directory to store the logs
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR,exist_ok=True)

# make sure to save the logs to that particular day
LOG_FLIE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename= LOG_FLIE,
    format= '%(asctime)s - %(levelname)s - %(message)s',
    level= logging.INFO
)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger