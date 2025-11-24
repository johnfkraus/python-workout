import logging
import sys, os
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")


def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler


def get_file_handler(log_file_name):
   file_handler = TimedRotatingFileHandler(
      log_file_name,
      when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler


def get_logger(logger_name, log_file_name, log_level=logging.INFO):
   logger = logging.getLogger(logger_name)
   logger.setLevel(log_level) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler(log_file_name))
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger


def main():
   logger = get_logger(os.path.basename(__file__), "test_log", logging.INFO)
   logger.info("an INFO message")
   logger.error("an ERROR message")


if __name__ == "__main__":
   main()
