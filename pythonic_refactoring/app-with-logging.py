import my_logging
from pathlib import Path

LOG_FILE_NAME = Path("app-with-logging.log")

my_logger = my_logging.get_logger("app-with-logging", log_file_name=LOG_FILE_NAME)

my_logger.error("Hello World!")
