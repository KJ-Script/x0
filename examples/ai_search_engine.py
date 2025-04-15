"""
AI Search Engine Example

This example demonstrates how to use the Gemini provider with search and scrape tools
to create an AI-powered search engine that can search the web and analyze the results.
"""
import os, sys
import asyncio
import json
from dotenv import load_dotenv


# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from exo.providers.gemni import GemniProvider
from exo.agents.agents.search import webscraper_agent

load_dotenv()
async def main():
    # Get API keys from environment variables
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    serpapi_key = os.getenv("SERPAPI_KEY")
    
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        return
    
    if not serpapi_key:
        print("Error: SERPAPI_KEY environment variable not set")
        return
    
    # Initialize the Gemini provider
    provider = GemniProvider(
        api_key=gemini_api_key,
        model="gemini-2.0-flash",
        temperature=0.7,
        max_output_tokens=1000
    )
    
    # Example search queries
    queries = [
        "What are the latest developments in quantum computing?",
        "Who are the top 5 AI companies in 2024?",
        "What are the best practices for Python async programming?"
    ]
    
    # Process each query
    for query in queries:
        print(f"\n\n{'='*50}")
        print(f"Processing query: {query}")
        print(f"{'='*50}\n")
        
        try:
            # Run the webscraper agent
            results = await webscraper_agent(query, provider)
            
            # Print the final answer
            print("\nFINAL ANSWER:")
            print(results["final_answer"])
            
            # Print the steps taken
            print("\nSTEPS TAKEN:")
            for step in results["steps"]:
                print(f"Step {step['step']}: Used {step['tool']} with parameters {step['parameters']}")
                print(f"Result: {json.dumps(step['result'], indent=2)[:200]}...")
                print("-" * 30)
                
        except Exception as e:
            print(f"Error processing query: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 