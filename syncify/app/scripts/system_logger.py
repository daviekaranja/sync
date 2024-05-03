import logging
from fastapi.logger import logger as fastapi_logger


class CustomLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logger = fastapi_logger
        self.logger.setLevel(logging.DEBUG)  # Set the log level as needed

        # Create file handler and set its formatter
        file_handler = logging.FileHandler(self.log_file)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Add stream handler for terminal output
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter('%(levelname)s:     %(message)s')
        stream_handler.setFormatter(stream_formatter)
        self.logger.addHandler(stream_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


logger = CustomLogger('app.log')
