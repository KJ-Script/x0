# Exo API Documentation

## Table of Contents
1. [Base Provider](#base-provider)
2. [Gemini Provider](#gemini-provider)
3. [Vector Storage](#vector-storage)
4. [Memory Management](#memory-management)
5. [Error Handling](#error-handling)
6. [Configuration](#configuration)

## Base Provider

The `BaseProvider` class defines the common interface for all AI model providers. It ensures consistent behavior across different providers while allowing provider-specific implementations.

### Methods

#### `chat(message: str, **kwargs) -> str`
Send a message to the provider and get a response. This method handles the conversation flow and maintains context.

```python
# Basic usage
response = await provider.chat("Hello, how are you?")

# With additional parameters
response = await provider.chat(
    "Tell me about AI",
    temperature=0.7,
    max_tokens=500
)
```

#### `get_chat_history() -> List[Dict[str, str]]`
Retrieve the conversation history. Each message in the history is a dictionary with 'role' and 'content' keys.

```python
# Get full history
history = provider.get_chat_history()
for msg in history:
    print(f"{msg['role']}: {msg['content']}")

# Filter history by role
user_messages = [msg for msg in history if msg['role'] == 'user']
```

#### `clear_chat_history()`
Clear the conversation history. Useful when starting a new conversation or managing memory.

```python
# Clear history
provider.clear_chat_history()

# Verify history is cleared
assert len(provider.get_chat_history()) == 0
```

## Gemini Provider

The `GemniProvider` class implements the BaseProvider interface for Google's Gemini models.

### Initialization

```python
from exo.providers.gemni import GemniProvider

provider = GemniProvider(
    api_key="your-api-key",  # Required: Your Gemini API key
    model="gemini-pro",      # Required: Model to use
    temperature=0.7,         # Optional: Controls randomness (0.0 to 1.0)
    max_output_tokens=500,   # Optional: Maximum response length
    top_p=0.95,             # Optional: Nucleus sampling parameter
    top_k=40                # Optional: Top-k sampling parameter
)
```

### Methods

Inherits all methods from `BaseProvider` plus:

#### `generate(prompt: str, **kwargs) -> str`
Generate text without maintaining chat history. Useful for one-off generations.

```python
# Basic generation
response = await provider.generate("Write a poem about AI")

# With parameters
response = await provider.generate(
    "Write a story",
    temperature=0.8,
    max_tokens=1000
)
```

## Vector Storage

Exo uses ChromaDB for vector storage, enabling semantic search and persistent memory.

### ChromaDB Integration

```python
import chromadb
from exo.providers.gemni import GemniProvider

# Initialize ChromaDB with persistent storage
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="chat_history",
    metadata={"hnsw:space": "cosine"}  # Use cosine similarity
)

# Store messages with metadata
collection.add(
    documents=["message content"],
    metadatas=[{
        "role": "user",
        "timestamp": "2024-03-20",
        "topic": "AI"
    }],
    ids=["unique_id"]
)

# Retrieve messages
results = collection.get()
```

### Semantic Search

```python
# Basic search
results = collection.query(
    query_texts=["your search query"],
    n_results=5
)

# Search with metadata filtering
results = collection.query(
    query_texts=["AI developments"],
    n_results=5,
    where={"role": "assistant"},
    where_document={"$contains": "machine learning"}
)
```

## Memory Management

### In-Memory Storage

```python
# Add to history
provider.add_to_history("user", "Hello")
provider.add_to_history("assistant", "Hi! How can I help?")

# Get history
history = provider.get_chat_history()
for msg in history:
    print(f"{msg['role']}: {msg['content']}")

# Clear history
provider.clear_chat_history()
```

### Vector Storage

```python
# Store in vector DB
collection.add(
    documents=["message content"],
    metadatas=[{
        "role": "user",
        "timestamp": "2024-03-20",
        "topic": "AI"
    }],
    ids=["msg_1"]
)

# Retrieve with metadata filtering
results = collection.get(
    where={"role": "user"},
    where_document={"$contains": "specific text"}
)

# Search with multiple conditions
results = collection.get(
    where={
        "role": "user",
        "timestamp": {"$gte": "2024-03-19"}
    },
    where_document={"$contains": "AI"}
)
```

## Error Handling

Exo provides comprehensive error handling for various scenarios:

```python
from exo.providers.base import ProviderError

try:
    # Basic chat
    response = await provider.chat("Hello")
except ProviderError as e:
    print(f"Provider error: {e}")
    # Handle provider-specific errors
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle other errors

# Error handling with retries
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def chat_with_retry(provider, message):
    try:
        return await provider.chat(message)
    except ProviderError as e:
        print(f"Retrying after error: {e}")
        raise
```

## Configuration

### Environment Variables

```bash
# Required
export GEMINI_API_KEY=your-api-key-here

# Optional
export GEMINI_MODEL=gemini-pro
export GEMINI_TEMPERATURE=0.7
export GEMINI_MAX_TOKENS=500
```

### Provider Configuration

```python
import os
from exo.providers.gemni import GemniProvider

# Basic configuration
provider = GemniProvider(
    api_key=os.getenv("GEMINI_API_KEY"),
    model=os.getenv("GEMINI_MODEL", "gemini-pro"),
    temperature=float(os.getenv("GEMINI_TEMPERATURE", "0.5")),
    max_output_tokens=int(os.getenv("GEMINI_MAX_TOKENS", "500"))
)

# Advanced configuration
provider = GemniProvider(
    api_key=os.getenv("GEMINI_API_KEY"),
    model=os.getenv("GEMINI_MODEL", "gemini-pro"),
    temperature=float(os.getenv("GEMINI_TEMPERATURE", "0.5")),
    max_output_tokens=int(os.getenv("GEMINI_MAX_TOKENS", "500")),
    top_p=float(os.getenv("GEMINI_TOP_P", "0.95")),
    top_k=int(os.getenv("GEMINI_TOP_K", "40")),
    safety_settings={
        "HARASSMENT": "block_none",
        "HATE_SPEECH": "block_none",
        "SEXUALLY_EXPLICIT": "block_none",
        "DANGEROUS_CONTENT": "block_none"
    }
)
```

### Configuration Best Practices

1. **API Key Management**
   - Store API keys in environment variables
   - Use a `.env` file for local development
   - Rotate keys regularly
   - Never commit keys to version control

2. **Model Configuration**
   - Choose appropriate model for your use case
   - Adjust temperature based on desired creativity
   - Set appropriate token limits
   - Configure safety settings as needed

3. **Error Handling**
   - Implement proper error handling
   - Use retries for transient failures
   - Log errors appropriately
   - Provide fallback options

4. **Performance**
   - Use async/await for concurrent operations
   - Implement proper caching
   - Monitor API usage and costs
   - Optimize token usage 