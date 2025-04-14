"""
Base Provider Interface for Exo Library

This module defines the abstract base class that all model providers must implement.
It establishes a standard interface for interacting with different language models,
ensuring consistency across different providers (OpenAI, Anthropic, Gemini, etc.).

The BaseProvider class defines the required methods that each provider implementation
must include to be compatible with the Exo library.
"""

from abc import ABC, abstractmethod

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
