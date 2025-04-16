"""
OpenAIProvider - A wrapper for OpenAI's AI models.

This module provides a provider implementation for OpenAI's AI models,
allowing seamless integration with the Exo library's provider interface.
"""

from . import BaseProvider
from exo.providers.base import BaseProvider
from openai import OpenAI

class OpenAIProvider(BaseProvider):
    """
    OpenAIProvider - A wrapper for OpenAI's AI models.
    """
    
    def __init__(self, model: str, **kwargs):
        """
        Initialize the OpenAI provider.
        """
        super().__init__(**kwargs)
        self.model = model
        self.client = OpenAI()
        
    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the OpenAI model.
        """
        response = self.client.chat.responses.create(
            model=self.model,
            prompt=prompt,
        )
        return response.output.text
    