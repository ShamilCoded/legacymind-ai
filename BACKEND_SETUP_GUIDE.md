# LegacyMind AI - Backend Setup Guide

## 🚀 Quick Start

This guide provides step-by-step instructions to set up the FastAPI backend for LegacyMind AI.

## 📋 Prerequisites

- **Python 3.11+** installed
- **Git** installed
- **OpenAI API Key** (required)
- **GitHub Token** (optional, for private repos)

## 🏗️ Step 1: Create Project Structure

```bash
# Navigate to project root
cd backend

# Create all directories
mkdir -p app/{api/{v1/endpoints},core,models,services/{github,analysis,embeddings,ai,vector_store},utils,storage/{repositories,embeddings,analysis,cache}}
mkdir -p tests/{test_api,test_services}
mkdir -p scripts

# Create __init__.py files
touch app/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/api/v1/endpoints/__init__.py
touch app/core/__init__.py
touch app/models/__init__.py
touch app/services/__init__.py
touch app/services/github/__init__.py
touch app/services/analysis/__init__.py
touch app/services/embeddings/__init__.py
touch app/services/ai/__init__.py
touch app/services/vector_store/__init__.py
touch app/utils/__init__.py
touch tests/__init__.py
```

## 📦 Step 2: Create Requirements Files

### `requirements.txt`
```txt
# Core Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
pydantic-settings==2.1.0

# AI/ML Stack
langchain==0.1.0
langgraph==0.0.20
openai==1.10.0
sentence-transformers==2.3.1
faiss-cpu==1.7.4

# GitHub Integration
gitpython==3.1.41
PyGithub==2.1.1

# Code Analysis
tree-sitter==0.20.4
radon==6.0.1

# Utilities
python-dotenv==1.0.0
httpx==0.26.0
aiofiles==23.2.1
python-multipart==0.0.6

# Additional
numpy==1.24.3
```

### `requirements-dev.txt`
```txt
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.26.0

# Code Quality
black==23.12.1
isort==5.13.2
mypy==1.7.1
flake8==6.1.0
pylint==3.0.3

# Development
ipython==8.18.1
```

## 🔧 Step 3: Create Environment Configuration

### `.env.example`
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

### Create your `.env` file
```bash
cp .env.example .env
# Edit .env and add your actual API keys
```

## 📝 Step 4: Create Core Configuration Files

### `app/core/config.py`
```python
"""Application configuration using Pydantic settings."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
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
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
```

### `app/core/security.py`
```python
"""Security utilities for API key authentication."""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """
    Verify API key from request header.
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        The verified API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key is missing"
        )
    
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return api_key
```

### `app/core/logging.py`
```python
"""Logging configuration."""
import logging
import sys
from app.core.config import settings


def setup_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set third-party loggers to WARNING
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
```

### `app/core/exceptions.py`
```python
"""Custom exception classes."""


class LegacyMindException(Exception):
    """Base exception for LegacyMind AI."""
    pass


class RepositoryError(LegacyMindException):
    """Repository-related errors."""
    pass


class RepositoryNotFoundError(RepositoryError):
    """Repository not found."""
    pass


class RepositoryCloneError(RepositoryError):
    """Failed to clone repository."""
    pass


class RepositorySizeError(RepositoryError):
    """Repository exceeds size limit."""
    pass


class AnalysisError(LegacyMindException):
    """Analysis-related errors."""
    pass


class EmbeddingError(LegacyMindException):
    """Embedding generation errors."""
    pass


class VectorStoreError(LegacyMindException):
    """Vector store errors."""
    pass


class AIServiceError(LegacyMindException):
    """AI service errors."""
    pass
```

## 🎯 Step 5: Create Main Application

### `app/main.py`
```python
"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.v1.router import api_router

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="AI-powered legacy code analysis and modernization platform",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
    logger.info(f"Storage path: {settings.STORAGE_PATH}")
    logger.info(f"CORS origins: {settings.CORS_ORIGINS}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down application")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        content={
            "status": "healthy",
            "version": settings.API_VERSION,
            "service": settings.API_TITLE
        }
    )


# Include API router
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
```

