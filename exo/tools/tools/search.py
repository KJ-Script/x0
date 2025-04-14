"""
Google search functionality using SerpAPI.
"""
from serpapi import GoogleSearch
import os
from exo.tools.base import Tool

def google_search(query, api_key=None, num_results=10, **kwargs):
    """
    Perform a Google search using SerpAPI.
    
    Args:
        query (str): The search query
        api_key (str, optional): SerpAPI key. If not provided, will look for SERPAPI_KEY env var
        num_results (int, optional): Number of results to return (default 10)
        **kwargs: Additional parameters to pass to SerpAPI
        
    Returns:
        dict: Search results containing organic results, knowledge graph, etc.
        
    Raises:
        ValueError: If API key is missing or invalid
        RuntimeError: If search fails
    """
    try:
        api_key = api_key or os.getenv("SERPAPI_KEY")
        if not api_key:
            raise ValueError("SerpAPI key is required")
            
        search_params = {
            "q": query,
            "api_key": api_key,
            "num": num_results,
            **kwargs
        }
        
        search = GoogleSearch(search_params)
        results = search.get_dict()
        
        return results
        
    except Exception as e:
        raise RuntimeError(f"Search failed: {str(e)}")


search = Tool(
    name="google_search",
    description="Search the web using Google",
    function=google_search,
    parameters={
        "query": {
            "type": "string",
            "description": "The search query"
        }
    }
)