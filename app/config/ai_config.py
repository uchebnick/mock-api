from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel

class AIConfig(BaseModel):
    ai_type: str
    token: Optional[str] = None
    base_url: str
    model: str

    @classmethod
    def load_config(cls, config_path: str = "app/config/ai_config.yaml") -> "AIConfig":
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"AI config file not found: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)
