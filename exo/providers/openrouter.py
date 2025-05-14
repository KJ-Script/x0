"""
OpenRouter Provider Implementation

This module implements the OpenRouter provider, which allows access to multiple
language models through a single API key. OpenRouter provides access to various
models from different providers like OpenAI, Anthropic, Google, and more.
"""

import aiohttp
from typing import Optional, List, Dict, Any
from .base import BaseProvider

class OpenRouterProvider(BaseProvider):
    """
    OpenRouter provider implementation that allows access to multiple models
    through a single API key.
    """

    BASE_URL = "https://openrouter.ai/api/v1"
    
    def __init__(
        self,
        api_key: str,
        model: str = "openai/gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """
        Initialize the OpenRouter provider.
        
        Args:
            api_key (str): Your OpenRouter API key
            model (str): The model to use (e.g., 'openai/gpt-3.5-turbo', 'anthropic/claude-2')
            temperature (float): Controls randomness in the output
            max_tokens (Optional[int]): Maximum number of tokens to generate
            **kwargs: Additional model-specific parameters
        """
        super().__init__(**kwargs)
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/yourusername/x0",  # Replace with your actual URL
            "X-Title": "X0 Library"  # Replace with your application name
        }

    async def _generate_chat_response(self, message: str, **kwargs) -> str:
        """
        Generate a chat response using the OpenRouter API.
        
        Args:
            message (str): The user's message
            **kwargs: Additional model-specific parameters
            
        Returns:
            str: The generated chat response
        """
        messages = self._chat_history.get_history()
        messages.append({"role": "user", "content": message})
        
        if self.system_prompt:
            messages.insert(0, {"role": "system", "content": self.system_prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
        }
        
        if self.max_tokens:
            payload["max_tokens"] = self.max_tokens
            
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.BASE_URL}/chat/completions",
                headers=self._headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"OpenRouter API error: {error_text}")
                
                result = await response.json()
                return result["choices"][0]["message"]["content"]

    async def generate(self, prompts: str | List[str], **kwargs) -> str | List[str]:
        """
        Generate text from the language model.
        
        Args:
            prompts (str or List[str]): The input prompt(s)
            **kwargs: Additional model-specific parameters
            
        Returns:
            str or List[str]: The generated text response(s)
        """
        if isinstance(prompts, str):
            return await self._generate_chat_response(prompts, **kwargs)
        
        return [await self._generate_chat_response(prompt, **kwargs) for prompt in prompts]

    @staticmethod
    def list_models() -> List[str]:
        """
        List all available models on OpenRouter.
        
        Returns:
            List[str]: List of available model identifiers
        """
        return [
            "openai/gpt-3.5-turbo",
            "openai/gpt-4",
            "anthropic/claude-2",
            "google/gemini-pro",
            "meta-llama/llama-2-70b-chat",
            "mistral/mistral-7b-instruct",
            "meta-llama/codellama-34b-instruct",
            "google/palm-2-chat-bison",
            "anthropic/claude-instant-1",
            "openai/gpt-4-32k",
            "openai/gpt-4-turbo-preview"
        ]

    @staticmethod
    def get_model_info() -> Dict[str, Any]:
        """
        Get information about the available models.
        
        Returns:
            Dict[str, Any]: Model information including capabilities and pricing
        """
        return {
            "provider": "OpenRouter",
            "description": "Access multiple AI models through a single API",
            "models": {
                "openai/gpt-3.5-turbo": {
                    "max_tokens": 4096,
                    "supports_chat": True,
                    "supports_completion": True
                },
                "openai/gpt-4": {
                    "max_tokens": 8192,
                    "supports_chat": True,
                    "supports_completion": True
                },
                "anthropic/claude-2": {
                    "max_tokens": 100000,
                    "supports_chat": True,
                    "supports_completion": True
                }
                # Add more model information as needed
            }
        } 