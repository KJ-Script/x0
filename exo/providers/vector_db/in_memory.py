"""
In-Memory Vector Database Implementation

A simple in-memory vector database implementation for testing and development.
"""

import numpy as np
import uuid
from typing import List, Dict, Any, Optional
from .base import VectorDBAdapter

class InMemoryVectorDB(VectorDBAdapter):
    """
    Simple in-memory vector database implementation.
    
    This implementation stores vectors and metadata in memory using numpy arrays
    for efficient similarity calculations. It's useful for testing and development,
    but not suitable for production use with large datasets.
    """

    def __init__(self):
        """Initialize the in-memory vector database."""
        self.vectors = []
        self.metadatas = []
        self.ids = []

    def add(self, embeddings: List[List[float]], metadatas: Optional[List[Dict[str, Any]]] = None):
        """
        Add embeddings and metadata to the database.
        
        Args:
            embeddings (List[List[float]]): List of embedding vectors to add
            metadatas (Optional[List[Dict[str, Any]]]): Optional list of metadata dictionaries
        """
        if metadatas is None:
            metadatas = [{} for _ in embeddings]
            
        if len(embeddings) != len(metadatas):
            raise ValueError("Number of embeddings must match number of metadatas")
            
        for emb, meta in zip(embeddings, metadatas):
            self.vectors.append(np.array(emb))
            self.metadatas.append(meta)
            self.ids.append(str(uuid.uuid4()))

    def query(self, embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query the database for similar vectors.
        
        Args:
            embedding (List[float]): Query vector
            top_k (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of metadata for top matches
        """
        if not self.vectors:
            return []
            
        # Convert query to numpy array
        query_vec = np.array(embedding)
        
        # Calculate cosine similarities
        similarities = []
        for vec in self.vectors:
            # Cosine similarity = dot product / (norm1 * norm2)
            dot_product = np.dot(query_vec, vec)
            norm1 = np.linalg.norm(query_vec)
            norm2 = np.linalg.norm(vec)
            similarity = dot_product / (norm1 * norm2) if norm1 * norm2 > 0 else 0
            similarities.append(similarity)
            
        # Get indices of top k matches
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Return metadata for top matches
        return [self.metadatas[i] for i in top_indices]

    def delete(self, ids: List[str]):
        """
        Delete entries by their IDs.
        
        Args:
            ids (List[str]): List of IDs to delete
        """
        # Create a list of indices to keep
        keep_indices = [i for i, id_ in enumerate(self.ids) if id_ not in ids]
        
        # Update all lists to keep only the specified entries
        self.vectors = [self.vectors[i] for i in keep_indices]
        self.metadatas = [self.metadatas[i] for i in keep_indices]
        self.ids = [self.ids[i] for i in keep_indices]

    def clear(self):
        """Clear all entries from the database."""
        self.vectors = []
        self.metadatas = []
        self.ids = [] 