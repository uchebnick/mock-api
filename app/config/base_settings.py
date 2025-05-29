from pydantic_settings import BaseSettings
from functools import lru_cache


class BaseAppSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"


@lru_cache()
def get_settings():
    return BaseAppSettings() 