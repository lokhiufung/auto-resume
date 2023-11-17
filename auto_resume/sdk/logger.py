import logging


LOGGING_DIR = './logs'
import os

if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)


def parse_level(level: str):
    level = level.lower()
    if level == 'info':
        level = logging.INFO
    elif level == 'error':
        level = logging.ERROR
    elif level == 'warning':
        level = logging.WARNING
    else:
        level = logging.DEBUG
    return level


def get_logger(name, logger_lv='debug'):
    # Create a logger object with the name "my_logger"
    logger = logging.getLogger(name)

    # Set the logging level
    logger_lv = parse_level(logger_lv)
    logger.setLevel(logger_lv)
    
    # Create a handler for logging to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_lv)

    # Create a handler for logging to a file
    file_handler = logging.FileHandler(os.path.join(LOGGING_DIR, f'{name}.log'))
    file_handler.setLevel(logger_lv)

    # Create a formatter for the log messages
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
