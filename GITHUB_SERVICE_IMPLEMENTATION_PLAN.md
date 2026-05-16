# GitHub Service Layer - Implementation Plan

## 📋 Overview

This document provides a detailed implementation plan for the GitHub service layer of LegacyMind AI, focusing on repository cloning, code scanning, and content extraction with support for Python, JavaScript, TypeScript, Java, and C# files.

## 🎯 Core Requirements

### Functional Requirements
1. **Accept GitHub repository URL** - Validate and parse GitHub URLs
2. **Clone repository using GitPython** - Secure cloning with size limits
3. **Scan code files** - Recursive directory traversal
4. **Extract code content** - Read and process file contents
5. **Ignore node_modules and binary files** - Smart filtering
6. **Support multiple languages** - Python (.py), JavaScript (.js), TypeScript (.ts), Java (.java), C# (.cs)

### Non-Functional Requirements
- **Performance**: Clone repos < 500MB in under 30 seconds
- **Security**: Validate URLs, prevent path traversal, limit repo size
- **Reliability**: Handle network failures, corrupted repos
- **Maintainability**: Clean, modular, well-documented code

## 🏗️ Architecture Integration

### Fits into LegacyMind AI Backend Structure
```
backend/
├── app/
│   ├── services/
│   │   └── github/              # ← THIS IS WHAT WE'RE BUILDING
│   │       ├── __init__.py
│   │       ├── cloner.py        # Repository cloning
│   │       ├── parser.py        # Code file parsing
│   │       └── metadata.py      # GitHub metadata extraction
│   ├── models/
│   │   └── repository.py        # Repository data models
│   ├── api/v1/endpoints/
│   │   └── repositories.py      # API endpoints
│   └── utils/
│       ├── file_utils.py        # File operations
│       ├── git_utils.py         # Git utilities
│       └── validators.py        # URL validation
```

## 📦 Dependencies

### Core Dependencies (Already in requirements.txt)
```python
gitpython==3.1.41          # Git operations
PyGithub==2.1.1            # GitHub API integration
aiofiles==23.2.1           # Async file I/O
httpx==0.26.0              # Async HTTP client
pydantic==2.5.0            # Data validation
```

### File Type Detection
```python
# Built-in Python modules (no additional dependencies)
import mimetypes
import pathlib
```

## 🔧 Implementation Details

### 1. Repository Cloner (`services/github/cloner.py`)

#### Class: `RepositoryCloner`

**Purpose**: Clone GitHub repositories with validation and size limits

**Key Methods**:

```python
class RepositoryCloner:
    """Clone and manage GitHub repositories"""
    
    def __init__(self, storage_path: str, max_size_mb: int = 500):
        """Initialize cloner with storage configuration"""
        
    async def clone_repository(self, url: str) -> dict:
        """
        Clone a GitHub repository
        
        Args:
            url: GitHub repository URL
            
        Returns:
            dict: {
                "repo_id": str,
                "local_path": str,
                "status": str,
                "size_mb": float
            }
            
        Raises:
            InvalidURLError: Invalid GitHub URL
            RepositoryTooLargeError: Repository exceeds size limit
            CloneError: Git clone operation failed
        """
        
    def validate_github_url(self, url: str) -> tuple[str, str]:
        """
        Validate and parse GitHub URL
        
        Returns:
            tuple: (owner, repo_name)
        """
        
    def generate_repo_id(self, owner: str, repo_name: str) -> str:
        """Generate unique repository ID"""
        
    async def check_repo_size(self, owner: str, repo_name: str) -> float:
        """
        Check repository size before cloning
        
        Returns:
            float: Size in MB
        """
        
    async def cleanup_repository(self, repo_id: str) -> bool:
        """Delete cloned repository"""
        
    async def cleanup_old_repositories(self, days: int = 7) -> int:
        """Remove repositories older than N days"""
```

**Implementation Strategy**:
1. Validate GitHub URL format
2. Check repository size via GitHub API
3. Generate unique repo_id (UUID + timestamp)
4. Clone to `storage/repositories/{repo_id}/`
5. Verify clone success
6. Return repository metadata

**Error Handling**:
- Invalid URL → `InvalidURLError`
- Size too large → `RepositoryTooLargeError`
- Network failure → `CloneError` with retry logic
- Disk space → `StorageError`

### 2. Code Parser (`services/github/parser.py`)

#### Class: `CodeParser`

**Purpose**: Parse code files with language-specific filtering

**Key Methods**:

