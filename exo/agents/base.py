"""
Agent Blueprint for Exo

This module provides a base Agent class that can be extended to create custom agents
using Exo's providers and tools. Agents can:
- Use a language model provider for reasoning and generation
- Use a set of tools for web automation, search, scraping, etc.
- Maintain state, memory, or context as needed
"""

from typing import List, Dict, Any, Optional, Callable

class Agent:
    def __init__(self, provider, tools: Optional[List[Any]] = None, name: Optional[str] = None):
        """
        Initialize the agent.
        Args:
            provider: The language model provider (must implement BaseProvider interface)
            tools (list): List of Tool instances the agent can use
            name (str, optional): Name of the agent
        """
        self.provider = provider
        self.tools = tools or []
        self.name = name or self.__class__.__name__
        self.memory = []  # Simple in-memory history (can be replaced with more advanced memory)

    def add_tool(self, tool):
        """Add a tool to the agent's toolbox."""
        self.tools.append(tool)

    def remember(self, item: Any):
        """Add an item to the agent's memory."""
        self.memory.append(item)

    def clear_memory(self):
        """Clear the agent's memory."""
        self.memory = []

    async def act(self, prompt: str, **kwargs) -> str:
        """
        Main entry point for the agent to process a prompt.
        By default, uses the provider to generate a response.
        Can be extended to use tools, memory, or more complex logic.
        Args:
            prompt (str): The user prompt or task
            **kwargs: Additional arguments for the provider
        Returns:
            str: The agent's response
        """
        self.remember({'role': 'user', 'content': prompt})
        response = await self.provider.chat(prompt, **kwargs)
        self.remember({'role': 'agent', 'content': response})
        return response

    def list_tools(self) -> List[str]:
        """List the names of available tools."""
        return [tool.name for tool in self.tools]

    def __repr__(self):
        return f"<Agent name={self.name} provider={self.provider.__class__.__name__} tools={self.list_tools()}>"
