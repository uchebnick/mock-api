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


class Config(BaseModel):
    prompts: PromptsConfig

    @classmethod
    def load_config(cls, config_path: str = "app/config/config.yaml") -> "Config":
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


class AIConfig:
    def __init__(self, ai_type: str, token: str = "", base_url: str = "", model: str = ""):
        self.ai_type = ai_type  # 'ollama', 'chatgpt', 'gemini', 'claude'
        self.token = token
        self.base_url = base_url
        self.model = model

# Пример конфигурации (замените на свои значения)
config = AIConfig(
    ai_type='chatgpt',
    token='sk-...ваш_токен...',
    base_url='https://api.openai.com/v1',
    model='gpt-3.5-turbo'
)