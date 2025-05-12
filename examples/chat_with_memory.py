import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


import asyncio
import os
from exo.providers.gemni import GemniProvider


async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set the GEMINI_API_KEY environment variable")
        return
    
    # Initialize provider with chat history enabled
    provider = GemniProvider(api_key=api_key, model="gemini-2.0-flash")
    
    print("Starting conversation with memory...")
    print("Type 'exit' to end the conversation")
    print("Type 'clear' to clear the conversation history")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'clear':
            provider.clear_chat_history()
            print("Conversation history cleared!")
            continue
            
        # Chat with the provider (it will automatically maintain history)
        response = await provider.chat(user_input)
        print(f"\nAssistant: {response}")
    
    # Print conversation history
    print("\nConversation History:")
    for msg in provider.get_chat_history():
        print(f"{msg['role'].capitalize()}: {msg['content']}")

if __name__ == "__main__":
    asyncio.run(main()) 