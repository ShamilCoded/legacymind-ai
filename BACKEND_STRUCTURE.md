# LegacyMind AI - Backend Folder Structure

## Complete FastAPI + LangGraph Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                        # FastAPI application entry point
│   │
│   ├── api/                           # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # Main API router
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── health.py          # Health check
│   │   │   │   ├── repository.py      # Repository operations
│   │   │   │   ├── analysis.py        # Analysis endpoints
│   │   │   │   ├── chat.py            # Chat endpoints
│   │   │   │   └── embeddings.py      # Embeddings operations
│   │   │   └── dependencies.py        # Route dependencies
│   │   └── middleware.py              # Custom middleware
│   │
│   ├── core/                          # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py                  # Settings and environment
│   │   ├── security.py                # Security utilities
│   │   ├── logging.py                 # Logging configuration
│   │   └── exceptions.py              # Custom exceptions
│   │
│   ├── models/                        # Data models
│   │   ├── __init__.py
│   │   ├── repository.py              # Repository models
│   │   ├── analysis.py                # Analysis models
│   │   ├── chat.py                    # Chat models
│   │   ├── embeddings.py              # Embedding models
│   │   └── schemas.py                 # Pydantic schemas
│   │
│   ├── services/                      # Business logic
│   │   ├── __init__.py
│   │   ├── github/
│   │   │   ├── __init__.py
│   │   │   ├── cloner.py              # Repository cloning
│   │   │   ├── parser.py              # Code parsing
│   │   │   └── analyzer.py            # GitHub API integration
│   │   │
│   │   ├── analysis/
│   │   │   ├── __init__.py
│   │   │   ├── code_analyzer.py       # Code analysis
│   │   │   ├── dependency_analyzer.py # Dependency analysis
│   │   │   ├── risk_analyzer.py       # Risk assessment
│   │   │   ├── architecture_analyzer.py # Architecture detection
│   │   │   └── modernization.py       # Modernization suggestions
│   │   │
│   │   ├── embeddings/
│   │   │   ├── __init__.py
│   │   │   ├── generator.py           # Embedding generation
│   │   │   ├── chunker.py             # Code chunking
│   │   │   └── indexer.py             # FAISS indexing
│   │   │
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── langgraph_workflow.py  # LangGraph workflow
│   │   │   ├── agents.py              # AI agents
│   │   │   ├── prompts.py             # Prompt templates
│   │   │   └── chains.py              # LangChain chains
│   │   │
│   │   └── vector_store/
│   │       ├── __init__.py
│   │       ├── faiss_store.py         # FAISS operations
│   │       └── retriever.py           # Vector retrieval
│   │
│   ├── utils/                         # Utility functions
│   │   ├── __init__.py
│   │   ├── file_utils.py              # File operations
│   │   ├── git_utils.py               # Git operations
│   │   ├── text_utils.py              # Text processing
│   │   └── validators.py              # Input validators
│   │
│   ├── db/                            # Database (optional)
│   │   ├── __init__.py
│   │   ├── session.py                 # DB session
│   │   └── models.py                  # SQLAlchemy models
│   │
│   └── storage/                       # File storage
│       ├── repositories/              # Cloned repos
│       ├── embeddings/                # Stored embeddings
│       └── cache/                     # Cache files
│
├── tests/                             # Test suite
│   ├── __init__.py
│   ├── conftest.py                    # Pytest fixtures
│   ├── unit/
│   │   ├── test_github_cloner.py
│   │   ├── test_code_analyzer.py
│   │   └── test_embeddings.py
│   └── integration/
│       ├── test_api_endpoints.py
│       └── test_workflow.py
│
├── scripts/                           # Utility scripts
│   ├── setup_env.py                   # Environment setup
│   ├── download_models.py             # Download ML models
│   └── migrate_db.py                  # Database migrations
│
├── .env                               # Environment variables
├── .env.example                       # Example env file
├── .gitignore                         # Git ignore
├── requirements.txt                   # Python dependencies
├── requirements-dev.txt               # Dev dependencies
├── Dockerfile                         # Docker configuration
├── docker-compose.yml                 # Docker Compose
├── render.yaml                        # Render deployment config
├── pyproject.toml                     # Python project config
└── README.md                          # Documentation
```

## Folder Explanations

### 📁 `app/`
**Purpose**: Main application package

#### `main.py`
**Purpose**: FastAPI application entry point
- Creates FastAPI app instance
- Configures CORS
- Includes routers
- Sets up middleware
- Initializes services

### 📁 `app/api/`
**Purpose**: API layer (routes and endpoints)

#### `v1/`
**Purpose**: API version 1 (allows versioning)
- `router.py`: Aggregates all endpoint routers
- `endpoints/`: Individual endpoint modules
  - `health.py`: Health check endpoint
  - `repository.py`: Repository CRUD operations
  - `analysis.py`: Analysis endpoints
  - `chat.py`: Chat with codebase
  - `embeddings.py`: Embedding operations
- `dependencies.py`: Dependency injection (auth, DB sessions)

#### `middleware.py`
**Purpose**: Custom middleware
- Request logging
- Error handling
- Rate limiting
- CORS configuration

### 📁 `app/core/`
**Purpose**: Core application configuration

#### Files
- `config.py`: Settings class (Pydantic BaseSettings)
  - Environment variables
  - API keys
  - Database URLs
  - Model configurations
- `security.py`: Security utilities
  - API key validation
  - Token generation
  - Password hashing
- `logging.py`: Logging setup
  - Log formatters
  - Log handlers
  - Log levels
- `exceptions.py`: Custom exceptions
  - `RepositoryNotFoundError`
  - `AnalysisFailedError`
  - `EmbeddingError`

### 📁 `app/models/`
**Purpose**: Data models and schemas

#### Files
- `repository.py`: Repository data models
  ```python
  class Repository:
      id, url, name, owner, language, stars, etc.
  ```
- `analysis.py`: Analysis result models
  ```python
  class AnalysisResult:
      summary, architecture, dependencies, risks, etc.
  ```
- `chat.py`: Chat message models
  ```python
  class ChatMessage:
      role, content, timestamp, etc.
  ```
- `embeddings.py`: Embedding models
  ```python
  class CodeEmbedding:
      file_path, chunk, embedding_vector, etc.
  ```
- `schemas.py`: Pydantic schemas for API validation
  - Request schemas
  - Response schemas
  - Validation rules

### 📁 `app/services/`
**Purpose**: Business logic layer (core functionality)

#### `github/`
**Purpose**: GitHub integration services
- `cloner.py`: Clone repositories
  - Git clone operations
  - Repository validation
  - Cleanup old repos
- `parser.py`: Parse code files
  - Language detection
  - AST parsing
  - Extract functions/classes
- `analyzer.py`: GitHub API integration
  - Fetch repo metadata
  - Get commit history
  - Analyze contributors

#### `analysis/`
**Purpose**: Code analysis services
- `code_analyzer.py`: Analyze code quality
  - Complexity metrics
  - Code smells
  - Best practices
- `dependency_analyzer.py`: Analyze dependencies
  - Parse package files (package.json, requirements.txt)
  - Detect outdated packages
  - Security vulnerabilities
- `risk_analyzer.py`: Risk assessment
  - Technical debt
  - Security risks
  - Maintenance risks
- `architecture_analyzer.py`: Detect architecture
  - Identify patterns (MVC, microservices)
  - Component relationships
  - Data flow
- `modernization.py`: Modernization suggestions
  - Framework upgrades
  - Best practices
  - Refactoring opportunities

#### `embeddings/`
**Purpose**: Embedding generation and management
- `generator.py`: Generate embeddings
  - Load sentence-transformers model
  - Batch processing
  - Embedding normalization
- `chunker.py`: Chunk code files
  - Smart chunking (by function/class)
  - Overlap strategy
  - Metadata extraction
- `indexer.py`: FAISS indexing
  - Create FAISS index
  - Add embeddings
  - Save/load index

#### `ai/`
**Purpose**: AI and LangGraph workflows
- `langgraph_workflow.py`: LangGraph workflow
  - Define workflow graph
  - State management
  - Node execution
- `agents.py`: AI agents
  - Summarization agent
  - Analysis agent
  - Chat agent
- `prompts.py`: Prompt templates
  - System prompts
  - User prompts
  - Few-shot examples
- `chains.py`: LangChain chains
  - RAG chain
  - Summarization chain
  - Q&A chain

#### `vector_store/`
**Purpose**: Vector database operations
- `faiss_store.py`: FAISS operations
  - Initialize FAISS index
  - Add vectors
  - Search vectors
- `retriever.py`: Vector retrieval
  - Semantic search
  - Similarity scoring
  - Result ranking

### 📁 `app/utils/`
**Purpose**: Utility functions

#### Files
- `file_utils.py`: File operations
  - Read/write files
  - Directory traversal
  - File type detection
- `git_utils.py`: Git operations
  - Git commands wrapper
  - Branch detection
  - Commit parsing
- `text_utils.py`: Text processing
  - Tokenization
  - Cleaning
  - Formatting
- `validators.py`: Input validators
  - URL validation
  - GitHub URL parsing
  - Input sanitization

### 📁 `app/db/` (Optional)
**Purpose**: Database layer (if using persistent storage)
- `session.py`: Database session management
- `models.py`: SQLAlchemy ORM models

### 📁 `app/storage/`
**Purpose**: File storage directories
- `repositories/`: Cloned repositories
- `embeddings/`: Saved FAISS indices
- `cache/`: Temporary cache files

### 📁 `tests/`
**Purpose**: Test suite

#### Structure
- `conftest.py`: Pytest fixtures and configuration
- `unit/`: Unit tests (isolated functions)
- `integration/`: Integration tests (API endpoints)

### 📁 `scripts/`
**Purpose**: Utility scripts
- `setup_env.py`: Set up environment
- `download_models.py`: Download ML models
- `migrate_db.py`: Database migrations

## Naming Conventions

### Files
- **Modules**: `snake_case.py` (e.g., `code_analyzer.py`)
- **Classes**: `PascalCase` (e.g., `CodeAnalyzer`)
- **Functions**: `snake_case` (e.g., `analyze_code`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE`)

