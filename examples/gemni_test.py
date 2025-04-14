import os
import sys
from dotenv import load_dotenv

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Load environment variables from .env file
load_dotenv()

from exo.providers.gemni import GemniProvider



async def main():
    provider = GemniProvider(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini-2.0-flash",
    )

    response = await provider.generate("Hello, how are you?", stream=False)
    for chunk in response:
        print(chunk.text, end="")






if __name__ == "__main__":
    import asyncio
    asyncio.run(main())