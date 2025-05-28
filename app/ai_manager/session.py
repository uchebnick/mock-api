from fastapi import Request
from .utils import utils
from .prompts import SessionPrompt
from fastapi import Depends
from ai_client import AIBaseClient, get_ai_client
from ..config.app_config import AppConfig, get_app_config
import logging
import re

logger = logging.getLogger("ai_manager.session")

class Session:
    def __init__(self, request: Request, llm_client: AIBaseClient = Depends(get_ai_client), app_config: AppConfig = Depends(get_app_config)):
        self.context = []
        self.llm_client = llm_client
        self.app_config = app_config

        str_request = utils.convert_request_to_text(request)
        self.init_session_prompt = SessionPrompt(str_request).get_prompt()

    def start(self) -> None:
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
        c = 1
        while not response and c <= max_steps:
            c += 1
            ai_msg = self._next_gen()
            response = self._get_response(ai_msg)

        return response

    def _handle_commands_from_message(self, msg: str):
        commands = self.app_config.enabled_commands()
        results = []
        
        # /interface.func %|param|% or /interface.func
        pattern = r'/(\w+)\.(\w+)(?:\s+%\|\s*([\s\S]*?)\s*\|%)?'
        matches = re.finditer(pattern, msg)
        
        for match in matches:
            interface_name = match.group(1)
            func_name = match.group(2)
            param = match.group(3)
            
            if interface_name in commands:
                interface_class = commands[interface_name]
                interface = interface_class()
                interface_commands = interface.get_commands()
                
                if func_name in interface_commands:
                    try:
                        if param is not None:
                            result = interface_commands[func_name](param)
                        else:
                            result = interface_commands[func_name]()
                        results.append(f"Command {interface_name}.{func_name} executed with result: {result}")
                    except Exception as e:
                        results.append(f"Error executing {interface_name}.{func_name}: {str(e)}")
                else:
                    results.append(f"Function {func_name} not found in interface {interface_name}")
            else:
                results.append(f"Interface {interface_name} not found")
                
        return results

    def _get_str_context(self) -> str:
        return "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in self.context])
    

    def _get_response(self, msg: str) -> str | None:
        match = re.search(r'/response %\|(.*?)\|%', msg, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return None


    def _next_gen(self):
        ai_message = self.context[-1]["content"]
        command_results = self._handle_commands_from_message(ai_message)
        
        system_message = "\n".join(command_results)
        self.context.append({
            "role": "user",
            "content": system_message
        })
        prompt = self._get_str_context()
            
        ans = self.llm_client.send_message(prompt)
        self.context.append({
            "role": "assistant",
            "content": ans
        })
        return ans





