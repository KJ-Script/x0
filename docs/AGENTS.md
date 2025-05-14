# Exo Agents and Tools

## Table of Contents
1. [Overview](#overview)
2. [Basic Agent Usage](#basic-agent-usage)
3. [Tools](#tools)
4. [Memory Management](#memory-management)
5. [Advanced Usage](#advanced-usage)
6. [Best Practices](#best-practices)

## Overview

Exo provides a flexible agent system that can use various AI models and tools to accomplish tasks. Agents are AI-powered executors that can:
- Use language models for reasoning and generation
- Use tools for web automation, search, scraping, etc.
- Maintain state and context
- Chain multiple actions together
- Learn from their interactions
- Adapt to different scenarios

## Basic Agent Usage

### Creating an Agent

```python
from exo.agents.base import Agent
from exo.providers.gemni import GemniProvider
´
# Initialize provider and agent
provider = GemniProvider(api_key="your-api-key", model="gemini-pro")
agent = Agent(provider, name="MyAgent")

# Use the agent
response = await agent.act("What's the weather in Paris?")
print(f"Agent: {response}")
```

### Agent Configuration

```python
# Create agent with custom configuration
agent = Agent(
    provider=provider,
    name="CustomAgent",
    max_iterations=5,        # Maximum number of tool calls
    temperature=0.7,         # Controls response randomness
    memory_enabled=True,     # Enable memory
    verbose=True            # Enable detailed logging
)
```

## Tools

### Available Tools

#### Web Automation
```python
from exo.tools.tools.web_automation import navigate_tool, extract_tool

# Navigate to a URL
await navigate_tool("https://example.com")

# Extract data from a page
data = await extract_tool(
    "https://example.com",
    selector=".content",
    timeout=30
)
```

#### Web Search
```python
from exo.tools.tools.search import search_tool

# Basic search
results = await search_tool("latest AI developments")

# Advanced search
results = await search_tool(
    "AI news",
    num_results=5,
    time_range="last_week"
)
```

#### Web Scraping
```python
from exo.tools.tools.scraping import scrape_tool

# Basic scraping
content = await scrape_tool("https://example.com")

# Scraping with options
content = await scrape_tool(
    "https://example.com",
    selector="article",
    timeout=30,
    wait_for=".content"
)
```

### Creating Custom Tools

```python
from exo.tools.base import Tool

class MyCustomTool(Tool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="My custom tool for specific tasks",
            parameters={
                "param1": {
                    "type": "string",
                    "description": "First parameter"
                },
                "param2": {
                    "type": "integer",
                    "description": "Second parameter"
                }
            }
        )
    
    async def execute(self, param1: str, param2: int, **kwargs):
        # Tool implementation
        result = f"Processed {param1} with value {param2}"
        return result

# Use custom tool
agent = Agent(provider, tools=[MyCustomTool()])
```

### Tool Chaining

```python
async def complex_task(agent):
    # Chain multiple tool calls
    search_results = await agent.tools[0].execute("AI news")
    content = await agent.tools[1].execute(search_results[0])
    summary = await agent.act(f"Summarize this content: {content}")
    return summary
```

## Memory Management

### Basic Memory

```python
# Add to memory
agent.remember({
    "action": "searched",
    "query": "AI news",
    "timestamp": "2024-03-20"
})

# Get memory
memory = agent.get_memory()
print(f"Memory: {memory}")

# Clear memory
agent.clear_memory()
```

### Vector Storage Memory

```python
import chromadb

# Initialize vector storage
client = chromadb.PersistentClient(path="./agent_memory")
collection = client.get_or_create_collection(
    name="agent_memory",
    metadata={"hnsw:space": "cosine"}
)

# Store in vector DB
collection.add(
    documents=["memory content"],
    metadatas=[{
        "action": "searched",
        "timestamp": "2024-03-20"
    }],
    ids=["mem_1"]
)

# Retrieve with semantic search
results = collection.query(
    query_texts=["previous searches about AI"],
    n_results=5
)
```

## Advanced Usage

### Context-Aware Agent

```python
class ContextAwareAgent(Agent):
    def __init__(self, provider, tools=None, name=None):
        super().__init__(provider, tools, name)
        self.context = {}
    
    async def act(self, prompt: str, **kwargs):
        # Use context in actions
        if "previous_topic" in self.context:
            prompt = f"Regarding {self.context['previous_topic']}: {prompt}"
        return await super().act(prompt, **kwargs)
    
    def update_context(self, key: str, value: any):
        self.context[key] = value
```

### Tool Selection Strategy

```python
class SmartAgent(Agent):
    async def select_tool(self, task: str) -> Tool:
        # Implement custom tool selection logic
        if "search" in task.lower():
            return self.tools[0]  # Search tool
        elif "scrape" in task.lower():
            return self.tools[1]  # Scraping tool
        return self.tools[2]  # Default tool
```

### Error Recovery

```python
class ResilientAgent(Agent):
    async def act(self, prompt: str, **kwargs):
        try:
            return await super().act(prompt, **kwargs)
        except Exception as e:
            # Log error
            self.log_error(e)
            # Try alternative approach
            return await self.fallback_action(prompt)
    
    async def fallback_action(self, prompt: str):
        # Implement fallback logic
        return "I encountered an error. Here's what I can tell you..."
```

## Best Practices

1. **Tool Selection**
   - Choose tools that match your agent's purpose
   - Keep the number of tools manageable
   - Document tool capabilities clearly
   - Implement proper error handling

2. **Memory Management**
   - Use memory for important context
   - Clear memory when starting new tasks
   - Consider using vector storage for long-term memory
   - Implement memory cleanup strategies

3. **Error Handling**
   - Handle tool execution errors gracefully
   - Provide fallback options
   - Log important actions and errors
   - Implement retry mechanisms

4. **Security**
   - Validate tool inputs
   - Limit tool access as needed
   - Handle sensitive data appropriately
   - Implement rate limiting

5. **Performance**
   - Use async/await for concurrent operations
   - Implement proper caching
   - Monitor resource usage
   - Optimize tool execution

6. **Testing**
   - Write unit tests for tools
   - Test agent behavior
   - Implement integration tests
   - Monitor agent performance

### Example: Research Agent

```python
import asyncio
from exo.agents.base import Agent
from exo.providers.gemni import GemniProvider
from exo.tools.tools.web_automation import navigate_tool, extract_tool
from exo.tools.tools.search import search_tool

class ResearchAgent(Agent):
    def __init__(self, provider, tools=None, name=None):
        super().__init__(provider, tools, name)
        self.research_history = []
    
    async def research(self, topic: str):
        # Search for information
        search_results = await self.tools[0].execute(topic)
        
        # Extract content from results
        contents = []
        for result in search_results[:3]:
            content = await self.tools[1].execute(result)
            contents.append(content)
        
        # Generate summary
        summary = await self.act(
            f"Summarize these findings about {topic}: {contents}"
        )
        
        # Store in history
        self.research_history.append({
            "topic": topic,
            "summary": summary,
            "timestamp": "2024-03-20"
        })
        
        return summary

async def main():
    # Initialize agent
    provider = GemniProvider(api_key="your-api-key", model="gemini-pro")
    agent = ResearchAgent(
        provider=provider,
        tools=[search_tool, extract_tool],
        name="ResearchAgent"
    )
    
    # Research task
    summary = await agent.research("latest AI developments")
    print(f"Research Summary: {summary}")
    
    # Get research history
    print("\nResearch History:")
    for item in agent.research_history:
        print(f"Topic: {item['topic']}")
        print(f"Summary: {item['summary']}\n")

if __name__ == "__main__":
    asyncio.run(main())
``` 