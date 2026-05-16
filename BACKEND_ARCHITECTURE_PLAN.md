# LegacyMind AI - Backend Architecture Plan

## 🎯 Architecture Overview

**Approach**: Balanced production-ready setup optimized for hackathon deployment
- **Storage**: File-system based (FAISS + JSON)
- **Authentication**: API key authentication
- **Background Tasks**: FastAPI BackgroundTasks
- **Deployment**: Render platform

## 📁 Complete Folder Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                           # FastAPI application entry
│   │
│   ├── api/                              # API Layer
│   │   ├── __init__.py
│   │   ├── deps.py                       # Dependency injection
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py                 # Main v1 router
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── health.py             # Health check
│   │           ├── repositories.py       # Repository operations
│   │           ├── analysis.py           # Analysis endpoints
│   │           ├── chat.py               # Chat with codebase
│   │           └── embeddings.py         # Embedding operations
│   │
│   ├── core/                             # Core Configuration
│   │   ├── __init__.py
│   │   ├── config.py                     # Settings (Pydantic)
│   │   ├── security.py                   # API key validation
│   │   ├── logging.py                    # Logging setup
│   │   └── exceptions.py                 # Custom exceptions
│   │
│   ├── models/                           # Data Models
│   │   ├── __init__.py
│   │   ├── repository.py                 # Repository models
│   │   ├── analysis.py                   # Analysis result models
│   │   ├── chat.py                       # Chat models
│   │   └── schemas.py                    # Pydantic schemas
│   │
│   ├── services/                         # Business Logic Layer
│   │   ├── __init__.py
│   │   │
│   │   ├── github/                       # GitHub Integration
│   │   │   ├── __init__.py
│   │   │   ├── cloner.py                 # Clone repositories
│   │   │   ├── parser.py                 # Parse code files
│   │   │   └── metadata.py               # Extract repo metadata
│   │   │
│   │   ├── analysis/                     # Code Analysis
│   │   │   ├── __init__.py
│   │   │   ├── code_analyzer.py          # Code quality analysis
│   │   │   ├── dependency_analyzer.py    # Dependency analysis
│   │   │   ├── risk_analyzer.py          # Risk assessment
│   │   │   ├── architecture_detector.py  # Architecture patterns
│   │   │   └── modernization.py          # Modernization suggestions
│   │   │
│   │   ├── embeddings/                   # Embedding Generation
│   │   │   ├── __init__.py
│   │   │   ├── chunker.py                # Code chunking
│   │   │   ├── generator.py              # Generate embeddings
│   │   │   └── indexer.py                # FAISS indexing
│   │   │
│   │   ├── ai/                           # AI Services
│   │   │   ├── __init__.py
│   │   │   ├── workflow.py               # LangGraph workflow
│   │   │   ├── agents.py                 # AI agents
│   │   │   ├── prompts.py                # Prompt templates
│   │   │   └── rag_chain.py              # RAG implementation
│   │   │
│   │   └── vector_store/                 # Vector Storage
│   │       ├── __init__.py
│   │       ├── faiss_manager.py          # FAISS operations
│   │       └── retriever.py              # Vector retrieval
│   │
│   ├── utils/                            # Utilities
│   │   ├── __init__.py
│   │   ├── file_utils.py                 # File operations
│   │   ├── git_utils.py                  # Git utilities
│   │   ├── text_utils.py                 # Text processing
│   │   └── validators.py                 # Input validation
│   │
│   └── storage/                          # File Storage
│       ├── repositories/                 # Cloned repos
│       ├── embeddings/                   # FAISS indices
│       ├── analysis/                     # Analysis results (JSON)
│       └── cache/                        # Temporary cache
│
├── tests/                                # Test Suite
│   ├── __init__.py
│   ├── conftest.py                       # Pytest fixtures
│   ├── test_api/
│   │   ├── test_health.py
│   │   ├── test_repositories.py
│   │   └── test_analysis.py
│   └── test_services/
│       ├── test_cloner.py
│       ├── test_embeddings.py
│       └── test_rag.py
│
├── scripts/                              # Utility Scripts
│   ├── setup_storage.py                  # Create storage dirs
│   ├── download_models.py                # Download ML models
│   └── cleanup.py                        # Cleanup old data
│
├── .env                                  # Environment variables
├── .env.example                          # Example env file
├── .gitignore                            # Git ignore
├── requirements.txt                      # Python dependencies
├── requirements-dev.txt                  # Dev dependencies
├── Dockerfile                            # Docker config
├── render.yaml                           # Render deployment
├── pyproject.toml                        # Python project config
└── README.md                             # Backend documentation
```

## 🔌 API Endpoints Specification

### Health & Status
```
GET  /health                              # Health check
GET  /api/v1/status                       # API status
```

### Repository Operations
```
POST   /api/v1/repositories/clone         # Clone repository
  Body: { "url": "https://github.com/user/repo" }
  Response: { "repo_id": "uuid", "status": "cloning" }

