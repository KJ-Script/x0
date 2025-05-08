"""
Base Vector Database Adapter Interface

This module defines the abstract base class that all vector database adapters must implement.
It establishes a standard interface for interacting with different vector databases,
ensuring consistency across different implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class VectorDBAdapter(ABC):
    """
    Abstract interface for a vector database adapter.
    
    This class defines the interface that all vector database implementations must follow.
    By inheriting from ABC (Abstract Base Class), it ensures that any class that
    inherits from VectorDBAdapter must implement all abstract methods.
    """

    @abstractmethod
    def add(self, embeddings: List[List[float]], metadatas: Optional[List[Dict[str, Any]]] = None):
        """
        Add embeddings (and optional metadata) to the vector DB.
        
        Args:
            embeddings (List[List[float]]): List of embedding vectors to add
            metadatas (Optional[List[Dict[str, Any]]]): Optional list of metadata dictionaries
                corresponding to each embedding
        """
        pass

    @abstractmethod
    def query(self, embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query the vector DB for the top_k most similar embeddings.
        
        Args:
            embedding (List[float]): The query embedding vector
            top_k (int): Number of most similar results to return
            
        Returns:
            List[Dict[str, Any]]: List of metadata dictionaries for the closest matches
        """
        pass

    @abstractmethod
    def delete(self, ids: List[str]):
        """
        Delete entries by their IDs.
        
        Args:
            ids (List[str]): List of IDs to delete
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Remove all entries from the vector DB.
        """
        pass 