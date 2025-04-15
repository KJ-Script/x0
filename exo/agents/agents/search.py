"""
WebScraper agent that lets the provider decide tool usage.
"""
from typing import List, Dict, Any, Optional
from exo.tools.base import Tool
from exo.providers.base import BaseProvider
from exo.tools.tools.search import search
from exo.tools.tools.scraper import scraper 

async def webscraper_agent(
    query: str,
    provider: BaseProvider,
) -> Dict[str, Any]:
    """
    An agent that lets the provider decide how to use search and scraping tools.
    
    Args:
        query (str): The user's query or research topic
        provider (BaseProvider): The language model provider to use
    """
    # Create tool descriptions for the provider
    available_tools = {
        "google_search": {
            "name": search.name,
            "description": search.description,
            "parameters": search.parameters
        },
        "scrape_website": {
            "name": scraper.name,
            "description": scraper.description,
            "parameters": scraper.parameters
        }
    }
    
    # Initial system prompt that explains available tools
    system_prompt = f"""You are a web research agent with access to these tools:

1. {search.name}: {search.description}
   Parameters: {search.parameters}

2. {scraper.name}: {scraper.description}
   Parameters: {scraper.parameters}

When you need to use a tool, format your response like this:
USE_TOOL: <tool_name>
PARAMETERS: <parameters as json>

After getting tool results, you can use another tool or provide final answer.
Always explain your thinking before using a tool.

Example:
"I'll search for relevant websites first.
USE_TOOL: google_search
PARAMETERS: {{"query": "example query", "num_results": 3}}"
"""

    conversation_history = []
    max_steps = 5  # Prevent infinite loops
    step = 0
    
    while step < max_steps:
        # If it's the first step, use the original query
        if step == 0:
            current_prompt = query
        
        # Get the provider's decision
        response = await provider.generate(
            system_prompt + "\n\nCurrent task: " + current_prompt + 
            "\n\nConversation history: " + str(conversation_history)
        )
        
        # Check if the response contains a tool call
        if "USE_TOOL:" in response:
            # Parse the tool call
            tool_parts = response.split("USE_TOOL:")[1].split("PARAMETERS:")
            tool_name = tool_parts[0].strip()
            tool_params = eval(tool_parts[1].strip())  # Convert string to dict
            
            # Execute the tool
            if tool_name == "google_search":
                result = search(**tool_params)
            elif tool_name == "scrape_website":
                result = scraper(**tool_params)
            else:
                result = {"error": "Unknown tool"}
            
            # Add to conversation history
            conversation_history.append({
                "step": step,
                "tool": tool_name,
                "parameters": tool_params,
                "result": result
            })
            
            # Update the prompt with the result
            current_prompt = f"Tool {tool_name} returned: {result}\nWhat should we do next?"
            
        else:
            # If no tool call, assume it's the final answer
            return {
                "query": query,
                "steps": conversation_history,
                "final_answer": response
            }
        
        step += 1
    
    return {
        "query": query,
        "steps": conversation_history,
        "final_answer": "Max steps reached without conclusion"
    }