from .sessions import InitSession, RequestSession
from ..config.app_config import get_app_config, AppConfig
from fastapi import Depends, Request
from .utils.utils import convert_request_to_text
from typing import Optional


class AIService:
    def __init__(self, user_docs: str, app_config: AppConfig):
        max_steps = app_config.max_steps
        docs, openapi = InitSession(user_docs, max_steps=max_steps).start()

        self.docs = docs
        self.openapi = openapi

    async def handle_request(self, request: Request):
        str_request = await convert_request_to_text(request)
        json_response = RequestSession(self.docs, self.openapi, str_request).start()
        return json_response


_ai_service_instance: Optional["AIService"] = None


async def get_ai_service(user_docs: str = None) -> AIService:
    global _ai_service_instance
    if _ai_service_instance is None or user_docs is not None:
        config = get_app_config()
        _ai_service_instance = AIService(user_docs=user_docs, app_config=config)
    return _ai_service_instance
