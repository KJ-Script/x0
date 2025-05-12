import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import asyncio
import os
import chromadb
from exo.providers.gemni import GemniProvider


async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set the GEMINI_API_KEY environment variable")
        return
    
    # Initialize ChromaDB with current configuration
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create or get collection
    collection = client.get_or_create_collection(
        name="chat_history",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Initialize provider
    provider = GemniProvider(api_key=api_key, model="gemini-pro")
    
    print("Starting conversation with vector storage...")
    print("Type 'exit' to end the conversation")
    print("Type 'clear' to clear the conversation history")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'clear':
            collection.delete(where={})
            provider.clear_chat_history()
            print("Conversation history cleared!")
            continue
            
        # Store user message in vector DB
        collection.add(
            documents=[user_input],
            metadatas=[{"role": "user"}],
            ids=[f"msg_{len(collection.get()['ids']) + 1}"]
        )
        
        # Get response from provider
        response = await provider.chat(user_input)
        print(f"\nAssistant: {response}")
        
        # Store assistant response in vector DB
        collection.add(
            documents=[response],
            metadatas=[{"role": "assistant"}],
            ids=[f"msg_{len(collection.get()['ids']) + 1}"]
        )
    
    # Print conversation history from vector store
    print("\nConversation History from Vector Store:")
    results = collection.get()
    for doc, metadata in zip(results["documents"], results["metadatas"]):
        print(f"{metadata['role'].capitalize()}: {doc}")

if __name__ == "__main__":
    asyncio.run(main()) 