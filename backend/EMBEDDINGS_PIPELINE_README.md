# Repository Embeddings Pipeline

A comprehensive, modular pipeline for creating semantic embeddings of repository files using sentence-transformers and FAISS for efficient similarity search.

## Features

- ✅ **Intelligent Chunking**: Automatically chunks large files while preserving context
- ✅ **Multiple File Types**: Supports code (Python, JS, TS, etc.), Markdown, and text files
- ✅ **Semantic Search**: Fast similarity search using FAISS vector store
- ✅ **Context-Aware Retrieval**: Retrieve results with surrounding chunks for better context
- ✅ **Flexible Models**: Choose from multiple sentence-transformer models
- ✅ **Persistent Storage**: Save and load vector stores for reuse
- ✅ **Modular Design**: Reusable components for custom workflows

## Architecture

```
backend/
├── src/
│   ├── services/
│   │   ├── embeddings/
│   │   │   ├── embedding_service.py    # Sentence-transformers wrapper
│   │   │   └── pipeline.py             # Main pipeline orchestrator
│   │   └── vector_store/
│   │       ├── vector_store.py         # FAISS vector store
│   │       └── retrieval.py            # Semantic search functions
│   └── utils/
│       └── chunking.py                 # Text chunking utilities
├── examples/
│   ├── basic_usage.py                  # Basic usage example
│   └── process_directory.py            # Directory processing example
└── tests/
    ├── test_chunking.py                # Chunking tests
    └── test_pipeline.py                # Pipeline integration tests
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# For GPU support (optional)
pip install faiss-gpu
```

### Requirements

- Python 3.8+
- sentence-transformers >= 2.2.0
- faiss-cpu >= 1.7.4 (or faiss-gpu for GPU support)
- numpy >= 1.24.0
- torch >= 2.0.0

## Quick Start

### Basic Usage

```python
from src.services.embeddings import create_pipeline

# Create pipeline
pipeline = create_pipeline(
    model_key='mini',      # Options: 'mini', 'base', 'large', 'code'
    chunk_size=1000,       # Characters per chunk
    chunk_overlap=200,     # Overlap between chunks
    index_type='flat'      # FAISS index type
)

# Process a file
chunk_count = pipeline.process_file(
    file_path="README.md",
    content="Your content here..."
)

# Search
results = pipeline.search(
    query="How do I install this?",
    k=5  # Number of results
)

# Display results
for result in results:
    print(f"Score: {result['score']:.3f}")
    print(f"File: {result['metadata']['file_path']}")
    print(f"Text: {result['metadata']['text'][:200]}...")
```

### Process Entire Directory

```python
# Process all files in a directory
results = pipeline.process_directory(
    directory="./src",
    file_patterns=['*.py', '*.md', '*.txt'],
    exclude_patterns=['*/node_modules/*', '*/.git/*'],
    recursive=True
)

print(f"Processed {len(results)} files")
```

### Save and Load Pipeline

```python
# Save pipeline state
pipeline.save("./vector_store_data")

# Load pipeline later
from src.services.embeddings import EmbeddingsPipeline
loaded_pipeline = EmbeddingsPipeline.load("./vector_store_data")

# Use loaded pipeline
results = loaded_pipeline.search("your query", k=5)
```

## Advanced Usage

### Search with Context

Get surrounding chunks for better context:

```python
results = pipeline.search_with_context(
    query="authentication implementation",
    k=5,
    context_window=1  # Include 1 chunk before/after
)

for result in results:
    print(f"Main: {result['metadata']['text'][:100]}...")
    if 'context' in result:
        for ctx in result['context']:
            print(f"  Context: {ctx['text'][:100]}...")
```

### Multi-Query Search

Search with multiple related queries:

```python
from src.services.vector_store import SemanticRetriever

retriever = pipeline.retriever
results = retriever.multi_query_search(
    queries=[
        "vector store implementation",
        "FAISS index creation",
        "similarity search"
    ],
    k=5,
    aggregation="max"  # Options: 'max', 'mean', 'sum'
)
```

### Search by File Type

```python
# Search only in Python files
results = retriever.search_by_type(
    query="class definition",
    content_type="python",
    k=5
)

# Search only in Markdown files
results = retriever.search_by_type(
    query="installation guide",
    content_type="markdown",
    k=5
)
```

### Hybrid Search

Combine semantic and keyword search:

```python
results = retriever.hybrid_search(
    query="authentication",
    keyword_filter="JWT",
    k=5,
    semantic_weight=0.7  # 70% semantic, 30% keyword
)
```

### Find Similar Chunks

```python
results = retriever.get_similar_chunks(
    chunk_text="Your reference text here",
    k=5,
    exclude_same_file=True
)
```

## Model Options

Choose the right model for your use case:

| Model Key | Model Name | Dimension | Speed | Quality | Use Case |
|-----------|------------|-----------|-------|---------|----------|
| `mini` | all-MiniLM-L6-v2 | 384 | ⚡⚡⚡ | ⭐⭐ | Fast prototyping |
| `base` | all-mpnet-base-v2 | 768 | ⚡⚡ | ⭐⭐⭐ | Balanced (recommended) |
| `large` | all-distilroberta-v1 | 768 | ⚡ | ⭐⭐⭐⭐ | Best quality |
| `code` | st-codesearch-distilroberta-base | 768 | ⚡⚡ | ⭐⭐⭐ | Code-specific |
| `multilingual` | paraphrase-multilingual-MiniLM-L12-v2 | 384 | ⚡⚡ | ⭐⭐⭐ | Multiple languages |