GET    /api/v1/repositories/{repo_id}     # Get repository details
  Response: { "id", "url", "name", "status", "metadata" }

GET    /api/v1/repositories               # List repositories
  Query: ?limit=10&offset=0
  Response: { "repositories": [...], "total": 100 }

DELETE /api/v1/repositories/{repo_id}     # Delete repository
  Response: { "message": "Repository deleted" }
```

### Analysis Operations
```
POST   /api/v1/analysis/summarize         # Generate AI summary
  Body: { "repo_id": "uuid" }
  Response: { "summary": "...", "key_points": [...] }

POST   /api/v1/analysis/architecture      # Analyze architecture
  Body: { "repo_id": "uuid" }
  Response: { "pattern": "MVC", "components": [...], "graph": {...} }

POST   /api/v1/analysis/dependencies      # Analyze dependencies
  Body: { "repo_id": "uuid" }
  Response: { "dependencies": [...], "outdated": [...], "vulnerabilities": [...] }

POST   /api/v1/analysis/risks             # Assess risks
  Body: { "repo_id": "uuid" }
  Response: { "risk_score": 7.5, "risks": [...], "recommendations": [...] }

POST   /api/v1/analysis/modernization     # Get modernization suggestions
  Body: { "repo_id": "uuid" }
  Response: { "suggestions": [...], "priority": "high" }

GET    /api/v1/analysis/{repo_id}/full    # Get complete analysis
  Response: { "summary", "architecture", "dependencies", "risks", "modernization" }
```

### Chat Operations
```
POST   /api/v1/chat                       # Chat with codebase
  Body: { "repo_id": "uuid", "message": "How does auth work?", "history": [...] }
  Response: { "response": "...", "sources": [...], "confidence": 0.95 }

GET    /api/v1/chat/{repo_id}/history     # Get chat history
  Response: { "messages": [...] }

DELETE /api/v1/chat/{repo_id}/history     # Clear chat history
  Response: { "message": "History cleared" }
```

### Embedding Operations
```
POST   /api/v1/embeddings/generate        # Generate embeddings
  Body: { "repo_id": "uuid" }
  Response: { "status": "processing", "total_chunks": 1500 }

GET    /api/v1/embeddings/{repo_id}/status # Get embedding status
  Response: { "status": "completed", "chunks": 1500, "index_size": "25MB" }

POST   /api/v1/embeddings/search          # Search embeddings
  Body: { "repo_id": "uuid", "query": "authentication logic", "k": 5 }
  Response: { "results": [...] }
```

## 🏗️ Service Layer Architecture

### 1. GitHub Service (`services/github/`)

#### Cloner (`cloner.py`)
```python
class RepositoryCloner:
    """Clone and manage GitHub repositories"""
    
    async def clone_repository(url: str) -> str:
        """Clone repository and return local path"""
        - Validate GitHub URL
        - Generate unique repo ID
        - Clone using GitPython
        - Apply size limits (500MB)
        - Return repo_id and path
    
    async def cleanup_old_repos(days: int = 7):
        """Remove repositories older than N days"""
    
    def get_repo_size(path: str) -> int:
        """Calculate repository size"""
