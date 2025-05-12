"""
Web Automation Tools using Playwright

This module provides tools for web automation using Playwright, allowing agents to:
- Navigate websites
- Fill forms
- Click buttons
- Extract data
- Handle authentication
- Take screenshots
"""

from typing import Dict, List, Optional, Union, Any
from playwright.async_api import async_playwright, Browser, Page, ElementHandle
from exo.tools.base import Tool
import asyncio
import json

class WebAutomation:
    """
    Web automation class that manages browser instances and provides automation tools.
    """
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self._playwright = None

    async def __aenter__(self):
        """Initialize Playwright and browser when entering context."""
        self._playwright = await async_playwright().start()
        self.browser = await self._playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting context."""
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()

async def navigate_to_url(url: str) -> Dict[str, Any]:
    """
    Navigate to a specific URL.
    
    Args:
        url (str): The URL to navigate to
        
    Returns:
        dict: Navigation result with status and metadata
    """
    async with WebAutomation() as web:
        try:
            response = await web.page.goto(url)
            return {
                'status': response.status,
                'url': url,
                'title': await web.page.title(),
                'success': response.ok
            }
        except Exception as e:
            return {
                'status': 'error',
                'url': url,
                'error': str(e),
                'success': False
            }

async def fill_form(selector: str, data: Dict[str, str]) -> Dict[str, Any]:
    """
    Fill a form with the provided data.
    
    Args:
        selector (str): CSS selector for the form
        data (dict): Dictionary of field selectors and values
        
    Returns:
        dict: Form filling result
    """
    async with WebAutomation() as web:
        try:
            form = await web.page.wait_for_selector(selector)
            for field, value in data.items():
                await web.page.fill(field, value)
            return {
                'success': True,
                'message': 'Form filled successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

async def click_element(selector: str) -> Dict[str, Any]:
    """
    Click an element on the page.
    
    Args:
        selector (str): CSS selector for the element
        
    Returns:
        dict: Click result
    """
    async with WebAutomation() as web:
        try:
            await web.page.click(selector)
            return {
                'success': True,
                'message': f'Clicked element: {selector}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

async def extract_data(selectors: Dict[str, str]) -> Dict[str, Any]:
    """
    Extract data from the page using provided selectors.
    
    Args:
        selectors (dict): Dictionary of data names and their CSS selectors
        
    Returns:
        dict: Extracted data
    """
    async with WebAutomation() as web:
        try:
            data = {}
            for name, selector in selectors.items():
                element = await web.page.wait_for_selector(selector)
                if element:
                    data[name] = await element.text_content()
            return {
                'success': True,
                'data': data
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

async def take_screenshot(selector: Optional[str] = None, path: str = "screenshot.png") -> Dict[str, Any]:
    """
    Take a screenshot of the page or a specific element.
    
    Args:
        selector (str, optional): CSS selector for the element to screenshot
        path (str): Path to save the screenshot
        
    Returns:
        dict: Screenshot result
    """
    async with WebAutomation() as web:
        try:
            if selector:
                element = await web.page.wait_for_selector(selector)
                await element.screenshot(path=path)
            else:
                await web.page.screenshot(path=path)
            return {
                'success': True,
                'path': path
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Create Tool instances
navigate_tool = Tool(
    name="navigate_to_url",
    description="Navigate to a specific URL",
    function=navigate_to_url,
    parameters={
        "url": {
            "type": "string",
            "description": "The URL to navigate to"
        }
    }
)

fill_form_tool = Tool(
    name="fill_form",
    description="Fill a form with provided data",
    function=fill_form,
    parameters={
        "selector": {
            "type": "string",
            "description": "CSS selector for the form"
        },
        "data": {
            "type": "object",
            "description": "Dictionary of field selectors and values"
        }
    }
)

click_tool = Tool(
    name="click_element",
    description="Click an element on the page",
    function=click_element,
    parameters={
        "selector": {
            "type": "string",
            "description": "CSS selector for the element to click"
        }
    }
)

extract_tool = Tool(
    name="extract_data",
    description="Extract data from the page using selectors",
    function=extract_data,
    parameters={
        "selectors": {
            "type": "object",
            "description": "Dictionary of data names and their CSS selectors"
        }
    }
)

screenshot_tool = Tool(
    name="take_screenshot",
    description="Take a screenshot of the page or element",
    function=take_screenshot,
    parameters={
        "selector": {
            "type": "string",
            "description": "Optional CSS selector for the element to screenshot"
        },
        "path": {
            "type": "string",
            "description": "Path to save the screenshot"
        }
    }
) 