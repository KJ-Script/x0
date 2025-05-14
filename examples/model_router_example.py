"""
Example demonstrating the usage of ModelRouterProvider.
"""

import asyncio
import os
from dotenv import load_dotenv
from exo.providers import ModelRouterProvider

async def main():
    # Load environment variables
    load_dotenv()
    
    # Configure the model router
    config = {
        "openai": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "models": ["gpt-3.5-turbo", "gpt-4"]
        },
        "anthropic": {
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "models": ["claude-2", "claude-instant-1"]
        },
        "gemini": {
            "api_key": os.getenv("GEMINI_API_KEY"),
            "models": ["gemini-pro"]
        }
    }
    
    # Initialize the model router
    router = ModelRouterProvider(
        config=config,
        default_model="openai/gpt-3.5-turbo",
        temperature=0.7
    )
    
    # Example 1: Using the default model
    print("\nExample 1: Using default model (GPT-3.5)")
    response = await router.chat("What is the capital of France?")
    print(f"Response: {response}")
    
    # Example 2: Using a specific model
    print("\nExample 2: Using Claude-2")
    response = await router.chat(
        "Explain quantum computing in simple terms",
        model="anthropic/claude-2"
    )
    print(f"Response: {response}")
    
    # Example 3: Using Gemini
    print("\nExample 3: Using Gemini Pro")
    response = await router.chat(
        "Write a short poem about AI",
        model="google/gemini-pro"
    )
    print(f"Response: {response}")
    
    # Example 4: Batch processing with different models
    print("\nExample 4: Batch processing")
    prompts = [
        "What is machine learning?",
        "Explain neural networks",
        "What is deep learning?"
    ]
    
    # Process each prompt with a different model
    models = [
        "openai/gpt-3.5-turbo",
        "anthropic/claude-2",
        "google/gemini-pro"
    ]
    
    for prompt, model in zip(prompts, models):
        print(f"\nProcessing with {model}:")
        response = await router.generate(prompt, model=model)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
    
    # Example 5: Getting model information
    print("\nExample 5: Model Information")
    model_info = router.get_model_info()
    print(f"Available models: {router.list_models()}")
    print(f"Model capabilities: {model_info['models']}")

if __name__ == "__main__":
    asyncio.run(main()) 