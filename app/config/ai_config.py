# app/config/ai_config.py

from .base_settings import BaseAppSettings
from functools import lru_cache


class AIConfig(BaseAppSettings):
    ai_type: str = "ollama"
    model: str = "deepseek-r1:1.5b"
    token: str = ""
    
    class Config:
        env_prefix = "AI_"
        extra = "allow"


@lru_cache()
def get_ai_config() -> AIConfig:
    return AIConfig()