## 🔌 Step 6: Create API Structure

### `app/api/deps.py`
```python
"""API dependencies."""
from typing import Generator
from app.core.security import verify_api_key


def get_api_key() -> Generator:
    """Dependency for API key verification."""
    return verify_api_key
```

### `app/api/v1/router.py`
```python
"""Main API v1 router."""
from fastapi import APIRouter
from app.api.v1.endpoints import health, repositories, analysis, chat, embeddings

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(repositories.router, prefix="/repositories", tags=["repositories"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])
```

### `app/api/v1/endpoints/health.py`
```python
"""Health check endpoints."""
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/status")
async def get_status():
    """Get API status."""
    return {
        "status": "operational",
        "version": settings.API_VERSION,
        "service": settings.API_TITLE
    }
```

### `app/api/v1/endpoints/repositories.py`
```python
"""Repository management endpoints."""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.core.security import verify_api_key
from app.models.schemas import CloneRequest, RepositoryResponse

router = APIRouter()


@router.post("/clone", response_model=RepositoryResponse)
async def clone_repository(
    request: CloneRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Clone a GitHub repository.
    
    This endpoint initiates the cloning process in the background.
    """
    # TODO: Implement repository cloning
    return {
        "repo_id": "placeholder",
        "url": request.url,
        "status": "cloning",
        "message": "Repository cloning initiated"
    }


@router.get("/{repo_id}", response_model=RepositoryResponse)
async def get_repository(
    repo_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get repository details by ID."""
    # TODO: Implement repository retrieval
    raise HTTPException(status_code=404, detail="Repository not found")


@router.get("/")
async def list_repositories(
    limit: int = 10,
    offset: int = 0,
    api_key: str = Depends(verify_api_key)
):
    """List all repositories."""
    # TODO: Implement repository listing
    return {
        "repositories": [],
        "total": 0,
        "limit": limit,
        "offset": offset
    }


@router.delete("/{repo_id}")
async def delete_repository(
    repo_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Delete a repository."""
    # TODO: Implement repository deletion
    return {"message": "Repository deleted successfully"}
```

### `app/api/v1/endpoints/analysis.py`
```python
"""Analysis endpoints."""
from fastapi import APIRouter, Depends
from app.core.security import verify_api_key

router = APIRouter()


@router.post("/summarize")
async def generate_summary(
    repo_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Generate AI summary of repository."""
    # TODO: Implement summary generation
    return {"summary": "Summary placeholder"}


@router.post("/architecture")
async def analyze_architecture(
    repo_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Analyze repository architecture."""
    # TODO: Implement architecture analysis
    return {"pattern": "Unknown", "components": []}


@router.post("/dependencies")
async def analyze_dependencies(
    repo_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Analyze repository dependencies."""
    # TODO: Implement dependency analysis
    return {"dependencies": [], "outdated": [], "vulnerabilities": []}


@router.post("/risks")
async def assess_risks(
    repo_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Assess repository risks."""
    # TODO: Implement risk assessment
    return {"risk_score": 0.0, "risks": []}


@router.post("/modernization")
async def suggest_modernization(
    repo_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Generate modernization suggestions."""
    # TODO: Implement modernization suggestions
    return {"suggestions": []}


@router.get("/{repo_id}/full")
async def get_full_analysis(
    repo_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get complete analysis for repository."""
    # TODO: Implement full analysis retrieval
    return {
        "summary": {},
        "architecture": {},
        "dependencies": {},
        "risks": {},
        "modernization": {}
    }
```

