import logging
import sys
import os
from pathlib import Path

default_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def create_std_out_logger(name, level=logging.INFO):
    handler = create_std_out_handler(level)
    handler.setFormatter(default_formatter)

    logger = logging.getLogger(name) # crete new logger if not exist
    logger.addHandler(handler)

    return logger

def create_std_out_handler(level=logging.INFO):
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    return handler

def create_file_and_std_out_logger(name, log_file, level=logging.INFO):
    handler = create_file_handler(log_file, level)
    handler.setFormatter(default_formatter)

    std_out_handler = create_std_out_handler(level)
    std_out_handler.setFormatter(default_formatter)

    logger = logging.getLogger(name) # crete new logger if not exist
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(std_out_handler)

    return logger

def create_file_handler(log_file, level=logging.INFO):
    # Create parent folders if not exist
    Path(os.path.dirname(log_file)).mkdir(parents=True, exist_ok=True)

    # Create file if not exist
    with open(log_file, "w+"):
        pass

    handler = logging.FileHandler(log_file)
    handler.setLevel(level)
    return handler

file_and_std_out_logger = create_file_and_std_out_logger("file_and_std_out_logger", "log/info.log", logging.INFO)

# For logging during development
# std_out_logger = create_std_out_logger("std_out_logger", logging.INFO)

def log(msg):
    file_and_std_out_logger.info(msg)
    # std_out_logger.info(msg)