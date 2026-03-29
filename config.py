import json
from pathlib import Path

class Config:

    BASE_DIR = Path(__file__).parent
    MEMORY_DIR = BASE_DIR / "memory"
    OUTPUT_DIR = BASE_DIR / "output"
    LOGS_DIR = BASE_DIR / "logs"

    MAX_PARALLEL_NODES = 5
    EXECUTION_TIMEOUT = 300

    QUALITY_THRESHOLD = 0.7
    CREATIVITY_THRESHOLD = 0.6
    PRACTICALITY_THRESHOLD = 0.75
    REFINEMENT_THRESHOLD = 0.7

    PLANNER_TIMEOUT = 10.0
    EXECUTOR_TIMEOUT = 30.0
    RESEARCHER_TIMEOUT = 15.0
    CRITIC_TIMEOUT = 5.0

    BROWSER_MAX_RESULTS = 10
    BROWSER_TIMEOUT = 10.0
    CODE_EXECUTION_TIMEOUT = 30.0

    NOTION_POLLING_INTERVAL = 5
    NOTION_APPROVAL_TIMEOUT = 300

    MAX_EPISODIC_ENTRIES = 1000
    MAX_STRATEGY_ENTRIES = 500

    @classmethod
    def init(cls):
        cls.MEMORY_DIR.mkdir(exist_ok=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)

    @classmethod
    def to_dict(cls):
        return {
            key: str(value) if isinstance(value, Path) else value
            for key, value in cls.__dict__.items()
            if not key.startswith('_') and key.isupper()
        }

Config.init()