### `app/api/v1/endpoints/chat.py`
```python
"""Chat endpoints."""
from fastapi import APIRouter, Depends
from app.core.security import verify_api_key
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat_with_codebase(
    request: ChatRequest,
    api_key: str = Depends(verify_api_key)
):
    """Chat with codebase using RAG."""
    # TODO: Implement RAG chat
    return {
        "response": "Chat response placeholder",
        "sources": [],
        "confidence": 0.0
    }


@router.get("/{repo_id}/history")
async def get_chat_history(
    repo_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get chat history for repository."""
    # TODO: Implement chat history retrieval
    return {"messages": []}


@router.delete("/{repo_id}/history")
async def clear_chat_history(
    repo_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Clear chat history for repository."""
    # TODO: Implement chat history clearing
    return {"message": "Chat history cleared"}
```

### `app/api/v1/endpoints/embeddings.py`
```python
"""Embedding endpoints."""
from fastapi import APIRouter, Depends, BackgroundTasks
from app.core.security import verify_api_key

router = APIRouter()


@router.post("/generate")
async def generate_embeddings(
    repo_id: str,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """Generate embeddings for repository."""
    # TODO: Implement embedding generation
    return {
        "status": "processing",
        "message": "Embedding generation initiated"
    }


@router.get("/{repo_id}/status")
async def get_embedding_status(
    repo_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get embedding generation status."""
    # TODO: Implement status retrieval
    return {
        "status": "unknown",
        "chunks": 0,
        "index_size": "0MB"
    }


@router.post("/search")
async def search_embeddings(
    repo_id: str,
    query: str,
    k: int = 5,
    api_key: str = Depends(verify_api_key)
):
    """Search embeddings by query."""
    # TODO: Implement embedding search
    return {"results": []}
```

## 📊 Step 7: Create Data Models

### `app/models/schemas.py`
```python
"""Pydantic schemas for API requests and responses."""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field


# Repository Schemas
class CloneRequest(BaseModel):
    """Request to clone a repository."""
    url: HttpUrl = Field(..., description="GitHub repository URL")


class RepositoryResponse(BaseModel):
    """Repository response."""
    repo_id: str
    url: str
    status: str
    message: Optional[str] = None
    created_at: Optional[datetime] = None


# Chat Schemas
class ChatMessage(BaseModel):
    """Chat message."""
    role: str = Field(..., description="Message role (user/assistant)")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request."""
    repo_id: str = Field(..., description="Repository ID")
    message: str = Field(..., description="User message")
    history: Optional[List[ChatMessage]] = Field(default=None, description="Chat history")


class Source(BaseModel):
    """Source code reference."""
    file_path: str
    line_start: int
    line_end: int
    content: str


class ChatResponse(BaseModel):
    """Chat response."""
    response: str = Field(..., description="AI response")
    sources: List[Source] = Field(default=[], description="Source code references")
    confidence: float = Field(..., description="Response confidence score")


# Analysis Schemas
class AnalysisSummary(BaseModel):
    """Analysis summary."""
    summary: str
    key_points: List[str]
    technologies: List[str]


class ArchitectureAnalysis(BaseModel):
    """Architecture analysis."""
    pattern: str
    components: List[dict]
    graph: dict


class DependencyAnalysis(BaseModel):
    """Dependency analysis."""
    dependencies: List[dict]
    outdated: List[dict]
    vulnerabilities: List[dict]


class RiskAnalysis(BaseModel):
    """Risk analysis."""
    risk_score: float
    risks: List[dict]
    recommendations: List[str]


class ModernizationSuggestions(BaseModel):
    """Modernization suggestions."""
    suggestions: List[dict]
    priority: str
```

## 🛠️ Step 8: Create Utility Scripts

### `scripts/setup_storage.py`
```python
"""Create storage directories."""
import os
from pathlib import Path


def setup_storage():
    """Create all required storage directories."""
    base_path = Path("app/storage")
    
    directories = [
        base_path / "repositories",
        base_path / "embeddings",
        base_path / "analysis",
        base_path / "cache"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {directory}")
    
    print("\n✅ Storage directories created successfully!")


if __name__ == "__main__":
    setup_storage()
```

