from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel


class SystemPromptConfig(BaseModel):
    max_steps: int


class TerminalPromptConfig(BaseModel):
    enabled: bool


class DBPromptConfig(BaseModel):
    enabled: bool


class TextStoragePromptConfig(BaseModel):
    enabled: bool


class PromptsConfig(BaseModel):
    system: SystemPromptConfig
    terminal: TerminalPromptConfig
    db: DBPromptConfig
    text_storage: TextStoragePromptConfig


class AppConfig(BaseModel):
    prompts: PromptsConfig

    @classmethod
    def load_config(cls, config_path: str = "app/configs/app_config.yaml") -> "AppConfig":
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)

        return cls(**config_data)

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


_app_config_instance: Optional[AppConfig] = None

def get_app_config(config_path: str = "app/config/app_config.yaml") -> AppConfig:
    global _app_config_instance
    if _app_config_instance is None:
        _app_config_instance = AppConfig.load_config(config_path)
    return _app_config_instance