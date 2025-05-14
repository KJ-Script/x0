"""
Model Router Provider Implementation

This module implements a custom model router provider that allows routing requests
to different AI models based on configuration. It supports multiple providers
and models through a unified interface.
"""

import asyncio
from typing import Optional, List, Dict, Any, Union
from .base import BaseProvider
from .openai import OpenAIProvider
from .anthropic import AnthropicProvider
from .gemni import GemniProvider

class ModelRouterProvider(BaseProvider):
    """
    Model Router provider implementation that allows routing requests to different
    AI models based on configuration.
    """

    def __init__(
        self,
        config: Dict[str, Any],
        default_model: str = "openai/gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """
        Initialize the Model Router provider.
        
        Args:
            config (Dict[str, Any]): Configuration for different providers
                Example:
                {
                    "openai": {
                        "api_key": "your-openai-key",
                        "models": ["gpt-3.5-turbo", "gpt-4"]
                    },
                    "anthropic": {
                        "api_key": "your-anthropic-key",
                        "models": ["claude-2", "claude-instant-1"]
                    },
                    "gemini": {
                        "api_key": "your-gemini-key",
                        "models": ["gemini-pro"]
                    }
                }
            default_model (str): The default model to use
            temperature (float): Controls randomness in the output
            max_tokens (Optional[int]): Maximum number of tokens to generate
            **kwargs: Additional model-specific parameters
        """
        super().__init__(**kwargs)
        self.config = config
        self.default_model = default_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._providers: Dict[str, BaseProvider] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize the providers based on configuration."""
        if "openai" in self.config:
            self._providers["openai"] = OpenAIProvider(
                api_key=self.config["openai"]["api_key"]
            )
        
        if "anthropic" in self.config:
            self._providers["anthropic"] = AnthropicProvider(
                api_key=self.config["anthropic"]["api_key"]
            )
        
        if "gemini" in self.config:
            self._providers["gemini"] = GemniProvider(
                api_key=self.config["gemini"]["api_key"]
            )

    def _get_provider_and_model(self, model: str) -> tuple[BaseProvider, str]:
        """
        Get the provider and model name from a model identifier.
        
        Args:
            model (str): Model identifier (e.g., 'openai/gpt-3.5-turbo')
            
        Returns:
            tuple[BaseProvider, str]: Provider instance and model name
        """
        provider_name, model_name = model.split("/", 1)
        
        if provider_name not in self._providers:
            raise ValueError(f"Provider '{provider_name}' not configured")
        
        if model_name not in self.config[provider_name]["models"]:
            raise ValueError(f"Model '{model_name}' not available for provider '{provider_name}'")
        
        return self._providers[provider_name], model_name

    async def _generate_chat_response(self, message: str, **kwargs) -> str:
        """
        Generate a chat response using the specified model.
        
        Args:
            message (str): The user's message
            **kwargs: Additional model-specific parameters
            
        Returns:
            str: The generated chat response
        """
        model = kwargs.get("model", self.default_model)
        provider, model_name = self._get_provider_and_model(model)
        
        # Set the model for the provider
        if hasattr(provider, "model"):
            provider.model = model_name
        
        # Set temperature if provided
        if hasattr(provider, "temperature"):
            provider.temperature = kwargs.get("temperature", self.temperature)
        
        # Set max_tokens if provided
        if hasattr(provider, "max_tokens"):
            provider.max_tokens = kwargs.get("max_tokens", self.max_tokens)
        
        return await provider.chat(message, **kwargs)

    async def generate(self, prompts: Union[str, List[str]], **kwargs) -> Union[str, List[str]]:
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
        List all available models across all configured providers.
        
        Returns:
            List[str]: List of available model identifiers
        """
        return [
            "openai/gpt-3.5-turbo",
            "openai/gpt-4",
            "anthropic/claude-2",
            "anthropic/claude-instant-1",
            "google/gemini-pro"
        ]

    @staticmethod
    def get_model_info() -> Dict[str, Any]:
        """
        Get information about the available models.
        
        Returns:
            Dict[str, Any]: Model information including capabilities and pricing
        """
        return {
            "provider": "ModelRouter",
            "description": "Custom model router for multiple AI providers",
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
                },
                "google/gemini-pro": {
                    "max_tokens": 32768,
                    "supports_chat": True,
                    "supports_completion": True
                }
            }
        } 