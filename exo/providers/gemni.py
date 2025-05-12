"""
GemniProvider - A wrapper for Google's Gemini AI models.

This module provides a provider implementation for Google's Gemini AI models,
allowing seamless integration with the Exo library's provider interface.
"""
from . import BaseProvider
import google.generativeai as genai
import os
from typing import List, Dict, Any, Optional, Union


class GemniProvider(BaseProvider):
    """
    Provider implementation for Google's Gemini AI models.
    
    This class wraps the Google Generative AI Python SDK to provide a consistent
    interface for interacting with Gemini models through the Exo library.
    
    Attributes:
        api_key (str): The API key for authenticating with Google's Gemini API
        model (str): The name of the Gemini model to use
        client (genai.Client): The Google Generative AI client instance
        chat_history (List[Dict[str, str]]): History of chat messages
    """

    def __init__(
            self, 
            api_key, 
            model,
            stream=False,
            max_output_tokens=500,
            temperature=0.5,
            top_p=0.95,
            top_k=40,
            **kwargs):
        """
        Initialize the Gemini provider.
        
        Args:
            api_key (str, optional): API key for Gemini. If not provided, will look for GEMNI_API_KEY env var
            model (str): The name of the Gemini model to use (e.g., 'gemini-pro')
            max_output_tokens (int, optional): The maximum number of tokens to generate
            temperature (float, optional): The temperature to use for the model
            top_p (float, optional): The top-p value to use for the model
            top_k (int, optional): The top-k value to use for the model
            **kwargs: Additional arguments passed to the BaseProvider
        """
        super().__init__(**kwargs)

        self.api_key = api_key or os.getenv("GEMNI_API_KEY")
        self.model_name = model
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.stream = stream
        self.chat_history = []

        if not self.api_key:
            raise ValueError("API key is required")

        # Configure the API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=self.model_name)

    async def generate(self, prompt, **kwargs):
        """
        Generate a response from the Gemini model.
        
        Args:
            prompt (str): The input prompt to send to the model
            **kwargs: Additional parameters for the generation request
            
        Returns:
            str: The generated text response from the model
        """
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=self.max_output_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                top_k=self.top_k,
            )
        )
        return response.text
    
    async def _generate_chat_response(self, message: str, **kwargs) -> str:
        """
        Generate a chat response using Gemini's chat format.
        """
        # Get the full conversation history
        history = self.get_chat_history()
        
        # Create a new chat session
        chat = self.model.start_chat(history=[])
        
        # Add conversation history
        for msg in history:
            if msg["role"] == "user":
                chat.send_message(msg["content"])
            elif msg["role"] == "assistant":
                # For assistant messages, we'll just continue as they're part of the history
                continue

        # Send the new message and get response
        response = chat.send_message(message)
        return response.text
    

    
        
        