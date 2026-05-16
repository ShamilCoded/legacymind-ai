"""
Basic usage example for the embeddings pipeline.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.embeddings import create_pipeline


def main():
    """Demonstrate basic pipeline usage."""
    
    print("=" * 60)
    print("Repository Embeddings Pipeline - Basic Usage")
    print("=" * 60)
    
    # Create pipeline with mini model (fast, good for testing)
    print("\n1. Creating pipeline...")
    pipeline = create_pipeline(
        model_key='mini',  # Options: 'mini', 'base', 'large', 'code'
        chunk_size=1000,
        chunk_overlap=200,
        index_type='flat'  # Options: 'flat', 'ivf', 'hnsw'
    )
    print("✓ Pipeline created")
    
    # Process a single file
    print("\n2. Processing a single file...")
    try:
        chunk_count = pipeline.process_file(
            file_path="README.md",
            content="""
            # Example Repository
            
            This is a sample repository for testing the embeddings pipeline.
            
            ## Features
            - Semantic search
            - Code understanding
            - Documentation retrieval
            
            ## Installation
            pip install -r requirements.txt
            
            ## Usage
            See examples directory for usage examples.
            """
        )
        print(f"✓ Processed file: {chunk_count} chunks created")
    except Exception as e:
        print(f"✗ Error processing file: {e}")
    
    # Search the repository
    print("\n3. Searching the repository...")
    results = pipeline.search(
        query="How do I install this?",
        k=3
    )
    
    print(f"\nFound {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n--- Result {i} (Score: {result.get('score', 0):.3f}) ---")
        print(f"File: {result['metadata'].get('file_path', 'N/A')}")
        print(f"Chunk: {result['metadata'].get('chunk_index', 'N/A')}")
        print(f"Text: {result['metadata'].get('text', '')[:200]}...")
    
    # Search with context
    print("\n4. Searching with context...")
    results_with_context = pipeline.search_with_context(
        query="What are the features?",
        k=2,
        context_window=1
    )
    
    print(f"\nFound {len(results_with_context)} results with context:")
    for i, result in enumerate(results_with_context, 1):
        print(f"\n--- Result {i} ---")
        print(f"Main text: {result['metadata'].get('text', '')[:150]}...")
        if 'context' in result:
            print(f"Context chunks: {len(result['context'])}")
    
    # Get statistics
    print("\n5. Pipeline statistics:")
    stats = pipeline.get_stats()
    print(f"Total vectors: {stats['vector_store']['total_vectors']}")
    print(f"Embedding dimension: {stats['embedding_dimension']}")
    print(f"Model: {stats['embedding_model']}")
    
    # Save pipeline
    print("\n6. Saving pipeline...")
    pipeline.save("./vector_store_data")
    print("✓ Pipeline saved to ./vector_store_data")
    
    # Load pipeline
    print("\n7. Loading pipeline...")
    loaded_pipeline = pipeline.load("./vector_store_data")
    print("✓ Pipeline loaded")
    
    # Verify loaded pipeline works
    print("\n8. Testing loaded pipeline...")
    test_results = loaded_pipeline.search("features", k=1)
    print(f"✓ Loaded pipeline works: {len(test_results)} results found")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Made with Bob
