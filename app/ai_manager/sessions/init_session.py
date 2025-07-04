from fastapi import Request
from ..prompts import InitPrompt
from fastapi import Depends
from .ai_client.ai_client import get_ai_client
from app.config.app_config import get_app_config
from .base_session import BaseSession
import re


class InitSession(BaseSession):
    def __init__(self, user_docs: str, max_steps: int = 3):
        init_session_prompt = InitPrompt(user_docs, max_steps=max_steps).get_prompt()
        llm_client = get_ai_client()
        app_config = get_app_config()
        super().__init__(init_session_prompt, llm_client, app_config)

    def _get_openapi(self, msg: str) -> str | None:
        match = re.search(r"command.openapi <(.*?)>", msg, re.DOTALL)

        if match:
            return match.group(1).strip()
        return None

    def _get_docs(self, msg: str) -> str | None:
        match = re.search(r"command.markdown <(.*?)>", msg, re.DOTALL)

        if match:
            return match.group(1).strip()
        return None

    def _write_openapi(self, openapi_docs: str):
        with open("app/docs/openapi_docs.yaml", "w", encoding="utf-8") as f:
            f.write(openapi_docs)

    def _write_docs(self, ai_docs: str):
        with open("app/docs/docs.md", "w", encoding="utf-8") as f:
            f.write(ai_docs)

    def start(self) -> tuple[str | None, str | None]:
        message = self.init_session_prompt
        ans = self.llm_client.send_message(message)
        self.context.append({"role": "system", "content": message})
        self.context.append({"role": "assistant", "content": ans})

        docs = self._get_docs(ans)
        openapi = self._get_openapi(ans)
        max_steps = self.app_config.max_steps
        c = 1
        while not (docs or openapi) and c <= max_steps:
            c += 1
            print(f"Step {c} of {max_steps}")

            if docs:
                message = "Markdown docs has been saved, it remains to save the openapi using command.openapi <OPENAPI_DOCS>"
            if openapi:
                message = "Openapi docs has been saved, it remains to save the markdown using command.markdown <MARKDOWN_DOCS>"

            # Безопасный вывод контекста
            for msg in self.context:
                content = msg.get("content", "")
                print(f"{msg.get('role', 'unknown')}: {content[:100]}...")

            ai_msg = self._next_gen(payload=message)

            if not docs:
                docs = self._get_docs(ai_msg)
            if not openapi:
                openapi = self._get_openapi(ai_msg)

        if docs:
            self._write_docs(docs)
        if openapi:
            self._write_openapi(openapi)

        return docs, openapi
