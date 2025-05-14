import asyncio
import os
from datetime import datetime
from typing import List, Dict, Any

from exo.providers.gemni import GemniProvider
import chromadb
from chromadb.config import Settings

# Initialize global variables
conversation_history = []
current_conversation_id = None
provider = None
conversation_collection = None

async def initialize_chatbot(api_key: str, model: str = "gemini-pro"):
    """Initialize the chatbot components."""
    global provider, conversation_collection
    
    # Initialize the AI provider
    provider = GemniProvider(
        api_key=api_key,
        model=model,
        temperature=0.7
    )
    
    # Initialize ChromaDB for persistent storage
    client = chromadb.PersistentClient(
        path="./customer_service_db",
        settings=Settings(
            anonymized_telemetry=False
        )
    )
    
    # Create or get the conversation collection
    conversation_collection = client.get_or_create_collection(
        name="customer_conversations",
        metadata={"hnsw:space": "cosine"}
    )

async def start_conversation(customer_id: str) -> str:
    """Start a new conversation with a customer."""
    global current_conversation_id, conversation_history
    
    current_conversation_id = f"conv_{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    conversation_history = []
    
    # Store initial greeting
    greeting = "Hello! I'm your customer service assistant. How can I help you today?"
    await add_to_history("assistant", greeting)
    
    return greeting

async def add_to_history(role: str, content: str):
    """Add a message to the conversation history and store in vector DB."""
    global conversation_history, current_conversation_id
    
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    conversation_history.append(message)
    
    # Store in vector DB
    conversation_collection.add(
        documents=[content],
        metadatas=[{
            "role": role,
            "conversation_id": current_conversation_id,
            "timestamp": message["timestamp"]
        }],
        ids=[f"{current_conversation_id}_{len(conversation_history)}"]
    )

def get_relevant_context(message: str) -> List[Dict[str, Any]]:
    """Retrieve relevant context from previous conversations."""
    results = conversation_collection.query(
        query_texts=[message],
        n_results=5,
        where={"role": "assistant"}  # Only get previous assistant responses
    )
    
    return [
        {
            "content": doc,
            "metadata": meta
        }
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]

def prepare_prompt(message: str, context: List[Dict[str, Any]]) -> str:
    """Prepare the prompt with context and conversation history."""
    prompt = "You are a helpful customer service assistant. "
    prompt += "Use the following context from previous conversations to provide better assistance:\n\n"
    
    for ctx in context:
        prompt += f"Previous response: {ctx['content']}\n"
    
    prompt += "\nCurrent conversation history:\n"
    for msg in conversation_history[-5:]:  # Last 5 messages
        prompt += f"{msg['role']}: {msg['content']}\n"
    
    prompt += f"\nCustomer message: {message}\n"
    prompt += "Please provide a helpful and professional response."
    
    return prompt

async def process_message(message: str) -> str:
    """Process a customer message and generate a response."""
    # Add customer message to history
    await add_to_history("user", message)
    
    # Get relevant context from previous conversations
    context = get_relevant_context(message)
    
    # Prepare the prompt with context
    prompt = prepare_prompt(message, context)
    
    # Generate response
    response = await provider.chat(prompt)
    
    # Add response to history
    await add_to_history("assistant", response)
    
    return response

def get_conversation_history() -> List[Dict[str, str]]:
    """Get the current conversation history."""
    return conversation_history

async def main():
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")
    
    # Initialize the chatbot
    await initialize_chatbot(api_key=api_key)
    
    # Start a conversation
    print(await start_conversation("customer123"))
    
    # Simulate a conversation
    messages = [
        "I'm having trouble with my order #12345",
        "It's been 3 days and I haven't received any updates",
        "Can you check the status for me?",
        "Thank you for your help!"
    ]
    
    for message in messages:
        print(f"\nCustomer: {message}")
        response = await process_message(message)
        print(f"Assistant: {response}")
    
    # Print conversation history
    print("\nConversation History:")
    for msg in get_conversation_history():
        print(f"{msg['role']}: {msg['content']}")

if __name__ == "__main__":
    asyncio.run(main()) 