# app/config/ai_config.py

from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel

class AIConfig(BaseModel):
    ai_type: str
    token: Optional[str] = None
    model: str

    @classmethod
    def load_config(cls, config_path: str = "configs/ai_config.yaml") -> "AIConfig":
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"AI config file not found: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)

_ai_config_instance: Optional[AIConfig] = None

def get_ai_config(config_path: str = "app/config/ai_config.yaml") -> AIConfig:
    global _ai_config_instance
    if _ai_config_instance is None:
        _ai_config_instance = AIConfig.load_config(config_path)
    return _ai_config_instance