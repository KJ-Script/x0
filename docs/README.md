# Exo Documentation

Exo is a powerful Python library for working with various AI models and tools, providing a unified interface for different providers and capabilities. It enables seamless integration of AI models, memory management, and various tools for web automation, search, and data processing.

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Concepts](#core-concepts)
4. [Providers](#providers)
5. [Memory Management](#memory-management)
6. [Tools and Agents](#tools-and-agents)
7. [Examples](#examples)
8. [Best Practices](#best-practices)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Basic Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/exo.git
cd exo

# Install dependencies
pip install -r requirements.txt
```

### Optional Dependencies
Some features require additional packages:
```bash
# For web automation
pip install playwright
playwright install

# For vector storage
pip install chromadb
```

## Quick Start

### Basic Chat Example
Here's a simple example of using Exo for basic chat functionality:

```python
import asyncio
from exo.providers.gemni import GemniProvider

async def main():
    # Initialize provider with your API key
    provider = GemniProvider(
        api_key="your-api-key",
        model="gemini-pro",
        temperature=0.7  # Controls response randomness
    )
    
    # Simple chat
    response = await provider.chat("Hello, how are you?")
    print(f"AI: {response}")
    
    # Continue the conversation
    response = await provider.chat("Tell me more about yourself")
    print(f"AI: {response}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Using Memory
Exo provides built-in memory management for maintaining conversation context:

```python
import asyncio
from exo.providers.gemni import GemniProvider

async def main():
    provider = GemniProvider(api_key="your-api-key", model="gemini-pro")
    
    # First message
    response1 = await provider.chat("What's the weather like in Paris?")
    print(f"AI: {response1}")
    
    # Second message (with context)
    response2 = await provider.chat("What about tomorrow?")
    print(f"AI: {response2}")
    
    # Get conversation history
    history = provider.get_chat_history()
    print("\nConversation History:")
    for msg in history:
        print(f"{msg['role']}: {msg['content']}")
    
    # Clear history if needed
    provider.clear_chat_history()

if __name__ == "__main__":
    asyncio.run(main())
```

### Vector Storage
For persistent storage and semantic search capabilities:

```python
import asyncio
import chromadb
from exo.providers.gemni import GemniProvider

async def main():
    # Initialize ChromaDB with persistent storage
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(
        name="chat_history",
        metadata={"hnsw:space": "cosine"}  # Use cosine similarity for search
    )
    
    # Initialize provider
    provider = GemniProvider(api_key="your-api-key", model="gemini-pro")
    
    # Chat and store in vector DB
    response = await provider.chat("Tell me about AI")
    
    # Store in vector DB with metadata
    collection.add(
        documents=[response],
        metadatas=[{
            "role": "assistant",
            "timestamp": "2024-03-20",
            "topic": "AI"
        }],
        ids=[f"msg_{len(collection.get()['ids']) + 1}"]
    )
    
    # Search for similar messages
    results = collection.query(
        query_texts=["What are the latest developments in AI?"],
        n_results=5
    )
    print("\nSimilar messages found:")
    for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
        print(f"Content: {doc}")
        print(f"Metadata: {metadata}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

## Core Concepts

### Providers
Providers are the core components that interface with different AI models. Each provider:
- Implements a common interface
- Handles API communication
- Manages conversation state
- Provides model-specific features

### Memory Management
Exo offers two types of memory management:
1. **In-Memory Storage**
   - Maintains conversation context during the session
   - Fast and efficient for short-term memory
   - Cleared when the program ends

2. **Vector Storage**
   - Persistent storage using ChromaDB
   - Enables semantic search
   - Suitable for long-term memory
   - Supports metadata filtering

### Tools and Agents
- **Tools**: Reusable components for specific tasks
- **Agents**: AI-powered executors that can use tools
- **Memory**: Context management for agents
- **Chaining**: Combining multiple tools and actions

## Providers

### Gemini Provider
```python
from exo.providers.gemni import GemniProvider

provider = GemniProvider(
    api_key="your-api-key",
    model="gemini-pro",
    temperature=0.7,         # Controls randomness (0.0 to 1.0)
    max_output_tokens=500,   # Maximum response length
    top_p=0.95,             # Nucleus sampling parameter
    top_k=40                # Top-k sampling parameter
)
```

### OpenAI Provider
```python
from exo.providers.openai import OpenAIProvider

provider = OpenAIProvider(
    api_key="your-api-key",
    model="gpt-3.5-turbo",
    temperature=0.7,
    max_tokens=500
)
```

### Anthropic Provider
```python
from exo.providers.anthropic import AnthropicProvider

provider = AnthropicProvider(
    api_key="your-api-key",
    model="claude-2",
    temperature=0.7,
    max_tokens=500
)
```

## Memory Management

### In-Memory Storage
```python
# Add messages to history
provider.add_to_history("user", "Hello")
provider.add_to_history("assistant", "Hi! How can I help?")

# Get conversation history
history = provider.get_chat_history()
for msg in history:
    print(f"{msg['role']}: {msg['content']}")

# Clear history
provider.clear_chat_history()
```

### Vector Storage
```python
import chromadb

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="chat_history",
    metadata={"hnsw:space": "cosine"}
)

# Store messages with metadata
collection.add(
    documents=["message content"],
    metadatas=[{
        "role": "user",
        "timestamp": "2024-03-20",
        "topic": "AI"
    }],
    ids=["msg_1"]
)

# Search with metadata filtering
results = collection.get(
    where={"role": "user"},
    where_document={"$contains": "AI"}
)
```

## Tools and Agents

### Basic Agent
```python
from exo.agents.base import Agent
from exo.providers.gemni import GemniProvider

# Initialize agent
provider = GemniProvider(api_key="your-api-key", model="gemini-pro")
agent = Agent(provider, name="MyAgent")

# Use agent
response = await agent.act("What's the weather in Paris?")
```

### Agent with Tools
```python
from exo.tools.tools.web_automation import navigate_tool, extract_tool
from exo.tools.tools.search import search_tool

# Create agent with tools
agent = Agent(
    provider=provider,
    tools=[navigate_tool, extract_tool, search_tool],
    name="WebAgent"
)

# List available tools
print(agent.list_tools())
```

## Examples

Check the `examples/` directory for complete working examples:

1. `chat_with_memory.py`: Basic chat with memory management
2. `chat_with_vectordb.py`: Chat with vector storage
3. `agent_example.py`: Using agents with tools
4. `web_automation_example.py`: Web automation capabilities
5. `scrape_and_store.py`: Web scraping and storage
6. `ai_search_engine.py`: AI-powered search

## Best Practices

1. **API Key Management**
   - Use environment variables for API keys
   - Never commit API keys to version control
   - Rotate keys regularly

2. **Memory Management**
   - Use in-memory storage for short conversations
   - Use vector storage for long-term memory
   - Clear memory when starting new tasks

3. **Error Handling**
   - Always wrap API calls in try-except blocks
   - Implement proper error logging
   - Provide fallback options

4. **Performance**
   - Use async/await for concurrent operations
   - Implement proper caching
   - Monitor API usage and costs

5. **Security**
   - Validate all inputs
   - Sanitize outputs
   - Implement rate limiting
   - Handle sensitive data appropriately 