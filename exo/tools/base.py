"""
Blue Print class for all tools.
"""
from typing import Callable, Dict, Optional, Any
from functools import wraps
class Tool:
    """
    Base class for all tools.
    """
    def __init__(
            self, 
            name: str, 
            description: 
            str, function: 
            Callable, parameters: 
            Optional[Dict[str, Any]] = None
        ):
        
        self.name = name or function.__name__
        self.description = description or function.__doc__ or f"Tool {self.name}"
        self.function = function
        self.parameters = parameters

        wraps(function)(this)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Call the tool with the given arguments.
        """
        return self.function(*args, **kwargs)
    
    def __str__(self) -> str:
        """
        Return the string representation of the tool.
        """
        return f"{self.name}: {self.description} {self.parameters}"
    
    def __repr__(self) -> str:
        """
        Return the string representation of the tool.
        """
        return self.__str__()
    
    
