import logging
import sys
from pathlib import Path

def setup_logger(name="trading_bot", log_file="trading_bot.log"):
    """
    Architects dual-stream logging (Console + Permanent rotating file).
    Allows cleaner CLI UI without losing strict verbose records.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if logger already initialized in current scope
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. Console Handler (Less noisy, uses rich internally instead in CLI, so disable info stream temporarily)
    # Kept primarily for direct code-reuse outside of Click/Typer
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.WARNING)
    ch.setFormatter(formatter)

    # 2. File Handler (Holds all API response JSON blobs for audit trailing)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

# Singleton initialization
logger = setup_logger()
