import logging
import json
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pathlib import Path

class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class StructuredLogger:

    def __init__(self, name: str, log_dir: str = "logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        log_file = self.log_dir / f"notionos_x.log"

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.events = []

    def log_event(self, event_type: str, component: str, message: str,
                  data: Optional[dict] = None, level: str = "INFO"):
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "component": component,
            "message": message,
            "data": data or {},
            "level": level
        }

        self.events.append(event)

        level_color = {
            "DEBUG": "\033[36m",
            "INFO": "\033[32m",
            "WARNING": "\033[33m",
            "ERROR": "\033[31m",
        }
        reset = "\033[0m"

        color = level_color.get(level, reset)
        timestamp = event["timestamp"]

        print(f"{color}[{level}]{reset} {timestamp} | {component:20s} | {event_type:15s} | {message}")

        if data:
            print(f"  └─ Data: {json.dumps(data, indent=2)}")

    def info(self, component: str, message: str, data: Optional[dict] = None):
        self.logger.info(f"{component}: {message}")
        self.log_event("INFO", component, message, data, "INFO")

    def debug(self, component: str, message: str, data: Optional[dict] = None):
        self.logger.debug(f"{component}: {message}")
        self.log_event("DEBUG", component, message, data, "DEBUG")

    def warning(self, component: str, message: str, data: Optional[dict] = None):
        self.logger.warning(f"{component}: {message}")
        self.log_event("WARNING", component, message, data, "WARNING")

    def error(self, component: str, message: str, data: Optional[dict] = None):
        self.logger.error(f"{component}: {message}")
        self.log_event("ERROR", component, message, data, "ERROR")

    def critical(self, component: str, message: str, data: Optional[dict] = None):
        self.logger.critical(f"{component}: {message}")
        self.log_event("ERROR", component, message, data, "ERROR")

    def save_events_log(self):
        log_file = self.log_dir / "events.json"
        with open(log_file, 'w') as f:
            json.dump(self.events, f, indent=2)

_logger: Optional[StructuredLogger] = None

def get_logger(name: str = "NotionOS_X") -> StructuredLogger:
    global _logger
    if _logger is None:
        _logger = StructuredLogger(name)
    return _logger