```python
class CodeParser:
    """Parse and analyze code files"""
    
    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript',
        '.java': 'Java',
        '.cs': 'C#'
    }
    
    # Directories to ignore
    IGNORE_DIRS = {
        'node_modules',
        '__pycache__',
        '.git',
        'venv',
        'env',
        'dist',
        'build',
        'target',
        '.next',
        'out',
        'bin',
        'obj'
    }
    
    # Binary file extensions to skip
    BINARY_EXTENSIONS = {
        '.exe', '.dll', '.so', '.dylib',
        '.jpg', '.jpeg', '.png', '.gif', '.ico',
        '.pdf', '.zip', '.tar', '.gz',
        '.mp4', '.mp3', '.wav',
        '.woff', '.woff2', '.ttf', '.eot'
    }
    
    async def parse_repository(self, repo_path: str) -> dict:
        """
        Parse all code files in repository
        
        Returns:
            dict: {
                "total_files": int,
                "files_by_language": dict,
                "total_lines": int,
                "files": list[dict]
            }
        """
        
    async def scan_directory(self, directory: str) -> list[dict]:
        """
        Recursively scan directory for code files
        
        Returns:
            list[dict]: List of file metadata
        """
        
    def should_ignore_path(self, path: str) -> bool:
        """Check if path should be ignored"""
        
    def is_binary_file(self, file_path: str) -> bool:
        """Check if file is binary"""
        
    def detect_language(self, file_path: str) -> str:
        """Detect programming language from extension"""
        
    async def extract_file_content(self, file_path: str) -> dict:
        """
        Extract content and metadata from file
        
        Returns:
            dict: {
                "path": str,
                "language": str,
                "lines": int,
                "size_bytes": int,
                "content": str
            }
        """
        
    def count_lines(self, content: str) -> int:
        """Count non-empty lines"""
        
    async def parse_dependencies(self, repo_path: str) -> dict:
        """
        Parse dependency files
        
        Looks for:
        - package.json (JavaScript/TypeScript)
        - requirements.txt (Python)
        - pom.xml (Java)
        - *.csproj (C#)
        
        Returns:
            dict: {
                "package_manager": str,
                "dependencies": list[str]
            }
        """
```

**Implementation Strategy**:
1. Walk directory tree using `os.walk()`
2. Filter out ignored directories (node_modules, etc.)
3. Check file extensions against supported languages
4. Skip binary files using magic number detection
5. Read file content asynchronously
6. Extract metadata (lines, size, language)
7. Return structured data

**Filtering Logic**:
```python
def should_process_file(file_path: str) -> bool:
    """Determine if file should be processed"""
    # Check extension
    if not has_supported_extension(file_path):
        return False
    
    # Check if binary
    if is_binary_file(file_path):
        return False
    
    # Check path components
    if any(ignored in file_path for ignored in IGNORE_DIRS):
        return False
    
    return True
```

### 3. Metadata Extractor (`services/github/metadata.py`)

#### Class: `MetadataExtractor`

**Purpose**: Extract repository metadata from GitHub API

**Key Methods**:

```python
class MetadataExtractor:
    """Extract repository metadata"""
    
    def __init__(self, github_token: Optional[str] = None):
        """Initialize with optional GitHub token"""
        
    async def get_github_metadata(self, owner: str, repo_name: str) -> dict:
        """
        Fetch metadata from GitHub API
        
        Returns:
            dict: {
                "name": str,
                "full_name": str,
                "description": str,
                "stars": int,
                "forks": int,
                "watchers": int,
                "language": str,
                "languages": dict,
                "topics": list[str],
                "license": str,
                "created_at": str,
                "updated_at": str,
                "size_kb": int,
                "default_branch": str,
                "open_issues": int,
                "has_wiki": bool,
                "has_pages": bool
            }
        """
        
    async def get_language_stats(self, owner: str, repo_name: str) -> dict:
        """Get language breakdown from GitHub"""
        
    async def get_contributors_count(self, owner: str, repo_name: str) -> int:
        """Get number of contributors"""
        
    def extract_local_metadata(self, repo_path: str) -> dict:
        """
        Extract metadata from local repository
        
        Returns:
            dict: {
                "file_count": int,
                "directory_count": int,
                "total_size_mb": float,
                "languages": dict,
                "has_readme": bool,
                "has_license": bool,
                "has_tests": bool
            }
        """
```

**Implementation Strategy**:
1. Use PyGithub library for API calls
2. Handle rate limiting gracefully
3. Cache responses to avoid redundant API calls
4. Combine GitHub API data with local analysis
5. Return comprehensive metadata

## 📊 Data Models

