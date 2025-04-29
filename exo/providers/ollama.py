"""
OllamaProvider - A wrapper for Ollama's AI models.

This module provides a provider implementation for Ollama's AI models,
allowing seamless integration with the Exo library's provider interface.
"""

from . import BaseProvider
from exo.providers.base import BaseProvider
from langchain_ollama import OllamaLLM
from typing import List, Dict

class OllamaProvider(BaseProvider):
    """
    OllamaProvider - A wrapper for Ollama's AI models.
    """
    
    def __init__(self, model: str, stream: bool = False, **kwargs):
        """
        Initialize the Ollama provider.
        """
        super().__init__(**kwargs)
        self.model = model
        self.stream = stream

        self.client = OllamaLLM(model=self.model)
        
    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the Ollama model.
        """
        if self.stream:
            response = self.client.stream(prompt)
            for chunk in response:
                yield chunk
        else:
            response = self.client.invoke(prompt)
            return response
        

    async def chat(self, message: str, **kwargs) -> str:
        """
        Generate a chat response from the Ollama model.
        """
        return await self.generate(message, **kwargs)   
    
    def clear_chat_history(self):
        """Clear the chat history."""
        self.chat_history = []
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the chat history."""
        return self.chat_history.copy()
