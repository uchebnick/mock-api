from .prompt_composer import PromptComposer
from app.config.app_config import config

class InitPrompt:
    def __init__(self, user_docs: str = "'hello world' server", max_steps: int = 5):

        self.user_docs = user_docs
        self.max_steps = max_steps

        component_paths = ["app/prompts/sys_prompt.md"]
        if config.use_terminal():
            component_paths.append("app/prompts/terminal_prompt.md")
        if config.use_db():
            component_paths.append("app/prompts/db_prompt.md")
        if config.use_text_storage():
            component_paths.append("app/prompts/text_storage_prompt.md")
        component_paths.append("app/prompts/init_prompt.md")

        context = {
            "user_docs": user_docs,
            "max_steps": max_steps
        }

        self.composer = PromptComposer(component_paths, context)

    def get_prompt(self) -> str:
        return self.composer.build_prompt()

