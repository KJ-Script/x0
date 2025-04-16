"""
AnthropicProvider - A wrapper for Anthropic's AI models.

This module provides a provider implementation for Anthropic's AI models,
allowing seamless integration with the Exo library's provider interface.
"""

import anthropic
from . import BaseProvider
from exo.providers.base import BaseProvider

class AnthropicProvider(BaseProvider):
    """
    AnthropicProvider - A wrapper for Anthropic's AI models.
    """
    
    def __init__(self, model: str, api_key: str, **kwargs):
        """
        Initialize the Anthropic provider.
        """
        super().__init__(**kwargs)
        self.model = model
        self.api_key = api_key
        self.client = anthropic.Anthropic(api_key=self.api_key)

    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the Anthropic model.
        """
        response = self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content
