"""
Vector Database Adapters for Exo Library

This package provides vector database adapters that can be used with any provider
for tasks like retrieval-augmented generation, semantic search, and embedding storage.
"""

from .base import VectorDBAdapter
from .in_memory import InMemoryVectorDB
from .chroma import ChromaDBAdapter

__all__ = ['VectorDBAdapter', 'InMemoryVectorDB', 'ChromaDBAdapter'] 