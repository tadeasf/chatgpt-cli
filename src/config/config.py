import os
from pathlib import Path
import yaml
from xdg_base_dirs import xdg_config_home
from typing import Any, Dict

BASE = Path(xdg_config_home(), "chatgpt-cli")
CONFIG_FILE = BASE / "config.yaml"
HISTORY_FILE = BASE / "history"
SAVE_FOLDER = BASE / "session-history"

DEFAULT_CONFIG = {
    "supplier": "anthropic",
    "openai_api_key": "<INSERT YOUR OPENAI API KEY HERE>",
    "anthropic_api_key": "<INSERT YOUR ANTHROPIC API KEY HERE>",
    "azure_api_key": "<INSERT YOUR AZURE API KEY HERE>",
    "gemini_api_key": "<INSERT YOUR GEMINI API KEY HERE>",
    "model": "claude-3-5-sonnet-20240620",
    "temperature": 0.7,
    "markdown": True,
    "easy_copy": True,
    "non_interactive": False,
    "json_mode": False,
    "use_proxy": False,
    "proxy": "socks5://127.0.0.1:2080",
    "openai_endpoint": "https://api.openai.com/v1",
    "anthropic_endpoint": "https://api.anthropic.com/v1",
    "gemini_endpoint": "https://generativelanguage.googleapis.com/v1beta",
    "azure_endpoint": "https://xxxx.openai.azure.com/",
    "azure_api_version": "2023-07-01-preview",
    "azure_deployment_name": "gpt-35-turbo",
    "azure_deployment_name_eb": "text-embedding-ada-002",
    "storage_format": "markdown",
    "embedding_model": "text-embedding-ada-002",
    "embedding_dimension": 1536,
    "max_context_tokens": 3500,
    "show_spinner": True,
    "max_tokens": 1024,
}

VALID_MODELS = {
    "anthropic": [
        "claude-3-opus-20240229",
        "claude-3-5-sonnet-20240620",
        "claude-3-haiku-20240307",
        "claude-2.1",
        "claude-2.0",
        "claude-instant-1.2",
    ],
    "openai": [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
    ],
    "gemini": [
        "gemini-1.5-flash",
    ],
}

PRICING_RATE = {
    "claude-3-opus-20240229": {"prompt": 15.00, "completion": 75.00},
    "claude-3-5-sonnet-20240620": {"prompt": 3.00, "completion": 15.00},
    "claude-3-haiku-20240307": {"prompt": 0.25, "completion": 1.25},
    "claude-2.1": {"prompt": 8.00, "completion": 24.00},
    "claude-2.0": {"prompt": 8.00, "completion": 24.00},
    "claude-instant-1.2": {"prompt": 0.80, "completion": 2.40},
    "gpt-4o": {"prompt": 5.00, "completion": 15.00},
    "gpt-4o-mini": {"prompt": 0.15, "completion": 0.60},
    "gpt-4-turbo": {"prompt": 0.35, "completion": 1.05},
    "gpt-4": {"prompt": 0.35, "completion": 1.05},
    "gpt-3.5-turbo": {"prompt": 0.35, "completion": 1.05},
    "dall-e": {"prompt": 0.50, "completion": 1.50},
    "tts": {"prompt": 0.50, "completion": 1.50},
    "whisper": {"prompt": 0.50, "completion": 1.50},
    "embeddings": {"prompt": 0.50, "completion": 1.50},
    "moderation": {"prompt": 0.50, "completion": 1.50},
    "gpt-base": {"prompt": 0.50, "completion": 1.50},
    "gemini-1.5-flash": {"prompt": 0.50, "completion": 1.50},
}


def load_config(config_file: str) -> Dict[str, Any]:
    if not Path(config_file).exists():
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, "w", encoding="utf-8") as file:
            yaml.dump(DEFAULT_CONFIG, file, default_flow_style=False)
        print(f"New config file initialized: {config_file}")

    with open(config_file, encoding="utf-8") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value

    # Add this block after loading the config
    supplier = config.get("supplier", "anthropic")
    api_key_name = f"{supplier}_api_key"
    config["api_key"] = config.get(api_key_name, "")

    return config


def create_save_folder():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)


def get_session_filename(config: Dict[str, Any]) -> str:
    from datetime import datetime

    now = datetime.now()
    extension: str = config.get("storage_format", "md")
    date_str = now.strftime("%d-%m-%Y")

    existing_files = [f for f in os.listdir(SAVE_FOLDER) if f.startswith(date_str)]

    if existing_files:
        max_index = max([int(f.split("_")[1].split(".")[0]) for f in existing_files])
        session_index = max_index + 1
    else:
        session_index = 1

    return f"{date_str}_{session_index}.{extension}"


def get_last_save_file() -> str | None:
    files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith((".json", ".md"))]
    if files:
        return max(files, key=lambda x: os.path.getctime(os.path.join(SAVE_FOLDER, x)))
    return None
