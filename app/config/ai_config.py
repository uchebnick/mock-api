from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import Field
from typing import Optional


class AIConfig(BaseSettings):
    AI_TYPE: str = Field(default="")
    AI_MODEL: str = Field(default="")
    AI_TOKEN: str = Field(default="")
    AI_BASE_URL: Optional[str] = Field(default=None)

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def ai_type(self):
        return self.AI_TYPE

    @property
    def model(self):
        return self.AI_MODEL

    @property
    def token(self):
        return self.AI_TOKEN

    @property
    def base_url(self):
        return self.AI_BASE_URL


@lru_cache()
def get_ai_config() -> AIConfig:
    return AIConfig()
