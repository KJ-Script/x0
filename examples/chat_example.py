"""
Chat Example with Gemini Provider

This example demonstrates how to use the chat functionality of the Gemini provider
to maintain conversation history and provide more context-aware responses.
"""
import os
import asyncio
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from exo.providers.gemni import GemniProvider

async def main():
    # Get API key from environment variable
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        return
    
    # Initialize the Gemini provider
    provider = GemniProvider(
        api_key=gemini_api_key,
        model="gemini-2.0-flash",
        temperature=0.7,
        max_output_tokens=1000
    )
    
    # Set a system prompt to define the assistant's role
    system_prompt = """You are a helpful AI assistant with expertise in technology and programming.
You provide clear, concise, and accurate information.
You can help with coding questions, explain technical concepts, and offer advice on best practices."""
    
    # Start a conversation
    print("Chat with Gemini (type 'exit' to quit)")
    print("-" * 50)
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nGoodbye!")
            break
        
        # Get response from the provider
        try:
            response = await provider.chat(
                message=user_input,
                system_prompt=system_prompt if provider.get_chat_history() == [] else None
            )
            
            # Print the response
            print(f"\nAssistant: {response}")
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 