### `scripts/download_models.py`
```python
"""Download required ML models."""
from sentence_transformers import SentenceTransformer


def download_models():
    """Download sentence-transformers model."""
    print("Downloading embedding model...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    print("✅ Model downloaded successfully!")
    
    # Test the model
    print("\nTesting model...")
    embeddings = model.encode(["Hello world"])
    print(f"✓ Model working! Embedding dimension: {embeddings.shape[1]}")


if __name__ == "__main__":
    download_models()
```

### `scripts/cleanup.py`
```python
"""Cleanup old repositories and cache."""
import shutil
from pathlib import Path
from datetime import datetime, timedelta


def cleanup_old_data(days: int = 7):
    """Remove data older than specified days."""
    base_path = Path("app/storage")
    cutoff_date = datetime.now() - timedelta(days=days)
    
    for directory in ["repositories", "embeddings", "analysis", "cache"]:
        dir_path = base_path / directory
        if not dir_path.exists():
            continue
        
        for item in dir_path.iterdir():
            if item.is_dir():
                # Check modification time
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                if mtime < cutoff_date:
                    shutil.rmtree(item)
                    print(f"✓ Removed {item}")
    
    print(f"\n✅ Cleanup complete! Removed data older than {days} days.")


if __name__ == "__main__":
    cleanup_old_data()
```

## 🧪 Step 9: Create Test Configuration

### `tests/conftest.py`
```python
"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def api_key():
    """Return test API key."""
    return "test_api_key"


@pytest.fixture
def headers(api_key):
    """Return headers with API key."""
    return {"X-API-Key": api_key}
```

### `tests/test_api/test_health.py`
```python
"""Test health endpoints."""


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_status(client, headers):
    """Test API status endpoint."""
    response = client.get("/api/v1/status", headers=headers)
    assert response.status_code == 200
    assert "status" in response.json()
```

## 📝 Step 10: Create Additional Configuration Files

### `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local

# Storage
app/storage/repositories/*
app/storage/embeddings/*
app/storage/analysis/*
app/storage/cache/*
!app/storage/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log
```

### `pyproject.toml`
```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

### `README.md`
```markdown
# LegacyMind AI - Backend

FastAPI backend for LegacyMind AI - AI-powered legacy code analysis platform.

## Features

- 🔄 Repository cloning and parsing
- 🧠 AI-powered code analysis
- 📊 Architecture detection
- 🔍 Dependency analysis
- ⚠️ Risk assessment
- 💬 RAG-based chat with codebase
- 🔐 API key authentication

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Create storage directories:
```bash
python scripts/setup_storage.py
```

4. Download models:
```bash
python scripts/download_models.py
```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

6. Visit API docs: http://localhost:8000/docs

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
pytest
```

## Deployment

See `render.yaml` for Render deployment configuration.
```

## 🚀 Step 11: Install and Run

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up storage
python scripts/setup_storage.py

# Download models
python scripts/download_models.py

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Verification Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] `.env` file created with API keys
- [ ] Storage directories created
- [ ] ML models downloaded
- [ ] Server starts without errors
- [ ] Health check responds: `curl http://localhost:8000/health`
- [ ] API docs accessible: http://localhost:8000/docs
- [ ] Can make authenticated requests with API key

## 🎯 Next Steps

1. ✅ Complete the TODO items in endpoint files
2. ✅ Implement service layer (GitHub, Analysis, Embeddings, AI)
3. ✅ Add comprehensive error handling
4. ✅ Write unit and integration tests
5. ✅ Optimize performance
6. ✅ Deploy to Render

## 📚 Documentation

- [Backend Architecture Plan](../BACKEND_ARCHITECTURE_PLAN.md)
- [Implementation Plan](../IMPLEMENTATION_PLAN.md)
- [API Documentation](http://localhost:8000/docs)

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Module Not Found
```bash
pip install -r requirements.txt --upgrade
```

### OpenAI API Error
- Verify API key in `.env`
- Check OpenAI account has credits
- Restart server after updating `.env`

## 🎉 Success!

Your backend is now set up and ready for development! 🚀