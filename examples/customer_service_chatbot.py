import asyncio
import os
from datetime import datetime
from typing import List, Dict, Any

from exo.providers.gemni import GemniProvider
import chromadb
from chromadb.config import Settings

class CustomerServiceChatbot:
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        # Initialize the AI provider
        self.provider = GemniProvider(
            api_key=api_key,
            model=model,
            temperature=0.7
        )
        
        # Initialize ChromaDB for persistent storage
        self.client = chromadb.PersistentClient(
            path="./customer_service_db",
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        
        # Create or get the conversation collection
        self.conversation_collection = self.client.get_or_create_collection(
            name="customer_conversations",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize conversation history
        self.current_conversation_id = None
        self.conversation_history = []
    
    async def start_conversation(self, customer_id: str) -> str:
        """Start a new conversation with a customer."""
        self.current_conversation_id = f"conv_{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.conversation_history = []
        
        # Store initial greeting
        greeting = "Hello! I'm your customer service assistant. How can I help you today?"
        self._add_to_history("assistant", greeting)
        
        return greeting
    
    def _add_to_history(self, role: str, content: str):
        """Add a message to the conversation history and store in vector DB."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(message)
        
        # Store in vector DB
        self.conversation_collection.add(
            documents=[content],
            metadatas=[{
                "role": role,
                "conversation_id": self.current_conversation_id,
                "timestamp": message["timestamp"]
            }],
            ids=[f"{self.current_conversation_id}_{len(self.conversation_history)}"]
        )
    
    async def process_message(self, message: str) -> str:
        """Process a customer message and generate a response."""
        # Add customer message to history
        self._add_to_history("user", message)
        
        # Get relevant context from previous conversations
        context = self._get_relevant_context(message)
        
        # Prepare the prompt with context
        prompt = self._prepare_prompt(message, context)
        
        # Generate response
        response = await self.provider.chat(prompt)
        
        # Add response to history
        self._add_to_history("assistant", response)
        
        return response
    
    def _get_relevant_context(self, message: str) -> List[Dict[str, Any]]:
        """Retrieve relevant context from previous conversations."""
        results = self.conversation_collection.query(
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
    
    def _prepare_prompt(self, message: str, context: List[Dict[str, Any]]) -> str:
        """Prepare the prompt with context and conversation history."""
        prompt = "You are a helpful customer service assistant. "
        prompt += "Use the following context from previous conversations to provide better assistance:\n\n"
        
        for ctx in context:
            prompt += f"Previous response: {ctx['content']}\n"
        
        prompt += "\nCurrent conversation history:\n"
        for msg in self.conversation_history[-5:]:  # Last 5 messages
            prompt += f"{msg['role']}: {msg['content']}\n"
        
        prompt += f"\nCustomer message: {message}\n"
        prompt += "Please provide a helpful and professional response."
        
        return prompt
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history

async def main():
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")
    
    # Initialize the chatbot
    chatbot = CustomerServiceChatbot(api_key=api_key)
    
    # Start a conversation
    print(await chatbot.start_conversation("customer123"))
    
    # Simulate a conversation
    messages = [
        "I'm having trouble with my order #12345",
        "It's been 3 days and I haven't received any updates",
        "Can you check the status for me?",
        "Thank you for your help!"
    ]
    
    for message in messages:
        print(f"\nCustomer: {message}")
        response = await chatbot.process_message(message)
        print(f"Assistant: {response}")
    
    # Print conversation history
    print("\nConversation History:")
    for msg in chatbot.get_conversation_history():
        print(f"{msg['role']}: {msg['content']}")

if __name__ == "__main__":
    asyncio.run(main()) 