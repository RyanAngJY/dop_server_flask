import logging
import sys
import os
from pathlib import Path

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_std_out_logger(name, level=logging.INFO):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name) # crete new logger if not exist
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def setup_file_logger(name, log_file, level=logging.INFO):
    # Create parent folders if not exist
    Path(os.path.dirname(log_file)).mkdir(parents=True, exist_ok=True)

    # Create file if not exist
    with open(log_file, "w+"):
        pass

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name) # crete new logger if not exist
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

file_logger = setup_file_logger("file_logger", "log/info.log", logging.INFO)

# For logging during development
std_out_logger = setup_std_out_logger("std_out_logger", logging.INFO)

def log(msg):
    file_logger.info(msg)
    std_out_logger.info(msg)