```

#### Parser (`parser.py`)
```python
class CodeParser:
    """Parse and analyze code files"""
    
    def parse_repository(repo_path: str) -> dict:
        """Parse all code files in repository"""
        - Traverse directory tree
        - Filter by language (.py, .js, .java, etc.)
        - Extract file metadata
        - Count lines of code
        - Identify main languages
    
    def extract_structure(file_path: str) -> dict:
        """Extract code structure (functions, classes)"""
        - Use AST parsing
        - Extract imports
        - Extract function/class definitions
        - Extract docstrings
    
    def parse_dependencies(repo_path: str) -> dict:
        """Parse dependency files"""
        - package.json (Node.js)
        - requirements.txt (Python)
        - pom.xml (Java)
        - Gemfile (Ruby)
```

#### Metadata Extractor (`metadata.py`)
```python
class MetadataExtractor:
    """Extract repository metadata"""
    
    async def get_github_metadata(url: str) -> dict:
        """Fetch metadata from GitHub API"""
        - Stars, forks, watchers
        - Primary language
        - Last commit date
        - Contributors count
        - License information
    
    def extract_local_metadata(repo_path: str) -> dict:
        """Extract metadata from local repo"""
        - File count
        - Total lines of code
        - Language distribution
        - Directory structure
```

### 2. Analysis Service (`services/analysis/`)

#### Code Analyzer (`code_analyzer.py`)
```python
class CodeAnalyzer:
    """Analyze code quality and complexity"""
    
    def analyze_complexity(file_path: str) -> dict:
        """Calculate cyclomatic complexity"""
        - Use radon library
        - Complexity per function
        - Average complexity
        - Hotspots identification
    
    def detect_code_smells(repo_path: str) -> list:
        """Detect common code smells"""
        - Long functions
        - Duplicate code
        - Large classes
        - Deep nesting
    
    def calculate_metrics(repo_path: str) -> dict:
        """Calculate code metrics"""
        - Lines of code
        - Comment ratio
        - Test coverage estimate
        - Maintainability index
```

#### Dependency Analyzer (`dependency_analyzer.py`)
```python
class DependencyAnalyzer:
    """Analyze project dependencies"""
    
    def parse_dependencies(repo_path: str) -> list:
        """Parse all dependency files"""
        - Identify package managers
        - Extract dependencies
        - Categorize (prod/dev)
    
    async def check_outdated(dependencies: list) -> list:
        """Check for outdated packages"""
        - Query package registries
        - Compare versions
        - Identify major updates
    
    async def check_vulnerabilities(dependencies: list) -> list:
        """Check for security vulnerabilities"""
        - Query vulnerability databases
        - Severity scoring
        - Remediation suggestions
```

#### Risk Analyzer (`risk_analyzer.py`)
```python
class RiskAnalyzer:
    """Assess technical risks"""
    
    def calculate_risk_score(analysis_data: dict) -> float:
        """Calculate overall risk score (0-10)"""
        - Complexity score
        - Dependency health
        - Code quality
        - Security issues
    
    def identify_risks(repo_path: str) -> list:
        """Identify specific risks"""
        - Technical debt
        - Security vulnerabilities
        - Outdated dependencies
        - Maintenance complexity
    
    def generate_recommendations(risks: list) -> list:
        """Generate risk mitigation recommendations"""
```

#### Architecture Detector (`architecture_detector.py`)
```python
class ArchitectureDetector:
    """Detect architecture patterns"""
    
    def detect_pattern(repo_path: str) -> str:
        """Detect primary architecture pattern"""
        - MVC (Model-View-Controller)
        - Microservices
        - Monolith
        - Layered architecture
        - Event-driven
    
    def build_component_graph(repo_path: str) -> dict:
        """Build component dependency graph"""
        - Identify components
        - Map dependencies
        - Calculate coupling
        - Generate graph data for React Flow
    
    def analyze_data_flow(repo_path: str) -> dict:
        """Analyze data flow patterns"""
