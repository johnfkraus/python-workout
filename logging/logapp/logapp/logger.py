from __future__ import annotations

import logging
from logging import Logger, Handler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from threading import Lock
from typing import Dict, Any

from colorlog import ColoredFormatter

from .config_loader import load_config


class SingletonLogger:
    _instance: Logger | None = None
    _lock: Lock = Lock()

    @classmethod
    def get_logger(cls) -> Logger:
        """Return the singleton logger instance."""
        with cls._lock:
            if cls._instance is None:
                config = load_config()
                cls._instance = cls._create_logger(config)
            return cls._instance

    @staticmethod
    def _create_logger(config: Dict[str, Any]) -> Logger:
        logger: Logger = logging.getLogger("AppLogger")

        if logger.handlers:
            return logger  # avoid re-adding handlers

        logger.setLevel(logging.DEBUG)

        # Load config values
        log_dir = Path(config["logfile"]["directory"])
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / config["logfile"]["filename"]
        rotate_when = config["logfile"]["rotate_when"]
        backup_count = config["logfile"]["backup_count"]
        console_level = getattr(logging, config["console"]["level"])
        file_level = getattr(logging, config["file"]["level"])

        # --- Colored Console Handler ---
        console_handler: Handler = logging.StreamHandler()
        console_handler.setLevel(console_level)

        console_format = ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        console_handler.setFormatter(console_format)

        # --- Rotating File Handler ---
        file_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(
            filename=str(log_file),
            when=rotate_when,
            interval=1,
            backupCount=backup_count,
            encoding="utf-8",
            utc=False,
        )
        file_handler.setLevel(file_level)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
        )

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger


