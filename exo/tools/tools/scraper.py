"""
Web scraping utilities using BeautifulSoup.
"""
from bs4 import BeautifulSoup
import requests
import os
from typing import Dict, List, Union, Optional
from exo.tools.base import Tool

def scrape_website(url: str, selector: Optional[str] = None) -> Dict[str, Union[str, List[str], int]]:
    """
    Scrape content from a website using BeautifulSoup.
    
    Args:
        url (str): The URL of the website to scrape
        selector (str, optional): CSS selector to target specific elements
        
    Returns:
        dict: Scraped content and metadata
        
    Raises:
        ValueError: If URL is invalid or content cannot be accessed
        RuntimeError: If scraping fails
    """
    try:
        # Direct website scraping with BeautifulSoup
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # If selector provided, get specific elements
        if selector:
            elements = soup.select(selector)
            content = [elem.get_text(strip=True) for elem in elements]
        else:
            # Get all text content
            content = soup.get_text(strip=True)
            
        return {
            'url': url,
            'content': content,
            'status': response.status_code
        }
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to access URL: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Scraping failed: {str(e)}")


scraper = Tool(
    name="scrape_website",
    description="Scrape content from a website using BeautifulSoup",
    function=scrape_website,
    parameters={
        "url": {
            "type": "string",
            "description": "The URL of the website to scrape"
        }
    }
)