### Modules
- **Services**: Noun-based (e.g., `cloner.py`, `analyzer.py`)
- **Utils**: Action-based (e.g., `file_utils.py`)
- **Models**: Entity-based (e.g., `repository.py`)

### API Endpoints
- **RESTful**: `/api/v1/repositories`, `/api/v1/analysis`
- **Actions**: POST `/api/v1/repositories/clone`
- **Resources**: GET `/api/v1/repositories/{id}`

## Key Architecture Decisions

### 1. **Layered Architecture**
- API Layer → Service Layer → Data Layer
- Clear separation of concerns

### 2. **Dependency Injection**
- Services injected via FastAPI dependencies
- Easy testing and mocking

### 3. **Async/Await**
- All I/O operations are async
- Better performance for concurrent requests

### 4. **Pydantic Models**
- Type validation
- Automatic API documentation
- Serialization/deserialization

### 5. **Service-Oriented**
- Each service has single responsibility
- Reusable across endpoints

### 6. **Vector Store Abstraction**
- FAISS implementation
- Easy to swap for other vector DBs

### 7. **LangGraph Workflow**
- Stateful AI workflow
- Modular agent design

## API Endpoint Structure

```
POST   /api/v1/repositories/clone          # Clone repository
GET    /api/v1/repositories/{id}           # Get repository details
POST   /api/v1/analysis/summarize          # Generate summary
POST   /api/v1/analysis/architecture       # Analyze architecture
POST   /api/v1/analysis/dependencies       # Analyze dependencies
POST   /api/v1/analysis/risks              # Analyze risks
POST   /api/v1/analysis/modernization      # Get modernization suggestions
POST   /api/v1/chat                        # Chat with codebase
GET    /api/v1/embeddings/{repo_id}        # Get embeddings status
POST   /api/v1/embeddings/generate         # Generate embeddings
GET    /health                             # Health check
```

