# Repository RAG Chatbot System

A comprehensive conversational AI system for repository Q&A using Retrieval-Augmented Generation (RAG), LangGraph orchestration, and semantic search.

## Features

### 🔍 Semantic Retrieval
- **FAISS Vector Store**: Efficient similarity search over code and documentation
- **Sentence Transformers**: High-quality embeddings for semantic understanding
- **Multi-query Search**: Aggregate results from multiple query variations
- **Hybrid Search**: Combine semantic and keyword-based search

### 💬 Conversational Memory
- **Session Management**: Maintain conversation context across interactions
- **Message History**: Track user and assistant messages with metadata
- **Context Windows**: Include relevant conversation history in responses
- **Persistent Storage**: Save and load conversation sessions

### 🧠 Code-Aware Responses
- **Language Detection**: Automatically identify programming languages
- **Code Element Extraction**: Parse functions, classes, imports, etc.
- **Pattern Recognition**: Identify design patterns and best practices
- **Context Generation**: Format code context for LLM understanding

### 🏗️ Architecture Explanations
- **Component Analysis**: Explain specific modules or components
- **Dependency Tracing**: Show what depends on what
- **High-level Overview**: Provide architectural summaries
- **Config File Analysis**: Understand project configuration

### 🔗 Dependency Reasoning
- **Import Tracking**: Extract and analyze import statements
- **Dependency Graphs**: Map relationships between files
- **Related Code**: Find code that uses or is used by target
- **Cross-reference**: Link related functionality

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                     │
├─────────────────────────────────────────────────────────────┤
│  Endpoints: /chat, /architecture, /dependencies, /search    │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼─────┐          ┌─────▼──────┐
    │ RAG      │          │ Session    │
    │ Chatbot  │          │ Manager    │
    └────┬─────┘          └────────────┘
         │
    ┌────▼──────────────────────────┐
    │      LangGraph Workflow       │
    ├───────────────────────────────┤
    │ 1. Retrieve (Vector Search)   │
    │ 2. Analyze (Code Analysis)    │
    │ 3. Generate (LLM Response)    │
    └────┬──────────────────────────┘
         │
    ┌────▼─────────────┐
    │  Vector Store    │
    │  (FAISS Index)   │
    └──────────────────┘
```

## Installation

### Prerequisites
- Python 3.9+
- OpenAI API key or Anthropic API key

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
# LLM Configuration
OPENAI_API_KEY=your_openai_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_key_here

LLM_PROVIDER=openai  # or anthropic
MODEL_NAME=gpt-4-turbo-preview  # or claude-3-opus-20240229

# Embedding Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Storage
VECTOR_STORE_PATH=./vector_store_data
```

## Quick Start

### 1. Index Your Repository

```python
from src.services.embeddings.pipeline import EmbeddingsPipeline
from src.services.embeddings.embedding_service import EmbeddingService
from src.services.vector_store.vector_store import VectorStore

# Initialize services
embedding_service = EmbeddingService(model_name="all-MiniLM-L6-v2")
vector_store = VectorStore(dimension=384)

# Create pipeline
pipeline = EmbeddingsPipeline(
    embedding_service=embedding_service,
    vector_store=vector_store
)

# Process repository
result = pipeline.process_directory(
    directory="/path/to/your/repo",
    file_patterns=["*.py", "*.js", "*.md"],
    exclude_patterns=["*/node_modules/*", "*/.git/*"]
)

# Save vector store
vector_store.save("./vector_store_data")
```

### 2. Start the API Server

```bash
# Using uvicorn
uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000

# Or using the startup script
python -m uvicorn src.api.app:app --reload
```

### 3. Use the API

```python
import requests

# Chat endpoint
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "query": "How does the authentication system work?",
        "session_id": "user-123",
        "max_results": 5
    }
)

print(response.json())
```

## API Endpoints

### POST /chat
Conversational Q&A with the repository.

**Request:**
```json
{
  "query": "How does the authentication work?",
  "session_id": "user-123",
  "max_results": 5,
  "include_sources": true
}
```

**Response:**
```json
{
  "response": "The authentication system uses JWT tokens...",
  "sources": [
    {
      "file_path": "src/auth/jwt.py",
      "score": 0.92,
      "preview": "def generate_token(user_id)...",
      "language": "python",
      "is_code": true
    }
  ],
  "suggestions": [
    "How are JWT tokens validated?",
    "Show me the user authentication flow"
  ],
  "session_id": "user-123",
  "metadata": {
    "num_retrieved": 5,
    "has_code_context": true
  }
}
```

### POST /architecture
Explain repository architecture.

**Request:**
```json
{
  "component": "authentication module",
  "session_id": "user-123"
}
```

### POST /dependencies
Trace dependencies for a file or function.

**Request:**
```json
{
  "target": "src/auth/jwt.py",
  "session_id": "user-123"
}
```

**Response:**
```json
{
  "response": "The jwt.py file depends on...",
  "dependencies": {
    "src/auth/jwt.py": ["jose", "datetime", "src.models.user"]
  },
  "sources": [...],
  "session_id": "user-123"
}
```

### POST /search
Search for code snippets.

**Request:**
```json
{
  "query": "function that validates email addresses",
  "k": 5,
  "file_type": "python"
}
```

