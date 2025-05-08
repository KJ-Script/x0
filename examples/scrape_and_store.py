"""
Example: Scraping websites and storing content in a vector database.

This example demonstrates:
1. Scraping content from multiple websites using the Tool class
2. Generating embeddings for the content
3. Storing the content and embeddings in ChromaDB
4. Searching through the stored content using semantic similarity
"""

import asyncio
from exo.tools.tools.scraper import scraper  # Import the Tool instance
from exo.providers.vector_db import ChromaDBAdapter
from exo.providers.gemni import GemniProvider

async def main():
    # Initialize providers
    provider = GemniProvider(api_key="your-api-key", model="gemini-pro")
    db = ChromaDBAdapter("./scraped_data", "web_content")
    
    # List of websites to scrape
    urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://en.wikipedia.org/wiki/Machine_learning", 
        "https://en.wikipedia.org/wiki/Deep_learning"
    ]

    print("Scraping websites and storing content...")
    
    # Scrape and store content using the Tool instance
    for url in urls:
        try:
            # Use the Tool instance directly
            result = scraper(url=url)  # Note: using named parameter as defined in the Tool
            content = result['content']
            
            # Split content into chunks
            chunks = [p for p in content.split('\n') if p.strip()]
            
            print(f"Processing {len(chunks)} chunks from {url}")
            
            # Generate embeddings and store in vector DB
            for i, chunk in enumerate(chunks):
                # Get embedding for the chunk
                embedding = [float(x) for x in (await provider.generate(
                    f"Generate embedding for: {chunk}")).split()[:384]]
                
                # Store in vector DB with metadata
                db.add(
                    embeddings=[embedding],
                    metadatas=[{
                        'url': url,
                        'chunk_index': i,
                        'text': chunk
                    }]
                )
            
            print(f"Stored content from {url}")
            
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")

    print("\nTesting semantic search...")
    
    # Example queries
    queries = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "Explain deep learning"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        
        # Get embedding for the query
        query_emb = [float(x) for x in (await provider.generate(
            f"Generate embedding for: {query}")).split()[:384]]
        
        # Search for similar content
        results = db.query(query_emb, top_k=2)
        
        # Display results
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"URL: {result['url']}")
            print(f"Text: {result['text'][:200]}...")  # Show first 200 chars

if __name__ == "__main__":
    asyncio.run(main())