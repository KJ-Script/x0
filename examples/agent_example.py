import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from exo.agents.base import Agent
from exo.providers.gemni import GemniProvider
from exo.tools.tools.web_automation import navigate_tool, extract_tool

async def main():
    api_key = os.getenv("GEMINI_API_KEY")    
    provider = GemniProvider(api_key=api_key, model="gemini-2.0-flash")
    agent = Agent(provider, tools=[navigate_tool, extract_tool], name="WebAgent")

    response = await agent.act("What is the weather in Paris?")
    print("Agent response:", response)
    print(agent) 
    print("Tools:", agent.list_tools())

    response = await agent.act("remind me of the weather again")
    print("Agent response:", response)

    response = await agent.act("What cities weather did you just give me")
    print("Agent response:", response)



if __name__ == "__main__":
    asyncio.run(main())