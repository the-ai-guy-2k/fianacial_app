import os
import json
from app.utils.logging_service import ErrorCategory, log_error, log_info

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CONFIG_FILE = os.path.join(ROOT, 'config.json')


class ConfigManager:
    def __init__(self):
        self.config = None
        self.errors = []
        self._load()

    def _load(self):
        if not os.path.exists(CONFIG_FILE):
            msg = log_error(ErrorCategory.CONFIG_ERROR, f"config.json not found at {CONFIG_FILE}")
            self.errors.append(msg)
            return
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as fh:
                self.config = json.load(fh)
            log_info(f"Config loaded from {CONFIG_FILE}")
        except Exception as e:
            msg = log_error(ErrorCategory.CONFIG_ERROR, "Failed to parse config.json", e)
            self.errors.append(msg)

    def get(self, key, default=None):
        if not self.config:
            return default
        keys = key.split('.')
        val = self.config
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                return default
        return val if val is not None else default

    def get_errors(self):
        return self.errors


# Global config instance
config = ConfigManager()
