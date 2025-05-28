from fastapi import Depends
from app.config.app_config import get_app_config, Config
from app.config.ai_config import get_ai_config, AIConfig
from ..utils import utils
from .prompt_composer import PromptComposer



class SessionPrompt:
    def __init__(self, str_request: str, app_config: Config = Depends(get_app_config), ai_config: AIConfig = Depends(get_ai_config)):
        self.app_config = app_config
        self.ai_config = ai_config

        self.str_request = str_request

        component_paths = ["app/prompts/sys_prompt.md"]
        if self.app_config.use_terminal():
            component_paths.append("app/prompts/terminal_prompt.md")
        if self.app_config.use_db():
            component_paths.append("app/prompts/db_prompt.md")
        if self.app_config.use_text_storage():
            component_paths.append("app/prompts/text_storage_prompt.md")
        component_paths.append("app/prompts/session_prompt.md")


        context = {
            "request": self.str_request
        }

        self.composer = PromptComposer(component_paths, context)

    def get_prompt(self) -> str:
        return self.composer.build_prompt()

