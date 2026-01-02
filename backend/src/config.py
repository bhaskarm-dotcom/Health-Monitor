import json
import os
from pathlib import Path

# Get the project root directory (two levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"


def load_config(filename: str) -> dict:
    """Load configuration from JSON file."""
    config_path = CONFIG_DIR / filename
    with open(config_path, 'r') as f:
        return json.load(f)


def get_scoring_config() -> dict:
    """Load scoring configuration."""
    return load_config("scoring_config.json")


def get_ai_prompts() -> dict:
    """Load AI prompt templates."""
    return load_config("ai_prompts.json")


# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

