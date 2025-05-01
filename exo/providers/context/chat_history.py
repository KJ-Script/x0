from typing import List, Dict, Optional
from datetime import datetime


class ChatHistory:
    """
    A class for managing and storing chat history.
    """
    
    def __init__(self):
        """Initialize the chat history."""
        self.messages: List[Dict[str, str]] = []
        self._system_prompt: Optional[str] = None


    @property
    def system_prompt(self) -> Optional[str]:
        """Get the current system prompt."""
        return self._system_prompt
    
    @system_prompt.setter
    def system_prompt(self, prompt: Optional[str]):
        """Set the system prompt."""
        self._system_prompt = prompt
        
    def add_message(self, role: str, content: str):
        """Add a message to the chat history."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def get_history(self) -> List[Dict[str, str]]:
        """Get the complete chat history."""
        return self.messages.copy()
    
    def clear_history(self):
        """Clear the chat history."""
        self.messages = []

    def get_history_as_string(self) -> str:
        """Get the chat history as a formatted string."""
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.messages])
