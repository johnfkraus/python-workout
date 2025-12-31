import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from threading import Lock


class LoggerBuilder:
    def __init__(self):
        # Defaults
        self._name = "app"
        self._level = logging.INFO
        self._log_dir = Path("logs")
        self._filename = "app.log"
        self._when = "midnight"      # daily rotation
        self._interval = 1
        self._backup_count = 7
        self._fmt = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        self._datefmt = "%Y-%m-%d %H:%M:%S"
        self._console_level = None   # None => same as logger level

    # Builder methods (fluent interface)
    def name(self, name: str):
        self._name = name
        return self

    def level(self, level: int):
        self._level = level
        return self

    def log_dir(self, log_dir: str | Path):
        self._log_dir = Path(log_dir)
        return self

    def filename(self, filename: str):
        self._filename = filename
        return self

    def rotation(self, when: str = "midnight", interval: int = 1, backup_count: int = 7):
        self._when = when
        self._interval = interval
        self._backup_count = backup_count
        return self

    def format(self, fmt: str, datefmt: str | None = None):
        self._fmt = fmt
        if datefmt is not None:
            self._datefmt = datefmt
        return self

    def console_level(self, level: int | None):
        self._console_level = level
        return self

    def build(self) -> logging.Logger:
        """
        Create and configure the logger instance (not yet singleton-wrapped).
        """
        self._log_dir.mkdir(parents=True, exist_ok=True)
        log_path = self._log_dir / self._filename

        logger = logging.getLogger(self._name)
        logger.setLevel(self._level)
        logger.propagate = False  # avoid duplicate logs if root logger has handlers

        # Clear any existing handlers to allow re-building cleanly
        if logger.handlers:
            logger.handlers.clear()

        formatter = logging.Formatter(self._fmt, self._datefmt)

        # File handler with timed rotation
        file_handler = TimedRotatingFileHandler(
            filename=str(log_path),
            when=self._when,
            interval=self._interval,
            backupCount=self._backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(self._level)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(self._console_level or self._level)
        logger.addHandler(console_handler)

        return logger


class SingletonLogger:
    """
    Singleton façade around a configured logging.Logger.
    """
    _instance: logging.Logger | None = None
    _lock = Lock()

    @classmethod
    def configure(cls, builder: LoggerBuilder) -> logging.Logger:
        """
        Configure (or reconfigure) the singleton logger using a builder.
        """
        with cls._lock:
            logger = builder.build()
            cls._instance = logger
            return logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Get the singleton logger instance, creating a default one if needed.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    # Default configuration if none was provided
                    default_builder = LoggerBuilder()
                    cls._instance = default_builder.build()
        return cls._instance


# Example usage
if __name__ == "__main__":
    # Build and configure singleton logger
    builder = (
        LoggerBuilder()
        .name("my_app")
        .level(logging.DEBUG)
        .log_dir("logs")
        .filename("my_app.log")
        .rotation(when="midnight", interval=1, backup_count=14)
        .format("%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s")
        .console_level(logging.INFO)
    )

    logger = SingletonLogger.configure(builder)

    logger.debug("Debug message (file only, not console)")
    logger.info("Info message (file and console)")
    logger.error("Error message (file and console)")