```

#### Modernization Advisor (`modernization.py`)
```python
class ModernizationAdvisor:
    """Generate modernization suggestions"""
    
    def suggest_upgrades(dependencies: list) -> list:
        """Suggest framework/library upgrades"""
        - Identify outdated frameworks
        - Suggest modern alternatives
        - Migration complexity estimate
    
    def suggest_refactoring(analysis: dict) -> list:
        """Suggest code refactoring"""
        - Based on code smells
        - Based on complexity
        - Best practices
    
    def suggest_architecture_improvements(pattern: str) -> list:
        """Suggest architecture improvements"""
```

### 3. Embedding Service (`services/embeddings/`)

#### Chunker (`chunker.py`)
```python
class CodeChunker:
    """Chunk code for embedding generation"""
    
    def chunk_by_function(file_content: str, language: str) -> list:
        """Chunk code by function/class"""
        - Parse AST
        - Extract functions/classes
        - Include context (imports, docstrings)
        - Add metadata (file, line numbers)
    
    def chunk_by_size(text: str, max_tokens: int = 512) -> list:
        """Chunk by token size with overlap"""
        - Tokenize text
        - Create chunks with overlap
        - Preserve code structure
    
    def add_metadata(chunk: str, file_path: str, line_start: int) -> dict:
        """Add metadata to chunk"""
        - File path
        - Line numbers
        - Language
        - Chunk type (function/class/module)
```

#### Generator (`generator.py`)
```python
class EmbeddingGenerator:
    """Generate embeddings using sentence-transformers"""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def generate_embeddings(chunks: list[str]) -> np.ndarray:
        """Generate embeddings for chunks"""
        - Batch processing (32 chunks at a time)
        - Normalize vectors
        - Return numpy array
    
    async def generate_for_repository(repo_id: str) -> dict:
        """Generate embeddings for entire repository"""
        - Load and chunk all files
        - Generate embeddings in batches
        - Save to FAISS index
        - Return statistics
```

#### Indexer (`indexer.py`)
```python
class FAISSIndexer:
    """Manage FAISS indices"""
    
    def create_index(dimension: int = 384) -> faiss.Index:
        """Create new FAISS index"""
        - Use IndexFlatL2 for accuracy
        - Or IndexIVFFlat for speed
    
    def add_embeddings(index: faiss.Index, embeddings: np.ndarray, metadata: list):
        """Add embeddings to index"""
        - Add vectors to FAISS
        - Store metadata separately (JSON)
    
    def save_index(index: faiss.Index, repo_id: str):
        """Save index to disk"""
        - Save FAISS index
        - Save metadata JSON
    
    def load_index(repo_id: str) -> tuple:
        """Load index from disk"""
        - Load FAISS index
        - Load metadata
        - Return both
```

### 4. AI Service (`services/ai/`)

#### LangGraph Workflow (`workflow.py`)
```python
from langgraph.graph import StateGraph, END

class AnalysisWorkflow:
    """LangGraph workflow for repository analysis"""
    
    def create_workflow() -> StateGraph:
        """Create analysis workflow graph"""
        
        workflow = StateGraph()
        
        # Define nodes
        workflow.add_node("parse_repo", parse_repository_node)
        workflow.add_node("analyze_structure", analyze_structure_node)
        workflow.add_node("analyze_dependencies", analyze_dependencies_node)
        workflow.add_node("assess_risks", assess_risks_node)
        workflow.add_node("detect_architecture", detect_architecture_node)
        workflow.add_node("generate_summary", generate_summary_node)
        
        # Define edges
        workflow.add_edge("parse_repo", "analyze_structure")
        workflow.add_edge("analyze_structure", "analyze_dependencies")
        workflow.add_edge("analyze_dependencies", "assess_risks")
        workflow.add_edge("assess_risks", "detect_architecture")
        workflow.add_edge("detect_architecture", "generate_summary")
        workflow.add_edge("generate_summary", END)
        
        # Set entry point
        workflow.set_entry_point("parse_repo")
        
        return workflow.compile()
    
    async def run_analysis(repo_id: str) -> dict:
        """Run complete analysis workflow"""
        - Initialize workflow
        - Execute nodes sequentially
        - Handle errors gracefully
        - Return complete analysis
