import requests
from abc import ABC, abstractmethod
from app.config.ai_config import AIConfig

class AIBaseClient(ABC):
    def __init__(self, config: AIConfig):
        self.config = config

    @abstractmethod
    def send_message(self, message: str) -> str:
        pass

class ChatGPTClient(AIBaseClient):
    def send_message(self, message: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.config.token}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.model or "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": message}]
        }
        response = requests.post(f"{self.config.base_url}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

class OllamaClient(AIBaseClient):
    def send_message(self, message: str) -> str:
        data = {"model": self.config.model or "llama2", "prompt": message}
        response = requests.post(f"{self.config.base_url}/api/generate", json=data)
        response.raise_for_status()
        return response.json()["response"]

class GeminiClient(AIBaseClient):
    def send_message(self, message: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.config.token}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.model or "gemini-pro",
            "messages": [{"role": "user", "content": message}]
        }
        response = requests.post(f"{self.config.base_url}/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

class ClaudeClient(AIBaseClient):
    def send_message(self, message: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.config.token}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.model or "claude-3-opus-20240229",
            "messages": [{"role": "user", "content": message}]
        }
        response = requests.post(f"{self.config.base_url}/v1/messages", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

CLIENTS = {
    "chatgpt": ChatGPTClient,
    "ollama": OllamaClient,
    "gemini": GeminiClient,
    "claude": ClaudeClient,
}

def get_ai_client(config: AIConfig) -> AIBaseClient:
    client_class = CLIENTS.get(config.ai_type)
    if not client_class:
        raise ValueError(f"Unknown AI type: {config.ai_type}")
    return client_class(config)

def ai_send_message(message: str, config: AIConfig) -> str:
    client = get_ai_client(config)
    return client.send_message(message)

# # Пример использования
# if __name__ == "__main__":
#     client = LLMClient()
#     response = client.generate("Как создать нейросеть?")
#     print(response)