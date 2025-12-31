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