```

#### RAG Chain (`rag_chain.py`)
```python
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class RAGChain:
    """Retrieval-Augmented Generation for code chat"""
    
    def __init__(self, repo_id: str):
        self.repo_id = repo_id
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.vector_store = self.load_vector_store(repo_id)
    
    def create_chain(self) -> RetrievalQA:
        """Create RAG chain"""
        - Load FAISS retriever
        - Create prompt template
        - Build QA chain
        - Configure return_source_documents
    
    async def chat(self, message: str, history: list = None) -> dict:
        """Chat with codebase"""
        - Retrieve relevant code chunks (k=5)
        - Format context with history
        - Generate response
        - Return response + sources
    
    def format_sources(self, documents: list) -> list:
        """Format source documents for frontend"""
        - Extract file paths
        - Extract line numbers
        - Format code snippets
```

#### Agents (`agents.py`)
```python
class SummaryAgent:
    """Agent for generating repository summaries"""
    
    async def generate_summary(analysis_data: dict) -> str:
        """Generate AI summary"""
        - Format analysis data
        - Create prompt
        - Call LLM
        - Return summary

class ArchitectureAgent:
    """Agent for architecture analysis"""
    
    async def analyze_architecture(components: dict) -> dict:
        """Analyze architecture with AI"""

class ModernizationAgent:
    """Agent for modernization suggestions"""
    
    async def suggest_modernization(analysis: dict) -> list:
        """Generate modernization suggestions"""
```

#### Prompts (`prompts.py`)
```python
SUMMARY_PROMPT = """
You are an expert software architect analyzing a codebase.

Repository Information:
- Name: {repo_name}
- Language: {primary_language}
- Files: {file_count}
- Lines of Code: {loc}

Analysis Data:
{analysis_data}

Generate a comprehensive summary including:
1. Purpose and functionality
2. Key technologies used
3. Architecture pattern
4. Code quality assessment
5. Notable strengths and weaknesses

Summary:
"""

ARCHITECTURE_PROMPT = """..."""
MODERNIZATION_PROMPT = """..."""
CHAT_PROMPT = """..."""
```

### 5. Vector Store Service (`services/vector_store/`)

#### FAISS Manager (`faiss_manager.py`)
```python
class FAISSManager:
    """Manage FAISS vector store operations"""
    
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
    
    def create_index(self, repo_id: str, dimension: int = 384):
        """Create new FAISS index for repository"""
    
    def add_vectors(self, repo_id: str, vectors: np.ndarray, metadata: list):
        """Add vectors to existing index"""
    
    def search(self, repo_id: str, query_vector: np.ndarray, k: int = 5) -> list:
        """Search for similar vectors"""
        - Perform similarity search
        - Retrieve metadata
        - Format results
    
    def get_index_stats(self, repo_id: str) -> dict:
        """Get index statistics"""
        - Total vectors
        - Index size
        - Last updated
```

#### Retriever (`retriever.py`)
```python
class VectorRetriever:
    """Retrieve relevant code chunks"""
    
    def __init__(self, repo_id: str):
        self.repo_id = repo_id
        self.faiss_manager = FAISSManager()
        self.embedding_generator = EmbeddingGenerator()
    
    async def retrieve(self, query: str, k: int = 5) -> list:
        """Retrieve relevant code chunks"""
        - Generate query embedding
        - Search FAISS index
        - Retrieve metadata
        - Format results with context
    
    def rerank_results(self, results: list, query: str) -> list:
        """Rerank results by relevance"""
        - Calculate semantic similarity
        - Consider code structure
        - Return sorted results
```

## 📊 Data Models

### Repository Model (`models/repository.py`)
```python
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class Repository(BaseModel):
    id: str
    url: HttpUrl
    name: str
    owner: str
    status: str  # cloning, ready, analyzing, error
    created_at: datetime
    updated_at: datetime
    metadata: Optional[dict] = None
    
class RepositoryMetadata(BaseModel):
    stars: int
    forks: int
    language: str
    size_mb: float
    file_count: int
    loc: int
    last_commit: datetime
