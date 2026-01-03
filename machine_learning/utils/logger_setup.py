import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str = "TrackLogger", log_dir: str = ".", log_level: str = "INFO") -> logging.Logger:
    """
    Sets up a logger with both activity and error file handlers.
    
    Args:
        name: Name of the logger.
        log_dir: Directory where log files will be stored.
        log_level: Minimum logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
        
    Returns:
        Configured logger.
    """
    # Convert log_level argument to uppercase and get corresponding level
    log_level = log_level.upper()
    level_dict = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    # Ensure the log_level is valid
    if log_level not in level_dict:
        raise ValueError(f"Invalid log level: {log_level}. Must be one of {', '.join(level_dict.keys())}.")
    
    logger = logging.getLogger(name)
    
    if logger.handlers:  # Prevent adding duplicate handlers
        return logger

    logger.setLevel(level_dict[log_level])

    os.makedirs(log_dir, exist_ok=True)

    # Activity logger
    activity_handler = RotatingFileHandler(
        os.path.join(log_dir, "activity.log"),
        maxBytes=1_000_000,
        backupCount=5
    )
    activity_handler.setLevel(logging.INFO)
    activity_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Error logger
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, "errors.log"),
        maxBytes=1_000_000,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Console logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level_dict[log_level])  # Show log level dynamically in the console
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger.addHandler(activity_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger
