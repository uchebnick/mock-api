from typing import Optional
from pydantic import BaseModel
from .base_settings import BaseAppSettings
from functools import lru_cache


class SystemPromptConfig(BaseModel):
    max_steps: int = 10

    class Config:
        extra = "allow"


class TerminalPromptConfig(BaseModel):
    enabled: bool = False

    class Config:
        extra = "allow"


class DBPromptConfig(BaseModel):
    enabled: bool = False

    class Config:
        extra = "allow"


class TextStoragePromptConfig(BaseModel):
    enabled: bool = False

    class Config:
        extra = "allow"


class PromptsConfig(BaseModel):
    system: SystemPromptConfig = SystemPromptConfig()
    terminal: TerminalPromptConfig = TerminalPromptConfig()
    db: DBPromptConfig = DBPromptConfig()
    text_storage: TextStoragePromptConfig = TextStoragePromptConfig()

    class Config:
        extra = "allow"


class AppConfig(BaseAppSettings):
    prompts: PromptsConfig = PromptsConfig()
    
    class Config:
        env_prefix = "APP_"
        extra = "allow"

    @property
    def max_steps(self) -> int:
        return self.prompts.system.max_steps

    @property
    def use_system_prompt(self) -> bool:
        return self.prompts.system.enabled

    @property
    def use_terminal(self) -> bool:
        return self.prompts.terminal.enabled

    @property
    def use_db(self) -> bool:
        return self.prompts.db.enabled

    @property
    def use_text_storage(self) -> bool:
        return self.prompts.text_storage.enabled
    
    @property
    def enabled_commands(self):
        from app.ai_manager.tool_interfaces import DBInterface, TerminalInterface, TextStorageInterface
        commands = {}
        if self.use_db:
            commands["/db"] = DBInterface
        if self.use_terminal:
            commands["/terminal"] = TerminalInterface
        if self.use_text_storage:
            commands["/text_storage"] = TextStorageInterface
        return commands


@lru_cache()
def get_app_config() -> AppConfig:
    return AppConfig()