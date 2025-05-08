"""
ChromaDB Vector Database Implementation

This module provides a ChromaDB implementation of the VectorDBAdapter interface.
ChromaDB is a vector database that supports persistent storage and efficient similarity search.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from .base import VectorDBAdapter

class ChromaDBAdapter(VectorDBAdapter):
    """
    ChromaDB implementation of the VectorDBAdapter interface.
    
    This adapter provides persistent vector storage and efficient similarity search
    using ChromaDB as the backend.
    """

    def __init__(self, 
                 persist_directory: str = "./chroma_db",
                 collection_name: str = "default",
                 embedding_function = None):
        """
        Initialize the ChromaDB adapter.
        
        Args:
            persist_directory (str): Directory to persist the database
            collection_name (str): Name of the collection to use
            embedding_function: Optional embedding function to use
        """
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        
        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function
        )

    def add(self, embeddings: List[List[float]], metadatas: Optional[List[Dict[str, Any]]] = None):
        """
        Add embeddings and metadata to ChromaDB.
        
        Args:
            embeddings (List[List[float]]): List of embedding vectors to add
            metadatas (Optional[List[Dict[str, Any]]]): Optional list of metadata dictionaries
        """
        if metadatas is None:
            metadatas = [{} for _ in embeddings]
            
        if len(embeddings) != len(metadatas):
            raise ValueError("Number of embeddings must match number of metadatas")
            
        # Generate unique IDs for each embedding
        ids = [f"doc_{i}" for i in range(len(embeddings))]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query ChromaDB for similar vectors.
        
        Args:
            embedding (List[float]): Query vector
            top_k (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of metadata for top matches
        """
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )
        
        # Format results to match the interface
        return results["metadatas"][0] if results["metadatas"] else []

    def delete(self, ids: List[str]):
        """
        Delete entries by their IDs.
        
        Args:
            ids (List[str]): List of IDs to delete
        """
        self.collection.delete(ids=ids)

    def clear(self):
        """Clear all entries from the collection."""
        # Get all IDs
        results = self.collection.get()
        if results and results["ids"]:
            self.collection.delete(ids=results["ids"]) 