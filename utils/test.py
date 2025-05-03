import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger_setup import setup_logger
logger = setup_logger("TrackLogger", log_dir="logs", log_level="DEBUG")

try:
    raise ValueError("Test exception for logging.")
except Exception as e:
    logger.error("[ERROR] Something went wrong", exc_info=True)
