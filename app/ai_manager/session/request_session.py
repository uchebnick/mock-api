from fastapi import Request
from ..prompts import RequestPrompt
from fastapi import Depends
from .ai_client.ai_client import AIBaseClient, get_ai_client
from ...config.app_config import AppConfig, get_app_config
from .base_session import BaseSession
import logging
import re
import json

class RequestSession(BaseSession):
    def __init__(self, ai_docs: str, openapi_docs: str, request: str):
        init_session_prompt = RequestPrompt(ai_docs, openapi_docs, request).get_prompt()
        llm_client = get_ai_client()
        app_config = get_app_config()
        super().__init__(init_session_prompt, llm_client, app_config)

    def _get_response(self, msg: str) -> str | None:
        match = re.search(r'/response %\|(.*?)\|%', msg, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def _parse_json_response(self, response_str: str) -> dict | None:
        try:
            return json.loads(response_str)
        except json.JSONDecodeError as e:
            error_message = f"Ошибка при разборе JSON: {str(e)}"
            logging.error(error_message)
            return None

    def start(self) -> dict | None:
        message = self.init_session_prompt
        ans = self.llm_client.send_message(message)
        self.context.append({
            "role": "system",
            "content": message
        })
        self.context.append({
            "role": "assistant",
            "content": ans
        })

        response = self._get_response(ans)
        max_steps = self.app_config.max_steps()
        current_step = 1

        while current_step <= max_steps:
            if not response:
                current_step += 1
                ai_msg = self._next_gen()
                response = self._get_response(ai_msg)
                continue

            json_response = self._parse_json_response(response)
            if json_response is not None:
                return json_response

            error_message = f"Не удалось преобразовать ответ в JSON. Попытка {current_step} из {max_steps}"
            logging.warning(error_message)
            
            message = f"json loads error: {error_message}"
            ans = self.llm_client.send_message(message)
            self.context.append({
                "role": "system",
                "content": message
            })
            self.context.append({
                "role": "assistant",
                "content": ans
            })
            
            response = self._get_response(ans)
            current_step += 1

        logging.error(f"Достигнуто максимальное количество попыток ({max_steps}). Не удалось получить корректный JSON-ответ.")
        return None