"""
GemniProvider - A wrapper for Google's Gemini AI models.

This module provides a provider implementation for Google's Gemini AI models,
allowing seamless integration with the Exo library's provider interface.
"""
from . import BaseProvider
from google import genai
from google.genai import types
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
        self.model = model
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.stream = stream
        self.chat_history = []

        if not self.api_key:
            raise ValueError("API key is required")

        self.client = genai.Client(api_key=self.api_key)

    async def generate(self, prompt, **kwargs):
        """
        Generate a response from the Gemini model.
        
        Args:
            prompt (str): The input prompt to send to the model
            **kwargs: Additional parameters for the generation request
            
        Returns:
            str: The generated text response from the model
        """
        if self.stream:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    max_output_tokens=self.max_output_tokens,
                    temperature=self.temperature,
                    topP=self.top_p,
                    topK=self.top_k,
                )
            )
            # Extract text from non-streaming response
            return response.text
        else:
            response = self.client.models.generate_content_stream(
                            model=self.model,
                            contents=[prompt],
                            config=types.GenerateContentConfig(
                                max_output_tokens=self.max_output_tokens,
                                temperature=self.temperature,
                                topP=self.top_p,
                                topK=self.top_k,
                            )
                        )
            # Extract text from streaming response
            full_text = ""
            for chunk in response:
                if chunk.text:
                    full_text += chunk.text
            return full_text
    
    async def chat(self, message: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Generate a chat response from the Gemini model with conversation history.
        
        Args:
            message (str): The user's message
            system_prompt (str, optional): A system prompt to set the context
            **kwargs: Additional parameters for the generation request
            
        Returns:
            str: The generated chat response from the model
        """
        # Add the user message to chat history
        self.chat_history.append({"role": "user", "content": message})
        
        # Prepare the chat content
        chat_content = []
        
        # Add system prompt if provided
        if system_prompt:
            chat_content.append(system_prompt)
        
        # Add chat history
        for msg in self.chat_history:
            chat_content.append(msg["content"])
        
        # Generate response
        if self.stream:
            response = self.client.models.generate_content(
                model=self.model,
                contents=chat_content,
                config=types.GenerateContentConfig(
                    max_output_tokens=self.max_output_tokens,
                    temperature=self.temperature,
                    topP=self.top_p,
                    topK=self.top_k,
                )
            )
            response_text = response.text
        else:
            response = self.client.models.generate_content_stream(
                model=self.model,
                contents=chat_content,
                config=types.GenerateContentConfig(
                    max_output_tokens=self.max_output_tokens,
                    temperature=self.temperature,
                    topP=self.top_p,
                    topK=self.top_k,
                )
            )
            response_text = ""
            for chunk in response:
                if chunk.text:
                    response_text += chunk.text
        
        # Add the assistant's response to chat history
        self.chat_history.append({"role": "assistant", "content": response_text})
        
        return response_text
    
    def clear_chat_history(self):
        """
        Clear the chat history.
        """
        self.chat_history = []
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """
        Get the chat history.
        
        Returns:
            List[Dict[str, str]]: The chat history
        """
        return self.chat_history
    

    
        
        