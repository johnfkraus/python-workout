import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from threading import Lock


class SingletonLogger:
    _instance = None
    _lock = Lock()   # ensures thread-safe singleton

    @classmethod
    def get_logger(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls._create_logger()
            return cls._instance

    @staticmethod
    def _create_logger():
        logger = logging.getLogger("AppLogger")
        logger.setLevel(logging.DEBUG)

        # Prevent multiple handler additions if re-imported
        if logger.handlers:
            return logger

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "app.log"

        # --- Terminal Handler ---
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(console_format)

        # --- Daily Rotating File Handler ---
        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="midnight",
            interval=1,
            backupCount=7,        # keep last 7 days
            encoding="utf-8",
            utc=False,
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_format)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger


# -------------------------------------------------------------------
# Example Usage
# -------------------------------------------------------------------

def main():
    logger = SingletonLogger.get_logger()

    logger.info("Application started.")
    logger.debug("Debug message example.")
    logger.warning("Warning example.")
    logger.error("Error example.")

    # Demonstrate singleton behavior
    same_logger = SingletonLogger.get_logger()
    logger.info(f"Logger objects are identical: {logger is same_logger}")


if __name__ == "__main__":
    main()
