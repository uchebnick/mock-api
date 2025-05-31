from .base_settings import BaseAppSettings
from pydantic_settings import SettingsConfigDict
from functools import lru_cache
from pydantic import Field, BaseModel
import yaml
import os

class TerminalConfig(BaseModel):
    enabled: bool = False

class DatabaseConfig(BaseModel):
    enabled: bool = False

class TextStorageConfig(BaseModel):
    enabled: bool = False

class SystemConfig(BaseModel):
    max_steps: int = 2

class AppConfig(BaseAppSettings):
    terminal: TerminalConfig = Field(default_factory=TerminalConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    text_storage: TextStorageConfig = Field(default_factory=TextStorageConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)

    model_config = SettingsConfigDict(env_prefix="APP_")

    @property
    def use_terminal(self) -> bool:
        return self.terminal.enabled

    @property
    def use_db(self) -> bool:
        return self.database.enabled

    @property
    def use_text_storage(self) -> bool:
        return self.text_storage.enabled

    @property
    def use_system_prompt(self) -> bool:
        return self.system.enabled

    @property
    def max_steps(self) -> int:
        return self.system.max_steps

    @property
    def enabled_commands(self):
        from app.ai_manager.tool_interfaces import (
            DBInterface,
            TerminalInterface,
            TextStorageInterface,
        )

        commands = {}
        if self.use_db:
            commands["/db"] = DBInterface
        if self.use_terminal:
            commands["/terminal"] = TerminalInterface
        if self.use_text_storage:
            commands["/text_storage"] = TextStorageInterface
        return commands

def load_app_config() -> AppConfig:
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)

@lru_cache()
def get_app_config() -> AppConfig:
    return load_app_config()