```

### Analysis Model (`models/analysis.py`)
```python
class AnalysisResult(BaseModel):
    repo_id: str
    summary: str
    architecture: ArchitectureAnalysis
    dependencies: DependencyAnalysis
    risks: RiskAnalysis
    modernization: ModernizationSuggestions
    created_at: datetime

class ArchitectureAnalysis(BaseModel):
    pattern: str
    components: list[Component]
    graph: dict
    
class DependencyAnalysis(BaseModel):
    total: int
    outdated: list[Dependency]
    vulnerabilities: list[Vulnerability]
    
class RiskAnalysis(BaseModel):
    score: float
    risks: list[Risk]
    recommendations: list[str]
```

### Chat Model (`models/chat.py`)
```python
class ChatMessage(BaseModel):
    role: str  # user, assistant
    content: str
    timestamp: datetime
    sources: Optional[list[Source]] = None

class ChatRequest(BaseModel):
    repo_id: str
    message: str
    history: Optional[list[ChatMessage]] = None

class ChatResponse(BaseModel):
    response: str
    sources: list[Source]
    confidence: float
```

## 🔐 Security Implementation

### API Key Authentication (`core/security.py`)
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    """Verify API key"""
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

# Usage in endpoints
@router.post("/repositories/clone")
async def clone_repository(
    request: CloneRequest,
    api_key: str = Depends(verify_api_key)
):
    ...
```

## ⚙️ Configuration (`core/config.py`)

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "LegacyMind AI API"
    API_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Security
    API_KEY: str
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"
    
    # GitHub
    GITHUB_TOKEN: str = ""
    
    # Storage
    STORAGE_PATH: str = "./app/storage"
    MAX_REPO_SIZE_MB: int = 500
    
    # Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    
    # FAISS
    FAISS_INDEX_TYPE: str = "IndexFlatL2"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

## 📦 Dependencies Explained

### Core Framework
```txt
fastapi==0.109.0              # Modern async web framework
  - High performance
  - Automatic API docs
  - Type validation
  - Async/await support

uvicorn[standard]==0.27.0     # ASGI server
  - Production-ready
  - WebSocket support
  - Auto-reload in dev
```

### Data Validation
```txt
pydantic==2.5.0               # Data validation
  - Type checking
  - Serialization
  - Settings management

pydantic-settings==2.1.0      # Environment variables
  - Load from .env
  - Type validation
  - Default values
```

### AI/ML Stack
```txt
langchain==0.1.0              # LLM framework
  - Chain management
  - Prompt templates
  - Memory management

langgraph==0.0.20             # Workflow orchestration
  - Stateful workflows
  - Graph-based execution
  - Error handling

openai==1.10.0                # OpenAI API client
  - GPT-4 access
  - Streaming support
  - Function calling

sentence-transformers==2.3.1  # Embedding generation
  - Pre-trained models
  - Fast inference
  - 384-dim vectors

faiss-cpu==1.7.4              # Vector similarity search
  - Fast search
  - CPU-optimized
  - Scalable to millions
```

### GitHub Integration
```txt
gitpython==3.1.41             # Git operations
  - Clone repositories
  - Git commands
  - Repository info

PyGithub==2.1.1               # GitHub API client
  - Fetch metadata
  - API rate limiting
  - Authentication
```

### Utilities
```txt
python-dotenv==1.0.0          # Environment variables
  - Load .env files
  - Development setup

httpx==0.26.0                 # Async HTTP client
  - API calls
  - Better than requests
  - Async support

aiofiles==23.2.1              # Async file I/O
  - Non-blocking file ops
  - Better performance

python-multipart==0.0.6       # File uploads
  - Handle multipart forms
  - File upload support
```

### Development Dependencies (`requirements-dev.txt`)
```txt
pytest==7.4.3                 # Testing framework
pytest-asyncio==0.21.1        # Async test support
pytest-cov==4.1.0             # Code coverage
black==23.12.1                # Code formatter
isort==5.13.2                 # Import sorting
mypy==1.7.1                   # Type checking
flake8==6.1.0                 # Linting
```

## 🚀 Deployment Configuration

