import json
import os
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path) as f:
        return json.load(f)

def get_settings_dir():
    return Path(__file__).parent.parent / "settings"

def get_logs_dir():
    return Path(__file__).parent.parent / "logs"
