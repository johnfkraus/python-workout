

logging module for json parsing code.

Logs to both stdout and file.


In Python 3.11+, I want code for a logger.  The logger should write to both the terminal and to a log file.  The logger should autorotate log files daily.  The logger should be a singleton.  The example code should include a main() method that demonstrates how to use the logger.


Below is a clean, Python-3.11-compatible example of a **singleton logger** that:

✔ Logs to **both terminal and a file**
✔ **Auto-rotates daily** (using `TimedRotatingFileHandler`)
✔ Ensures **only one logger instance** exists
✔ Includes a **main() demo**

---

# ✅ `logger_singleton.py`

```python
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
```

---

# ✔ How It Works

### **Singleton behavior**

* `SingletonLogger.get_logger()` ensures the logger is created **once**, even across threads.

### **Auto-rotating log file**

* A new file is created **every midnight**.
* By default, it keeps **7 old logs** (change via `backupCount`).

### **Dual output**

* `StreamHandler` → prints to terminal
* `TimedRotatingFileHandler` → writes to daily log files

---

If you want enhancements (colored terminal output, async logging, JSON logs, etc.), just let me know!


Add type hints.

Below is the same logger implementation updated with **full type annotations** and still compatible with **Python 3.11+**.

---

# ✅ `logger_singleton.py` (with type hints)

```python
from __future__ import annotations

import logging
from logging import Logger, Handler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from threading import Lock


class SingletonLogger:
    _instance: Logger | None = None
    _lock: Lock = Lock()

    @classmethod
    def get_logger(cls) -> Logger:
        """Return the singleton application logger."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls._create_logger()
            return cls._instance

    @staticmethod
    def _create_logger() -> Logger:
        """Create and configure the singleton logger."""
        logger: Logger = logging.getLogger("AppLogger")
        logger.setLevel(logging.DEBUG)

        # Avoid adding handlers twice in environments like REPL or reloads
        if logger.handlers:
            return logger

        log_dir: Path = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file: Path = log_dir / "app.log"

        # --- Console Handler ---
        console_handler: Handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(console_format)

        # --- File Handler (Daily Rotation) ---
        file_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(
            filename=str(log_file),
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8",
            utc=False,
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_format)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger


# -------------------------------------------------------------------
# Example Usage
# -------------------------------------------------------------------

def main() -> None:
    logger: Logger = SingletonLogger.get_logger()

    logger.info("Application started.")
    logger.debug("Debug message example.")
    logger.warning("Warning example.")
    logger.error("Error example.")

    # Demonstrate singleton behavior
    same_logger: Logger = SingletonLogger.get_logger()
    logger.info(f"Logger objects are identical: {logger is same_logger}")


if __name__ == "__main__":
    main()
```

---

If you'd like, I can also:

* Wrap this in a package/module structure
* Add a configuration file (YAML/JSON)
* Add colored terminal logging
* Add async or queue-based logging (for high-throughput apps)

Just say the word!


* Wrap this in a package/module structure
* Add a configuration file (YAML/JSON)
* Add colored terminal logging

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



Google:


explain from __future__ import annotations

The statement from __future__ import annotations is a special directive that changes how Python interprets type annotations, allowing you to use features of newer Python versions in older ones. Specifically, it enables postponed evaluation of annotations as defined in PEP 563. 

What it Does

Without this future import, Python attempts to evaluate type annotations when the code is run (at "definition time"). This causes issues if a type name used in an annotation hasn't been defined yet, leading to a NameError. 
The from __future__ import annotations statement tells the Python compiler to: 
Treat all annotations as strings instead of evaluating them immediately at runtime.
Store these annotations in a dictionary that can be accessed later (e.g., by type-checking tools like Mypy) using functions like typing.get_type_hints(). 
Key Benefits
Solves the Forward Reference Problem: This is the primary reason for the import. You can use a class name as a type hint before the class has been defined in the file.
python
from __future__ import annotations # No NameError here

def get_my_instance() -> MyClass:
    # Code that uses MyClass instance
    pass

class MyClass:
    # Class definition
    pass
Use code with caution.

Breaks Circular Imports: In complex projects, two modules might need to import each other for type hints, creating a circular dependency. Treating hints as strings resolves this, as the actual definitions aren't needed at import time.
Enables Modern Syntax in Older Versions: It allows the use of newer, cleaner type hint syntax like the | (union) operator for multiple types (e.g., str | None instead of typing.Optional[str]), even in Python versions before 3.10. 
Future of the Feature
The behavior introduced by this statement (postponed evaluation) was planned to become the default in future Python versions, removing the need for the import. This change has been delayed multiple times and no final decision has been made on when it will become mandatory default behavior. 
For best practice and forward compatibility, it is currently recommended to add from __future__ import annotations to all your modules. 


