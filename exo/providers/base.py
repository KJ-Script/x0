"""
Base Provider Interface for Exo Library

This module defines the abstract base class that all model providers must implement.
It establishes a standard interface for interacting with different language models,
ensuring consistency across different providers (OpenAI, Anthropic, Gemini, etc.).

The BaseProvider class defines the required methods that each provider implementation
must include to be compatible with the Exo library.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from exo.providers.context.chat_history import ChatHistory
from .vector_db import VectorDBAdapter, InMemoryVectorDB

class BaseProvider(ABC):
    """
    Abstract base class for all model providers.
    
    This class defines the interface that all provider implementations must follow.
    By inheriting from ABC (Abstract Base Class), it ensures that any class that
    inherits from BaseProvider must implement all abstract methods.
    
    The BaseProvider interface standardizes how the Exo library interacts with
    different language models, making it easy to swap between providers while
    maintaining consistent behavior.
    """

    # Shared chat history instance for all providers
    _shared_history = ChatHistory()

    def __init__(self, **kwargs):
        """
        Initialize the base provider.
        """
        # Use the shared history instead of creating a new one
        self._chat_history = self._shared_history
        self._system_prompt: Optional[str] = None
        self._vector_db: VectorDBAdapter = InMemoryVectorDB()

    @property
    def system_prompt(self) -> Optional[str]:
        """Get the current system prompt."""
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, prompt: Optional[str]):
        """Set the system prompt."""
        self._system_prompt = prompt

    @property
    def vector_db(self) -> VectorDBAdapter:
        """Get the vector database adapter."""
        return self._vector_db

    @vector_db.setter
    def vector_db(self, adapter: VectorDBAdapter):
        """Set the vector database adapter."""
        self._vector_db = adapter

    @abstractmethod
    async def generate(self, prompts, **kwargs):
        """
        Generate text from the language model.
        
        This abstract method must be implemented by all provider classes to generate
        text responses from their respective language models.
        
        Args:
            prompts (str or List[str]): The input prompt(s) to send to the model.
                Can be a single string or a list of strings for batch processing.
            **kwargs: Additional model-specific parameters such as:
                - temperature (float): Controls randomness in the output
                - max_tokens (int): Maximum number of tokens to generate
                - top_p (float): Controls diversity via nucleus sampling
                - stop (List[str]): Custom stop sequences
                - etc.
        
        Returns:
            str or List[str]: The generated text response(s) from the model.
                Return type should match the input type (single string for single prompt,
                list of strings for multiple prompts).
        
        Raises:
            NotImplementedError: If the provider class doesn't implement this method.
            Various provider-specific exceptions for API errors, rate limits, etc.
        """
        pass

    async def chat(self, message: str, **kwargs) -> str:
        """
        Generate a chat response using the shared chat history.
        
        Args:
            message (str): The user's message
            **kwargs: Additional model-specific parameters
            
        Returns:
            str: The generated chat response
        """
        # Add user message to history
        self._chat_history.add_message('user', message)
        
        # Get response from concrete implementation
        response = await self._generate_chat_response(message, **kwargs)
        
        # Add assistant response to history
        self._chat_history.add_message('assistant', response)
        
        return response

    @abstractmethod
    async def _generate_chat_response(self, message: str, **kwargs) -> str:
        """
        Concrete implementation of chat response generation.
        To be implemented by each provider.
        """
        pass

    def clear_chat_history(self):
        """Clear the chat history."""
        self._chat_history.clear_history()
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the chat history."""
        return self._chat_history.get_history()

    def get_model_info():
        pass
    
    def list_models():
        pass

    def list_providers():
        """
        Returns all Model providers. 
        
        """
        return [
            'Anthropic-Claude',
            'Google-Gemni',
            'Ollama',
            'Openai-GPT'
        ]
