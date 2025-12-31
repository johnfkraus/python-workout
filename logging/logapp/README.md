
export PYTHONPATH="/home/john/projects:$PYTHONPATH"

from myapp.logger import SingletonLogger

run:

Increment version number in setup.py, then

pip install -e .

from logapp.logger import SingletonLogger


Below is a complete, production-ready **package/module structure** with:

✔ A **singleton logger**
✔ **Daily log rotation**
✔ **Colored terminal output** (using `colorlog`)
✔ **Configurable via YAML OR JSON**
✔ A clean Python **package layout**
✔ A `main.py` demonstrating usage

This is ready to drop into a real project.

---

# 📁 Project Structure

```
myapp/
│
├── myapp/
│   ├── __init__.py
│   ├── logger.py
│   ├── config_loader.py
│   └── main.py
│
├── config/
│   ├── logging.yaml
│   └── logging.json
│
└── requirements.txt
```

---

# 📦 requirements.txt

```
pyyaml
colorlog
```

---

# 📁 config/logging.yaml  (Recommended)

```yaml
logfile:
  directory: logs
  filename: app.log
  rotate_when: midnight
  backup_count: 7

console:
  level: INFO

file:
  level: DEBUG
```

---

# 📁 config/logging.json (Alternative)

```json
{
  "logfile": {
    "directory": "logs",
    "filename": "app.log",
    "rotate_when": "midnight",
    "backup_count": 7
  },
  "console": {
    "level": "INFO"
  },
  "file": {
    "level": "DEBUG"
  }
}
```

---

# 📁 myapp/config_loader.py

Loads YAML or JSON config automatically.

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import yaml


def load_config(config_dir: str = "config") -> Dict[str, Any]:
    """
    Loads logging configuration from YAML or JSON.
    Prefers YAML if both exist.
    """
    config_path_yaml = Path(config_dir) / "logging.yaml"
    config_path_json = Path(config_dir) / "logging.json"

    if config_path_yaml.exists():
        with config_path_yaml.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    if config_path_json.exists():
        with config_path_json.open("r", encoding="utf-8") as f:
            return json.load(f)

    raise FileNotFoundError("No logging.yaml or logging.json found in 'config/'")
```

---

# 📁 myapp/logger.py

Contains the singleton logger with color support.

```python
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
```

---

# 📁 myapp/main.py

```python
from __future__ import annotations
from logging import Logger

from .logger import SingletonLogger


def main() -> None:
    logger: Logger = SingletonLogger.get_logger()

    logger.info("Application started.")
    logger.debug("Debug message example.")
    logger.warning("Warning example.")
    logger.error("Error example.")
    logger.critical("Critical example.")

    # Demonstrating singleton behavior
    same_logger = SingletonLogger.get_logger()
    logger.info(f"Logger objects identical? {logger is same_logger}")


if __name__ == "__main__":
    main()
```

---

# ✔ Features Included

### ✔ **Singleton Logger**

Only one global logger instance across the whole app.

### ✔ **Daily Log Rotation**

Uses `TimedRotatingFileHandler`.

### ✔ **Config file support**

Automatically loads `logging.yaml` or `logging.json`.

### ✔ **Colorized console output**

Uses `colorlog` for nice, readable output.

### ✔ **Strong Type Annotations**

Every module is fully typed for Python 3.11+.

---

# Want more?

I can also add:

* JSON-formatted logs
* Structured logging (with `structlog`)
* Async logging or queue-based logging
* A full CLI entrypoint (`python -m myapp`)
* Unit tests (pytest) for logger and config loader
* A logging middleware for FastAPI or Flask

Just tell me!
