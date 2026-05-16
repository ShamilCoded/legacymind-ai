"""
Advanced usage examples for the embeddings pipeline.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.embeddings import create_pipeline
from config import get_preset_config, PipelineConfig


def example_preset_configs():
    """Demonstrate using preset configurations."""
    print("=" * 60)
    print("Using Preset Configurations")
    print("=" * 60)
    
    # Available presets: 'fast', 'balanced', 'quality', 'code', 'large_scale'
    
    # Fast preset - for quick prototyping
    print("\n1. Fast preset (mini model):")
    config = get_preset_config('fast')
    print(f"   Model: {config['model']['name']}")
    print(f"   Chunk size: {config['chunking']['size']}")
    print(f"   Index type: {config['index']['type']}")
    
    # Balanced preset - recommended for production
    print("\n2. Balanced preset (base model):")
    config = get_preset_config('balanced')
    print(f"   Model: {config['model']['name']}")
    print(f"   Chunk size: {config['chunking']['size']}")
    
    # Code preset - optimized for code
    print("\n3. Code preset (code-specific model):")
    config = get_preset_config('code')
    print(f"   Model: {config['model']['name']}")
    print(f"   Description: Optimized for code repositories")


def example_custom_config():
    """Demonstrate creating custom configurations."""
    print("\n" + "=" * 60)
    print("Custom Configuration")
    print("=" * 60)
    
    # Create custom config
    config = PipelineConfig.create_custom_config(
        model_key='base',
        chunk_size=1500,
        chunk_overlap=300,
        index_type='ivf',
        storage_dir='./my_vector_store'
    )
    
    print("\nCustom configuration created:")
    print(f"Model: {config['model']['name']}")
    print(f"Chunk size: {config['chunking']['size']}")
    print(f"Chunk overlap: {config['chunking']['overlap']}")
    print(f"Index type: {config['index']['type']}")
    print(f"Storage: {config['storage']['directory']}")


def example_advanced_search():
    """Demonstrate advanced search features."""
    print("\n" + "=" * 60)
    print("Advanced Search Features")
    print("=" * 60)
    
    # Create pipeline
    pipeline = create_pipeline(model_key='mini')
    
    # Add sample content
    sample_files = {
        'auth.py': """
def authenticate_user(username, password):
    '''Authenticate user with JWT token'''
    token = generate_jwt_token(username)
    return token

def verify_token(token):
    '''Verify JWT token validity'''
    return jwt.decode(token)
""",
        'database.py': """
class DatabaseConnection:
    '''Handle database connections'''
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def connect(self):
        '''Establish database connection'''
        pass
""",
        'README.md': """
# Authentication System

This system provides JWT-based authentication.

## Features
- User authentication
- Token generation
- Token verification

## Installation
pip install jwt-auth
"""
    }
    
    print("\n1. Processing sample files...")
    for file_path, content in sample_files.items():
        chunks = pipeline.process_file(file_path, content)
        print(f"   {file_path}: {chunks} chunks")
    
    # Multi-query search
    print("\n2. Multi-query search:")
    from src.services.vector_store import SemanticRetriever
    retriever = pipeline.retriever
    
    results = retriever.multi_query_search(
        queries=[
            "JWT authentication",
            "token generation",
            "user verification"
        ],
        k=3,
        aggregation="max"
    )
    
    print(f"   Found {len(results)} results")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['metadata']['file_path']} "
              f"(Score: {result['score']:.3f})")
    
    # Search by type
    print("\n3. Search in Python files only:")
    results = retriever.search_by_type(
        query="database connection",
        content_type="python",
        k=2
    )
    
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['metadata']['file_path']} "
              f"(Score: {result['score']:.3f})")
    
    # Hybrid search
    print("\n4. Hybrid search (semantic + keyword):")
    results = retriever.hybrid_search(
        query="authentication",
        keyword_filter="JWT",
        k=3,
        semantic_weight=0.7
    )
    
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['metadata']['file_path']} "
              f"(Score: {result['score']:.3f}, "
              f"Semantic: {result.get('semantic_score', 0):.3f}, "
              f"Keyword: {result.get('keyword_score', 0):.3f})")


def example_filtering():
    """Demonstrate filtering and metadata usage."""
    print("\n" + "=" * 60)
    print("Filtering and Metadata")
    print("=" * 60)
    
    pipeline = create_pipeline(model_key='mini')
    
    # Add files with metadata
    files = {
        'frontend/app.js': 'React component code',
        'backend/api.py': 'FastAPI endpoint code',
        'docs/guide.md': 'User guide documentation'
    }
    
    print("\n1. Processing files with metadata...")
    for file_path, content in files.items():
        pipeline.process_file(file_path, content)
        print(f"   Processed: {file_path}")
    
    # Search with filters
    print("\n2. Search with file path filter:")
    results = pipeline.search(
        query="code",
        k=5,
        filters={'file_path': 'backend/api.py'}
    )
    
    print(f"   Found {len(results)} results in backend/api.py")
    
    # Search with score threshold
    print("\n3. Search with score threshold:")
    results = pipeline.search(
        query="documentation",
        k=5,
        score_threshold=0.3
    )
    
    print(f"   Found {len(results)} results with score >= 0.3")


def example_batch_processing():
    """Demonstrate batch processing capabilities."""
    print("\n" + "=" * 60)
    print("Batch Processing")
    print("=" * 60)
    
    pipeline = create_pipeline(model_key='mini')
    
    # Simulate processing multiple files
    print("\n1. Processing multiple files in batch...")
    
    files = [
        ('file1.txt', 'Content of file 1'),
        ('file2.txt', 'Content of file 2'),
        ('file3.txt', 'Content of file 3'),
        ('file4.txt', 'Content of file 4'),
        ('file5.txt', 'Content of file 5')
    ]
    
    total_chunks = 0
    for file_path, content in files:
        chunks = pipeline.process_file(file_path, content)
        total_chunks += chunks
    
    print(f"   Processed {len(files)} files")
    print(f"   Total chunks: {total_chunks}")
    
    # Batch search
    print("\n2. Performing batch searches...")
    queries = [
        "file content",
        "document text",
        "information"
    ]
    
    for query in queries:
        results = pipeline.search(query, k=2)
        print(f"   '{query}': {len(results)} results")


def main():
    """Run all advanced examples."""
    example_preset_configs()
    example_custom_config()
    example_advanced_search()
    example_filtering()
    example_batch_processing()
    
    print("\n" + "=" * 60)
    print("Advanced examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Made with Bob