### Render Configuration (`render.yaml`)
```yaml
services:
  - type: web
    name: legacymind-api
    env: python
    region: oregon
    plan: starter
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements.txt
      python scripts/setup_storage.py
      python scripts/download_models.py
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: API_KEY
        generateValue: true
      - key: OPENAI_API_KEY
        sync: false
      - key: GITHUB_TOKEN
        sync: false
      - key: STORAGE_PATH
        value: /opt/render/project/src/app/storage
      - key: CORS_ORIGINS
        value: https://legacymind.vercel.app
    disk:
      name: storage
      mountPath: /opt/render/project/src/app/storage
      sizeGB: 10
```

### Dockerfile (Optional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY scripts/ ./scripts/

# Create storage directories
RUN python scripts/setup_storage.py

# Download models
RUN python scripts/download_models.py

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 Environment Variables Template (`.env.example`)

```env
# API Configuration
API_TITLE=LegacyMind AI API
API_VERSION=1.0.0
API_HOST=0.0.0.0
API_PORT=8000

# Security (Generate a secure random key)
API_KEY=your_secure_api_key_here

# OpenAI Configuration
OPENAI_API_KEY=sk-your_openai_api_key_here
OPENAI_MODEL=gpt-4

# GitHub Configuration (Optional)
GITHUB_TOKEN=ghp_your_github_token_here

# Storage Configuration
STORAGE_PATH=./app/storage
MAX_REPO_SIZE_MB=500

# Embedding Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
CHUNK_SIZE=512
CHUNK_OVERLAP=50

# FAISS Configuration
FAISS_INDEX_TYPE=IndexFlatL2

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://legacymind.vercel.app

# Logging Configuration
LOG_LEVEL=INFO
```

## 🎯 Implementation Priority

### Phase 1: Foundation (2-3 hours)
1. ✅ Create folder structure
2. ✅ Set up configuration (`core/config.py`)
3. ✅ Create main FastAPI app (`main.py`)
4. ✅ Implement health endpoint
5. ✅ Set up API key authentication
6. ✅ Configure CORS

### Phase 2: GitHub Integration (2-3 hours)
1. ✅ Implement repository cloner
2. ✅ Implement code parser
3. ✅ Implement metadata extractor
4. ✅ Create repository endpoints
5. ✅ Test cloning functionality

### Phase 3: Embeddings (2-3 hours)
1. ✅ Implement code chunker
2. ✅ Implement embedding generator
3. ✅ Implement FAISS indexer
4. ✅ Create embedding endpoints
5. ✅ Test embedding generation

### Phase 4: Analysis Services (3-4 hours)
1. ✅ Implement code analyzer
2. ✅ Implement dependency analyzer
3. ✅ Implement risk analyzer
4. ✅ Implement architecture detector
5. ✅ Create analysis endpoints

### Phase 5: AI Integration (3-4 hours)
1. ✅ Implement LangGraph workflow
2. ✅ Implement RAG chain
3. ✅ Implement AI agents
4. ✅ Create chat endpoint
5. ✅ Test AI responses

### Phase 6: Testing & Polish (2-3 hours)
1. ✅ Write unit tests
2. ✅ Write integration tests
3. ✅ Add error handling
4. ✅ Add logging
5. ✅ Optimize performance

### Phase 7: Deployment (1-2 hours)
1. ✅ Configure Render deployment
2. ✅ Set up environment variables
3. ✅ Deploy to Render
4. ✅ Test production API
5. ✅ Update frontend API URL

## 📊 Success Metrics

- ✅ API responds to health checks
- ✅ Successfully clones repositories
- ✅ Generates embeddings in <30 seconds
- ✅ Analysis completes in <2 minutes
- ✅ Chat responds in <3 seconds
- ✅ API documentation accessible
- ✅ All endpoints secured with API key
- ✅ Deployed and accessible online

## 🎉 Next Steps

1. Review this architecture plan
2. Approve the approach
3. Switch to Code mode to implement
4. Follow the implementation priority
5. Test each phase before moving forward
6. Deploy and celebrate! 🚀