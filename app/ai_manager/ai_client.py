import logging
from abc import ABC, abstractmethod
from fastapi import Depends
from app.config.ai_config import get_ai_config, AIConfig

logger = logging.getLogger("ai_manager.ai_client")

class AIBaseClient(ABC):
    def __init__(self, config: AIConfig = None):
        if config is None:
            config = get_ai_config()
        self.config = config

    @abstractmethod
    def send_message(self, message: str) -> str:
        pass

class ChatGPTClient(AIBaseClient):
    def __init__(self, config: AIConfig = None):
        super().__init__(config)
        import openai
        openai.api_key = self.config.token
        self.client = openai

    def send_message(self, message: str) -> str:
        response = self.client.ChatCompletion.create(
            model=self.config.model,
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content

class OllamaClient(AIBaseClient):
    def __init__(self, config: AIConfig = None):
        super().__init__(config)
        import ollama
        self.client = ollama

    def send_message(self, message: str) -> str:
        response = self.client.chat(
            model=self.config.model,
            messages=[{"role": "user", "content": message}]
        )
        return response['message']['content']

class GeminiClient(AIBaseClient):
    def __init__(self, config: AIConfig = None):
        super().__init__(config)
        import google.generativeai as genai
        genai.configure(api_key=self.config.token)
        self.client = genai.GenerativeModel(self.config.model)

    def send_message(self, message: str) -> str:
        response = self.client.generate_content(message)
        return response.text

class ClaudeClient(AIBaseClient):
    def __init__(self, config: AIConfig = None):
        super().__init__(config)
        import anthropic
        self.client = anthropic.Anthropic(api_key=self.config.token)

    def send_message(self, message: str) -> str:
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": message}]
        )
        return response.content[0].text

CLIENTS = {
    "chatgpt": ChatGPTClient,
    "ollama": OllamaClient,
    "gemini": GeminiClient,
    "claude": ClaudeClient,
}

def get_ai_client(config: AIConfig = Depends(get_ai_config)) -> AIBaseClient:
    client_class = CLIENTS.get(config.ai_type)
    if not client_class:
        logger.critical(f"Unknown AI type: {config.ai_type}")
        raise ValueError(f"Unknown AI type: {config.ai_type}")
    return client_class(config)

def ai_send_message(message: str, client: AIBaseClient = Depends(get_ai_client)) -> str:
    return client.send_message(message)