from fastapi import Request
from .utils import utills
from .prompts import SessionPrompt
import logging

logger = logging.getLogger("ai_manager.session")

class Session:
    def __init__(self, request: Request):
        self.context = []

        str_request = utills.convert_request_to_text(request)

        self.init_session_prompt = SessionPrompt(str_request).get_prompt()

    def start(self):
        
        

    def _get_str_context(self) -> str:
        result = ""
        

        for message in self.context:
            result += 