## Environment Variables

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# OpenAI/LLM
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4

# GitHub
GITHUB_TOKEN=ghp_...

# Storage
STORAGE_PATH=./app/storage
MAX_REPO_SIZE_MB=500

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
FAISS_INDEX_TYPE=IndexFlatL2

# Database (optional)
DATABASE_URL=postgresql://user:pass@localhost/legacymind

# CORS
CORS_ORIGINS=http://localhost:3000,https://legacymind.vercel.app

# Logging
LOG_LEVEL=INFO
```

## Dependencies (requirements.txt)

```txt
# FastAPI
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
pydantic-settings==2.1.0

# AI/ML
langchain==0.1.0
langgraph==0.0.20
openai==1.10.0
sentence-transformers==2.3.1
faiss-cpu==1.7.4

# GitHub
gitpython==3.1.41
PyGithub==2.1.1

# Code Analysis
tree-sitter==0.20.4
radon==6.0.1
pylint==3.0.3

# Utilities
python-dotenv==1.0.0
httpx==0.26.0
aiofiles==23.2.1
python-multipart==0.0.6

# Database (optional)
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9
```

## Next Steps

1. Initialize FastAPI project
2. Set up folder structure
3. Install dependencies
4. Configure environment variables
5. Implement core services
6. Create API endpoints
7. Set up LangGraph workflow
8. Add tests
9. Configure Render deployment

This structure supports:
- ✅ Scalability (modular services)
- ✅ Maintainability (clear separation)
- ✅ Testability (dependency injection)
- ✅ Performance (async operations)
- ✅ Production-ready (error handling, logging)