from fastapi import Depends
from app.config.app_config import get_app_config, AppConfig
from app.config.ai_config import get_ai_config, AIConfig
from .prompt_composer import PromptComposer



class RequestPrompt:
    def __init__(self, ai_docs: str, openapi_docs: str, str_request: str):
        self.app_config = get_app_config()
        self.ai_config = get_ai_config()
        self.str_request = str_request
        self.ai_docs = ai_docs
        self.openapi_docs = openapi_docs

        component_paths = ["app/prompts/sys_prompt.md"]
        if self.app_config.use_terminal:
            component_paths.append("app/prompts/terminal_prompt.md")
        if self.app_config.use_db:
            component_paths.append("app/prompts/db_prompt.md")
        if self.app_config.use_text_storage:
            component_paths.append("app/prompts/text_storage_prompt.md")
        component_paths.append("app/prompts/request_handler_prompt.md")


        context = {
            "request": self.str_request,
            "ai_docs": self.ai_docs,
            "openapi_docs": self.openapi_docs
        }

        self.composer = PromptComposer(component_paths, context)

    def get_prompt(self) -> str:
        return self.composer.build_prompt()