### POST /index
Index a new repository.

**Request:**
```json
{
  "repository_path": "/path/to/repo",
  "file_patterns": ["*.py", "*.js"],
  "exclude_patterns": ["*/node_modules/*"],
  "chunk_size": 1000,
  "chunk_overlap": 200
}
```

### GET /sessions
List all active sessions.

### GET /sessions/{session_id}
Get conversation history for a session.

### DELETE /sessions/{session_id}
Delete a session.

### GET /health
Health check endpoint.

## Usage Examples

### Example 1: Basic Chat

```python
from src.services.chat.rag_chatbot import RAGChatbot
from src.services.embeddings.embedding_service import EmbeddingService
from src.services.vector_store.vector_store import VectorStore
from src.services.chat.memory import ConversationMemory

# Load services
embedding_service = EmbeddingService()
vector_store = VectorStore.load("./vector_store_data")

# Create chatbot
chatbot = RAGChatbot(
    embedding_service=embedding_service,
    vector_store=vector_store,
    llm_provider="openai",
    model_name="gpt-4-turbo-preview",
    api_key="your-api-key"
)

# Create memory
memory = ConversationMemory()

# Chat
response = chatbot.chat(
    query="What does the main function do?",
    memory=memory
)

print(response["response"])
print("Sources:", response["sources"])
print("Suggestions:", response["suggestions"])
```

### Example 2: Architecture Explanation

```python
# Explain overall architecture
response = chatbot.explain_architecture()
print(response["response"])

# Explain specific component
response = chatbot.explain_architecture(
    component="database layer"
)
print(response["response"])
```

### Example 3: Dependency Tracing

```python
# Trace dependencies
response = chatbot.trace_dependencies(
    file_or_function="src/api/routes.py"
)

print(response["response"])
print("Dependencies:", response["dependencies"])
```

### Example 4: Code Search

```python
# Find similar code
results = chatbot.find_similar_code(
    code_description="async function that handles HTTP requests",
    k=5
)

for result in results:
    print(f"File: {result['file_path']}")
    print(f"Score: {result['score']}")
    print(f"Code:\n{result['code']}\n")
```

### Example 5: Session Management

```python
from src.services.chat.memory import SessionManager

# Create session manager
session_manager = SessionManager()

# Create session
memory = session_manager.create_session("user-123")

# Chat with memory
response = chatbot.chat(
    query="How does authentication work?",
    memory=memory
)

# Continue conversation
response = chatbot.chat(
    query="Can you show me an example?",
    memory=memory
)

# Save session
session_manager.save_session("user-123")

# Load session later
memory = session_manager.load_session("user-123")
```

## Configuration

### Embedding Models

Available models in `EmbeddingService`:
- `all-MiniLM-L6-v2`: Fast, 384 dimensions (default)
- `all-mpnet-base-v2`: Balanced, 768 dimensions
- `all-distilroberta-v1`: High quality, 768 dimensions
- `flax-sentence-embeddings/st-codesearch-distilroberta-base`: Code-optimized

### LLM Providers

Supported providers:
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude 3 Opus, Claude 3 Sonnet

### Vector Store

FAISS index types:
- `flat`: Exact search (< 100K vectors)
- `ivf`: Fast approximate search (large datasets)
- `hnsw`: Hierarchical navigable small world

## Advanced Features

### Custom Code Analyzer

```python
from src.services.chat.code_analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()

# Analyze code chunk
analysis = analyzer.analyze_code_chunk({
    'text': code_text,
    'metadata': {'file_path': 'src/main.py'}
})

print(analysis['language'])
print(analysis['elements'])  # functions, classes, etc.
print(analysis['is_test'])
```

### Multi-Query Search

```python
from src.services.vector_store.retrieval import SemanticRetriever

retriever = SemanticRetriever(embedding_service, vector_store)

# Search with multiple query variations
results = retriever.multi_query_search(
    queries=[
        "authentication system",
        "user login flow",
        "JWT token generation"
    ],
    k=5,
    aggregation="max"
)
```

### Hybrid Search

```python
# Combine semantic and keyword search
results = retriever.hybrid_search(
    query="authentication",
    keyword_filter="JWT",
    k=5,
    semantic_weight=0.7
)
```

## Testing

Run tests:

```bash
pytest backend/tests/ -v
```

Run with coverage:

```bash
pytest backend/tests/ --cov=src --cov-report=html
```

## Performance Tips

1. **Use appropriate chunk sizes**: 800-1200 tokens for code, 1500-2000 for docs
2. **Enable GPU**: Use `faiss-gpu` for large datasets
3. **Batch processing**: Process multiple queries together
4. **Cache embeddings**: Reuse embeddings for repeated queries
5. **Index optimization**: Use IVF or HNSW for > 100K vectors

## Troubleshooting

### Issue: Slow retrieval
- Use IVF or HNSW index types
- Reduce number of results (k parameter)
- Enable GPU acceleration

### Issue: Poor response quality
- Increase chunk overlap for better context
- Use larger embedding model
- Adjust score threshold
- Include more context in prompts

### Issue: Out of memory
- Reduce batch size
- Use smaller embedding model
- Process files in batches
- Enable streaming responses

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Made with Bob

Built with ❤️ using FastAPI, LangGraph, and sentence-transformers.