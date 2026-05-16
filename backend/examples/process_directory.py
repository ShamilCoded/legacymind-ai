"""
Example of processing an entire directory of files.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.embeddings import create_pipeline


def main():
    """Process a directory and perform searches."""
    
    print("=" * 60)
    print("Directory Processing Example")
    print("=" * 60)
    
    # Create pipeline
    print("\n1. Creating pipeline with base model...")
    pipeline = create_pipeline(
        model_key='base',  # Better quality than mini
        chunk_size=800,
        chunk_overlap=150,
        index_type='flat'
    )
    print("✓ Pipeline created")
    
    # Process directory
    print("\n2. Processing directory...")
    directory = "./src"  # Change to your directory
    
    results = pipeline.process_directory(
        directory=directory,
        file_patterns=['*.py', '*.md', '*.txt'],
        exclude_patterns=['*/node_modules/*', '*/.git/*', '*/__pycache__/*'],
        recursive=True
    )
    
    print(f"\n✓ Processed {len(results)} files")
    print("\nFiles processed:")
    for file_path, chunk_count in results.items():
        print(f"  - {file_path}: {chunk_count} chunks")
    
    # Get statistics
    print("\n3. Pipeline statistics:")
    stats = pipeline.get_stats()
    print(f"Total vectors: {stats['vector_store']['total_vectors']}")
    print(f"Embedding dimension: {stats['embedding_dimension']}")
    
    # Perform various searches
    print("\n4. Performing searches...")
    
    # Basic search
    print("\n--- Search: 'embedding service' ---")
    results = pipeline.search("embedding service", k=3)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['metadata'].get('file_path', 'N/A')} "
              f"(Score: {result.get('score', 0):.3f})")
    
    # Search by file type
    print("\n--- Search in Python files: 'class definition' ---")
    from src.services.vector_store import SemanticRetriever
    retriever = pipeline.retriever
    results = retriever.search_by_type("class definition", "python", k=3)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['metadata'].get('file_path', 'N/A')} "
              f"(Score: {result.get('score', 0):.3f})")
    
    # Multi-query search
    print("\n--- Multi-query search ---")
    queries = [
        "vector store implementation",
        "FAISS index creation",
        "similarity search"
    ]
    results = retriever.multi_query_search(queries, k=3, aggregation="max")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['metadata'].get('file_path', 'N/A')} "
              f"(Score: {result.get('score', 0):.3f})")
    
    # Save the processed data
    print("\n5. Saving pipeline...")
    save_dir = "./vector_store_directory"
    pipeline.save(save_dir)
    print(f"✓ Pipeline saved to {save_dir}")
    
    print("\n" + "=" * 60)
    print("Directory processing completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Made with Bob