### Repository Model (`models/repository.py`)

```python
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum

class RepositoryStatus(str, Enum):
    """Repository processing status"""
    PENDING = "pending"
    CLONING = "cloning"
    CLONED = "cloned"
    PARSING = "parsing"
    READY = "ready"
    ERROR = "error"

class LanguageStats(BaseModel):
    """Language statistics"""
    language: str
    file_count: int
    line_count: int
    percentage: float

class RepositoryMetadata(BaseModel):
    """GitHub repository metadata"""
    name: str
    full_name: str
    description: Optional[str] = None
    stars: int = 0
    forks: int = 0
    watchers: int = 0
    primary_language: Optional[str] = None
    languages: Dict[str, int] = Field(default_factory=dict)
    topics: List[str] = Field(default_factory=list)
    license: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    size_kb: int = 0
    default_branch: str = "main"
    open_issues: int = 0

class CodeFile(BaseModel):
    """Parsed code file"""
    path: str
    relative_path: str
    language: str
    lines: int
    size_bytes: int
    content: str
    
class ParsedRepository(BaseModel):
    """Parsed repository data"""
    total_files: int
    total_lines: int
    total_size_mb: float
    languages: List[LanguageStats]
    files: List[CodeFile]
    dependencies: Dict[str, List[str]] = Field(default_factory=dict)

class Repository(BaseModel):
    """Complete repository model"""
    id: str = Field(description="Unique repository ID")
    url: HttpUrl = Field(description="GitHub repository URL")
    owner: str
    name: str
    status: RepositoryStatus = RepositoryStatus.PENDING
    local_path: Optional[str] = None
    metadata: Optional[RepositoryMetadata] = None
    parsed_data: Optional[ParsedRepository] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None
```

### API Schemas (`models/schemas.py`)

```python
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List

class CloneRepositoryRequest(BaseModel):
    """Request to clone a repository"""
    url: HttpUrl = Field(description="GitHub repository URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://github.com/facebook/react"
            }
        }

class CloneRepositoryResponse(BaseModel):
    """Response after cloning repository"""
    repo_id: str
    status: str
    message: str
    
class RepositoryDetailResponse(BaseModel):
    """Detailed repository information"""
    id: str
    url: str
    owner: str
    name: str
    status: str
    metadata: Optional[dict] = None
    parsed_data: Optional[dict] = None
    created_at: str
    updated_at: str

class RepositoryListResponse(BaseModel):
    """List of repositories"""
    repositories: List[RepositoryDetailResponse]
    total: int
    limit: int
    offset: int
```

## 🔌 API Endpoints

### Repository Endpoints (`api/v1/endpoints/repositories.py`)

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List

router = APIRouter(prefix="/repositories", tags=["repositories"])

@router.post("/clone", response_model=CloneRepositoryResponse)
async def clone_repository(
    request: CloneRepositoryRequest,
    background_tasks: BackgroundTasks,
    cloner: RepositoryCloner = Depends(get_cloner),
    parser: CodeParser = Depends(get_parser),
    metadata_extractor: MetadataExtractor = Depends(get_metadata_extractor)
):
    """
    Clone a GitHub repository and parse its contents
    
    This endpoint:
    1. Validates the GitHub URL
    2. Checks repository size
    3. Clones the repository
    4. Parses code files (background task)
    5. Extracts metadata (background task)
    
    Returns immediately with repo_id and status
    """

@router.get("/{repo_id}", response_model=RepositoryDetailResponse)
async def get_repository(
    repo_id: str,
    repo_manager: RepositoryManager = Depends(get_repo_manager)
):
    """Get repository details by ID"""

@router.get("/", response_model=RepositoryListResponse)
async def list_repositories(
    limit: int = 10,
    offset: int = 0,
    repo_manager: RepositoryManager = Depends(get_repo_manager)
):
    """List all repositories"""

@router.delete("/{repo_id}")
async def delete_repository(
    repo_id: str,
    cloner: RepositoryCloner = Depends(get_cloner),
    repo_manager: RepositoryManager = Depends(get_repo_manager)
):
    """Delete a repository"""

@router.get("/{repo_id}/files", response_model=List[CodeFile])
async def get_repository_files(
    repo_id: str,
    language: Optional[str] = None,
    repo_manager: RepositoryManager = Depends(get_repo_manager)
):
    """Get all code files from repository, optionally filtered by language"""
```

## 🛠️ Utility Modules

### File Utils (`utils/file_utils.py`)

```python
import os
import shutil
import aiofiles
from pathlib import Path
from typing import Optional

