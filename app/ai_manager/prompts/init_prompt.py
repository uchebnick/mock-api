from fastapi import Depends
from app.config.app_config import get_app_config
from app.config.ai_config import get_ai_config
from .prompt_composer import PromptComposer


class InitPrompt:
    def __init__(self, user_docs: str, max_steps: int = 5):
        self.app_config = get_app_config()
        self.ai_config = get_ai_config()
        self.user_docs = user_docs
        self.max_steps = max_steps

        component_paths = ["app/prompts/sys_prompt.md"]

        if self.app_config.use_terminal:
            component_paths.append("app/prompts/terminal_prompt.md")
        if self.app_config.use_db:
            component_paths.append("app/prompts/db_prompt.md")
        if self.app_config.use_text_storage:
            component_paths.append("app/prompts/text_storage_prompt.md")
        component_paths.append("app/prompts/init_prompt.md")

        context = {"user_docs": self.user_docs, "max_steps": self.max_steps}

        self.composer = PromptComposer(component_paths, context)

    def get_prompt(self) -> str:
        return self.composer.build_prompt()
