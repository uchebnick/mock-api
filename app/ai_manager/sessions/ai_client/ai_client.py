import logging
from abc import ABC, abstractmethod
from fastapi import Depends
from app.config.ai_config import get_ai_config, AIConfig
from openai import OpenAI

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
        self.client = OpenAI(
            api_key=self.config.token,
            base_url=(
                self.config.base_url
                if self.config.base_url
                else "https://api.openai.com/v1"
            ),
        )

    def send_message(self, message: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.config.model, messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в OpenAI: {str(e)}")
            raise


class OllamaClient(AIBaseClient):
    def __init__(self, config: AIConfig = None):
        super().__init__(config)
        import ollama

        self.client = ollama
        if self.config.base_url:
            self.client.set_host(self.config.base_url)
        else:
            self.client.set_host("http://localhost:11434")

    def send_message(self, message: str) -> str:
        try:
            response = self.client.chat(
                model=self.config.model, messages=[{"role": "user", "content": message}]
            )
            return response["message"]["content"]
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в Ollama: {str(e)}")
            raise


class GeminiClient(AIBaseClient):
    def __init__(self, config: AIConfig = None):
        super().__init__(config)
        import google.generativeai as genai

        genai.configure(api_key=self.config.token)
        if self.config.base_url:
            genai.configure(transport="rest", api_endpoint=self.config.base_url)
        else:
            genai.configure(
                transport="rest",
                api_endpoint="https://generativelanguage.googleapis.com",
            )
        self.client = genai.GenerativeModel(self.config.model)

    def send_message(self, message: str) -> str:
        try:
            response = self.client.generate_content(message)
            return response.text
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в Gemini: {str(e)}")
            raise


class ClaudeClient(AIBaseClient):
    def __init__(self, config: AIConfig = None):
        super().__init__(config)
        import anthropic

        self.client = anthropic.Anthropic(
            api_key=self.config.token,
            base_url=(
                self.config.base_url
                if self.config.base_url
                else "https://api.anthropic.com"
            ),
        )

    def send_message(self, message: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": message}],
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в Claude: {str(e)}")
            raise


CLIENTS = {
    "chatgpt": ChatGPTClient,
    "ollama": OllamaClient,
    "gemini": GeminiClient,
    "claude": ClaudeClient,
}


def get_ai_client():
    config = get_ai_config()
    client_class = CLIENTS.get(config.ai_type)
    if not client_class:
        raise ValueError(f"Unsupported AI type: {config.ai_type}")
    return client_class(config)


def ai_send_message(message: str, client: AIBaseClient) -> str:
    return client.send_message(message)