async def read_file_async(file_path: str) -> str:
    """Read file content asynchronously"""

async def write_file_async(file_path: str, content: str) -> None:
    """Write file content asynchronously"""

def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""

def get_directory_size(directory: str) -> int:
    """Get total directory size in bytes"""

def ensure_directory(directory: str) -> None:
    """Create directory if it doesn't exist"""

def delete_directory(directory: str) -> None:
    """Delete directory and all contents"""

def is_text_file(file_path: str) -> bool:
    """Check if file is text (not binary)"""

def get_file_extension(file_path: str) -> str:
    """Get file extension"""

def get_relative_path(file_path: str, base_path: str) -> str:
    """Get relative path from base"""
```

### Git Utils (`utils/git_utils.py`)

```python
from git import Repo, GitCommandError
from typing import Optional

def clone_repo(url: str, destination: str) -> Repo:
    """Clone git repository"""

def get_repo_info(repo_path: str) -> dict:
    """Get repository information"""

def get_commit_count(repo_path: str) -> int:
    """Get total commit count"""

def get_branch_name(repo_path: str) -> str:
    """Get current branch name"""

def get_remote_url(repo_path: str) -> str:
    """Get remote URL"""
```

### Validators (`utils/validators.py`)

```python
import re
from typing import Tuple, Optional
from urllib.parse import urlparse

def validate_github_url(url: str) -> Tuple[str, str]:
    """
    Validate GitHub URL and extract owner/repo
    
    Supports:
    - https://github.com/owner/repo
    - https://github.com/owner/repo.git
    - git@github.com:owner/repo.git
    
    Returns:
        Tuple[str, str]: (owner, repo_name)
        
    Raises:
        ValueError: Invalid GitHub URL
    """

def is_valid_repo_name(name: str) -> bool:
    """Check if repository name is valid"""

def sanitize_path(path: str) -> str:
    """Sanitize file path to prevent traversal attacks"""
```

## 🔐 Security Considerations

### 1. URL Validation
```python
# Whitelist GitHub domains only
ALLOWED_DOMAINS = ['github.com', 'www.github.com']

def validate_github_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc in ALLOWED_DOMAINS
```

### 2. Path Traversal Prevention
```python
def sanitize_path(path: str) -> str:
    # Remove .. and absolute paths
    path = os.path.normpath(path)
    if path.startswith('..') or os.path.isabs(path):
        raise ValueError("Invalid path")
    return path
```

### 3. Size Limits
```python
MAX_REPO_SIZE_MB = 500
MAX_FILE_SIZE_MB = 10
MAX_FILES = 10000
```

### 4. Rate Limiting
```python
# Limit cloning operations
@limiter.limit("5/minute")
async def clone_repository(...):
    pass
```

## 🧪 Testing Strategy

### Unit Tests (`tests/test_services/test_cloner.py`)

```python
import pytest
from app.services.github.cloner import RepositoryCloner

@pytest.mark.asyncio
async def test_validate_github_url():
    """Test GitHub URL validation"""

@pytest.mark.asyncio
async def test_clone_repository_success():
    """Test successful repository cloning"""

@pytest.mark.asyncio
async def test_clone_repository_too_large():
    """Test rejection of oversized repositories"""

@pytest.mark.asyncio
async def test_clone_invalid_url():
    """Test handling of invalid URLs"""
```

### Integration Tests (`tests/test_api/test_repositories.py`)

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_clone_endpoint(client: AsyncClient):
    """Test /repositories/clone endpoint"""

@pytest.mark.asyncio
async def test_get_repository(client: AsyncClient):
    """Test /repositories/{id} endpoint"""

@pytest.mark.asyncio
async def test_list_repositories(client: AsyncClient):
    """Test /repositories endpoint"""
```

## 📈 Performance Optimization

### 1. Async Operations
- Use `asyncio` for I/O operations
- Parallel file reading with `asyncio.gather()`
- Background tasks for parsing

### 2. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_file_language(extension: str) -> str:
    """Cache language detection"""
```

### 3. Streaming
```python
async def stream_file_content(file_path: str):
    """Stream large files in chunks"""
    async with aiofiles.open(file_path, 'r') as f:
        while chunk := await f.read(8192):
            yield chunk