```python
# Use different models
pipeline_mini = create_pipeline(model_key='mini')    # Fast
pipeline_base = create_pipeline(model_key='base')    # Balanced
pipeline_large = create_pipeline(model_key='large')  # Best quality
pipeline_code = create_pipeline(model_key='code')    # For code
```

## FAISS Index Types

Choose the right index for your scale:

| Index Type | Speed | Memory | Accuracy | Best For |
|------------|-------|--------|----------|----------|
| `flat` | ⚡ | High | 100% | < 100K vectors |
| `ivf` | ⚡⚡⚡ | Medium | ~95% | 100K - 1M vectors |
| `hnsw` | ⚡⚡ | High | ~99% | Fast approximate search |

```python
# Flat index - exact search (default)
pipeline = create_pipeline(index_type='flat')

# IVF index - faster for large datasets
pipeline = create_pipeline(index_type='ivf')

# HNSW index - hierarchical navigable small world
pipeline = create_pipeline(index_type='hnsw')
```

## Chunking Strategies

### Text Chunking

```python
from src.utils.chunking import TextChunker

chunker = TextChunker(
    chunk_size=1000,      # Max characters per chunk
    chunk_overlap=200,    # Overlap for context
    separator="\n\n"      # Split on paragraphs
)

chunks = chunker.chunk_text(text, metadata={'source': 'doc.txt'})
```

### Code Chunking

```python
chunks = chunker.chunk_code(
    code=python_code,
    language='python',
    metadata={'file': 'app.py'}
)
```

### Markdown Chunking

```python
chunks = chunker.chunk_markdown(
    markdown=md_content,
    metadata={'file': 'README.md'}
)
```

## API Reference

### EmbeddingsPipeline

Main pipeline class for processing and searching.

**Methods:**

- `process_file(file_path, content, file_type)` - Process a single file
- `process_directory(directory, file_patterns, exclude_patterns, recursive)` - Process directory
- `search(query, k, **kwargs)` - Semantic search
- `search_with_context(query, k, context_window)` - Search with context
- `save(directory)` - Save pipeline state
- `load(directory)` - Load pipeline state (class method)
- `get_stats()` - Get pipeline statistics

### EmbeddingService

Service for generating embeddings.

**Methods:**

- `encode_text(text, normalize, show_progress)` - Encode text to embeddings
- `encode_chunks(chunks, text_key, normalize, show_progress)` - Encode multiple chunks
- `encode_query(query, normalize)` - Encode search query
- `compute_similarity(embedding1, embedding2)` - Compute cosine similarity
- `get_embedding_dimension()` - Get embedding dimension

### VectorStore

FAISS-based vector store.

**Methods:**

- `add_vectors(embeddings, metadata, ids)` - Add vectors to store
- `search(query_embedding, k, return_scores)` - Search for similar vectors
- `search_batch(query_embeddings, k, return_scores)` - Batch search
- `get_by_id(vec_id)` - Get metadata by ID
- `delete_by_id(vec_id)` - Delete vector by ID
- `save(directory)` - Save to disk
- `load(directory)` - Load from disk (class method)
- `get_stats()` - Get store statistics

### SemanticRetriever

Advanced retrieval functions.

**Methods:**

- `search(query, k, filters, score_threshold)` - Basic search
- `search_with_context(query, k, context_window, filters)` - Search with context
- `search_by_file(query, file_path, k)` - Search within file
- `search_by_type(query, content_type, k)` - Search by content type
- `multi_query_search(queries, k, aggregation)` - Multi-query search
- `hybrid_search(query, keyword_filter, k, semantic_weight)` - Hybrid search
- `get_similar_chunks(chunk_text, k, exclude_same_file, file_path)` - Find similar chunks

## Performance Tips

1. **Choose the right model**: Use `mini` for prototyping, `base` for production
2. **Optimize chunk size**: Larger chunks (1000-2000) for documents, smaller (500-800) for code
3. **Use appropriate index**: `flat` for < 100K vectors, `ivf` for larger datasets
4. **Batch processing**: Process multiple files together for better efficiency
5. **GPU acceleration**: Use `faiss-gpu` and `device='cuda'` for large datasets

## Examples

See the `examples/` directory for complete examples:

- `basic_usage.py` - Basic pipeline usage
- `process_directory.py` - Process entire directories

Run examples:

```bash
cd backend
python examples/basic_usage.py
python examples/process_directory.py
```

## Testing

Run tests:

```bash
cd backend
pytest tests/ -v
```

Run specific test file:

```bash
pytest tests/test_chunking.py -v
pytest tests/test_pipeline.py -v
```

## Troubleshooting

### Out of Memory

- Use smaller chunk sizes
- Process files in batches
- Use `ivf` index instead of `flat`
- Consider using CPU instead of GPU for very large datasets

### Slow Search

- Use `ivf` or `hnsw` index for large datasets
- Reduce `k` (number of results)
- Use smaller embedding model (`mini` instead of `large`)

### Poor Search Quality

- Use larger embedding model (`base` or `large`)
- Increase chunk overlap for better context
- Adjust chunk size based on content type
- Use `code` model for code search

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.