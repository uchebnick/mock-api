from .prompt_composer import PromptComposer
from app.config.app_config import config



class SessionPrompt:
    def __init__(self, request: str):

        self.request = request

        component_paths = ["app/prompts/sys_prompt.md"]
        if config.use_terminal():
            component_paths.append("app/prompts/terminal_prompt.md")
        if config.use_db():
            component_paths.append("app/prompts/db_prompt.md")
        if config.use_text_storage():
            component_paths.append("app/prompts/text_storage_prompt.md")
        component_paths.append("app/prompts/session_prompt.md")


        context = {
            "request": request
        }

        self.composer = PromptComposer(component_paths, context)

    def get_prompt(self) -> str:
        return self.composer.build_prompt()