```

## 📝 Implementation Checklist

### Phase 1: Foundation (2-3 hours)
- [x] Review architecture and requirements
- [ ] Create backend folder structure
- [ ] Set up virtual environment
- [ ] Install dependencies
- [ ] Create configuration files (.env, config.py)
- [ ] Implement custom exceptions
- [ ] Set up logging

### Phase 2: Utilities (1-2 hours)
- [ ] Implement file_utils.py
- [ ] Implement git_utils.py
- [ ] Implement validators.py
- [ ] Write unit tests for utilities

### Phase 3: GitHub Services (3-4 hours)
- [ ] Implement RepositoryCloner class
- [ ] Implement CodeParser class
- [ ] Implement MetadataExtractor class
- [ ] Write unit tests for services

### Phase 4: Data Models (1 hour)
- [ ] Create Repository model
- [ ] Create API schemas
- [ ] Add validation rules

### Phase 5: API Endpoints (2-3 hours)
- [ ] Implement clone endpoint
- [ ] Implement get repository endpoint
- [ ] Implement list repositories endpoint
- [ ] Implement delete repository endpoint
- [ ] Add dependency injection
- [ ] Write integration tests

### Phase 6: Testing & Polish (2-3 hours)
- [ ] Run all tests
- [ ] Fix bugs
- [ ] Add error handling
- [ ] Optimize performance
- [ ] Add API documentation
- [ ] Create usage examples

**Total Estimated Time: 11-16 hours**

## 🚀 Deployment Considerations

### Environment Variables
```env
# Required
API_KEY=your_secure_api_key
OPENAI_API_KEY=sk-xxx

# Optional
GITHUB_TOKEN=ghp_xxx
MAX_REPO_SIZE_MB=500
STORAGE_PATH=./app/storage
```

### Render Configuration (`render.yaml`)
```yaml
services:
  - type: web
    name: legacymind-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: API_KEY
        sync: false
      - key: OPENAI_API_KEY
        sync: false
    disk:
      name: storage
      mountPath: /opt/render/project/src/app/storage
      sizeGB: 10
```

## 📚 Usage Examples

### Example 1: Clone Repository
```bash
curl -X POST http://localhost:8000/api/v1/repositories/clone \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"url": "https://github.com/facebook/react"}'
```

Response:
```json
{
  "repo_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "cloning",
  "message": "Repository cloning started"
}
```

### Example 2: Get Repository Details
```bash
curl http://localhost:8000/api/v1/repositories/550e8400-e29b-41d4-a716-446655440000 \
  -H "X-API-Key: your_api_key"
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "url": "https://github.com/facebook/react",
  "owner": "facebook",
  "name": "react",
  "status": "ready",
  "metadata": {
    "stars": 220000,
    "language": "JavaScript",
    "description": "A declarative, efficient, and flexible JavaScript library"
  },
  "parsed_data": {
    "total_files": 1523,
    "total_lines": 145230,
    "languages": [
      {"language": "JavaScript", "file_count": 1200, "percentage": 78.8},
      {"language": "TypeScript", "file_count": 323, "percentage": 21.2}
    ]
  }
}
```

### Example 3: List Repositories
```bash
curl "http://localhost:8000/api/v1/repositories?limit=10&offset=0" \
  -H "X-API-Key: your_api_key"
```

## 🎯 Success Criteria

### Functional
- ✅ Successfully clone GitHub repositories
- ✅ Parse Python, JavaScript, TypeScript, Java, C# files
- ✅ Ignore node_modules and binary files
- ✅ Extract file content and metadata
- ✅ Handle errors gracefully

### Performance
- ✅ Clone medium repos (< 100MB) in < 10 seconds
- ✅ Parse 1000 files in < 5 seconds
- ✅ API response time < 200ms (excluding cloning)

### Security
- ✅ Validate all GitHub URLs
- ✅ Prevent path traversal attacks
- ✅ Enforce size limits
- ✅ API key authentication

## 🔄 Next Steps

1. **Review this plan** - Ensure all requirements are covered
2. **Approve approach** - Confirm architecture decisions
3. **Switch to Code mode** - Begin implementation
4. **Start with Phase 1** - Set up foundation
5. **Iterate through phases** - Build incrementally
6. **Test continuously** - Verify each component
7. **Deploy and integrate** - Connect with frontend

## 📞 Questions to Consider

Before implementation, please confirm:

1. **Storage Strategy**: Should we store repository metadata in JSON files or add a database?
2. **Background Processing**: Should parsing happen synchronously or as a background task?
3. **Caching**: Should we cache GitHub API responses? For how long?
4. **Cleanup**: How long should cloned repositories be kept before cleanup?
5. **Rate Limiting**: What rate limits should we apply to the clone endpoint?

---

**Ready to proceed with implementation! 🚀**

This plan provides a complete roadmap for building the GitHub service layer that integrates seamlessly with your LegacyMind AI architecture.