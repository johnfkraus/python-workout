
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
# LOG_FILE = "my_app2.log"

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler


def get_file_handler(log_file_name):
   file_handler = TimedRotatingFileHandler(log_file_name, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler


def get_logger(logger_name, log_file_name):
   print(f"{log_file_name=}")
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler(log_file_name))
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger


def main():
   my_logger = get_logger("my module name", LOG_FILE)
   my_logger.debug("a debug message")

if __name__ == "__main__":
   main()
