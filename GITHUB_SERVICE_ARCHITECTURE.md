# GitHub Service Layer - Architecture Diagram

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[Frontend Application]
        B[API Client]
    end
    
    subgraph "API Layer"
        C[FastAPI Application]
        D[API Router v1]
        E[Repository Endpoints]
        F[Authentication Middleware]
    end
    
    subgraph "Service Layer"
        G[Repository Cloner]
        H[Code Parser]
        I[Metadata Extractor]
        J[Repository Manager]
    end
    
    subgraph "Utility Layer"
        K[File Utils]
        L[Git Utils]
        M[Validators]
    end
    
    subgraph "External Services"
        N[GitHub API]
        O[Git Repository]
    end
    
    subgraph "Storage Layer"
        P[File System]
        Q[Cloned Repositories]
        R[Metadata JSON]
    end
    
    A --> B
    B --> C
    C --> F
    F --> D
    D --> E
    E --> G
    E --> H
    E --> I
    E --> J
    G --> K
    G --> L
    G --> M
    H --> K
    I --> N
    G --> O
    J --> P
    P --> Q
    P --> R
```

## 🔄 Repository Cloning Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Cloner
    participant Parser
    participant Metadata
    participant GitHub
    participant Storage
    
    Client->>API: POST /repositories/clone
    API->>API: Validate API Key
    API->>Cloner: validate_github_url(url)
    Cloner->>GitHub: Check repo size
    GitHub-->>Cloner: Size info
    
    alt Repo too large
        Cloner-->>API: RepositoryTooLargeError
        API-->>Client: 400 Bad Request
    else Size OK
        Cloner->>Cloner: Generate repo_id
        API-->>Client: 202 Accepted {repo_id, status: cloning}
        
        Note over API,Storage: Background Tasks Start
        
        Cloner->>GitHub: git clone
        GitHub-->>Cloner: Repository files
        Cloner->>Storage: Save to /repositories/{repo_id}
        
        par Parse Code
            Parser->>Storage: Scan directory
            Parser->>Parser: Filter files
            Parser->>Parser: Extract content
            Parser->>Storage: Save parsed data
        and Extract Metadata
            Metadata->>GitHub: Fetch metadata
            GitHub-->>Metadata: Repo info
            Metadata->>Storage: Save metadata
        end
        
        Cloner->>Storage: Update status: ready
    end
```

## 📁 File Structure Flow

```mermaid
graph LR
    A[Repository URL] --> B[Clone Repository]
    B --> C[Local Directory]
    C --> D{Scan Files}
    D --> E{Check Extension}
    E -->|.py .js .ts .java .cs| F[Supported]
    E -->|Other| G[Skip]
    F --> H{Check Path}
    H -->|node_modules| I[Ignore]
    H -->|__pycache__| I
    H -->|.git| I
    H -->|Valid Path| J{Check Binary}
    J -->|Binary| K[Skip]
    J -->|Text| L[Extract Content]
    L --> M[Parse Metadata]
    M --> N[Store Results]
```

## 🎯 Component Responsibilities

### 1. Repository Cloner
```
┌─────────────────────────────────┐
│   Repository Cloner             │
├─────────────────────────────────┤
│ • Validate GitHub URLs          │
│ • Check repository size         │
│ • Clone using GitPython         │
│ • Generate unique repo IDs      │
│ • Manage storage directories    │
│ • Cleanup old repositories      │
└─────────────────────────────────┘
```

### 2. Code Parser
```
┌─────────────────────────────────┐
│   Code Parser                   │
├─────────────────────────────────┤
│ • Recursive directory scanning  │
│ • File type detection           │
│ • Binary file filtering         │
│ • Content extraction            │
│ • Line counting                 │
│ • Language statistics           │
│ • Dependency parsing            │
└─────────────────────────────────┘
```

### 3. Metadata Extractor
```
┌─────────────────────────────────┐
│   Metadata Extractor            │
├─────────────────────────────────┤
│ • GitHub API integration        │
│ • Repository statistics         │
│ • Language breakdown            │
│ • Contributor information       │
│ • License detection             │
│ • Topic extraction              │
└─────────────────────────────────┘
```

## 🔐 Security Architecture

```mermaid
graph TB
    A[Incoming Request] --> B{API Key Valid?}
    B -->|No| C[403 Forbidden]
    B -->|Yes| D{GitHub URL Valid?}
    D -->|No| E[400 Bad Request]
    D -->|Yes| F{Repo Size OK?}
    F -->|No| G[413 Payload Too Large]
    F -->|Yes| H{Path Safe?}
    H -->|No| I[400 Bad Request]
    H -->|Yes| J[Process Request]
    J --> K{Clone Success?}
    K -->|No| L[500 Internal Error]
    K -->|Yes| M[200 OK]
```

## 📊 Data Flow

```mermaid
graph LR
    subgraph "Input"
        A[GitHub URL]
    end
    
    subgraph "Processing"
        B[Validate URL]
        C[Clone Repo]
        D[Scan Files]
        E[Parse Content]
        F[Extract Metadata]
    end
    
    subgraph "Storage"
        G[File System]
        H[Repository Files]
        I[Parsed Data JSON]
        J[Metadata JSON]
    end
    
    subgraph "Output"
        K[API Response]
        L[Repository Object]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    C --> F
    E --> G
    F --> G
    G --> H
    G --> I
    G --> J
    H --> K
    I --> K
    J --> K
    K --> L
```

## 🗂️ Storage Structure

```
app/storage/
├── repositories/
│   ├── {repo_id_1}/
│   │   ├── .git/
│   │   ├── src/
│   │   ├── package.json
│   │   └── README.md
│   ├── {repo_id_2}/
│   │   └── ...
│   └── metadata/
│       ├── {repo_id_1}.json
│       └── {repo_id_2}.json
├── cache/
│   └── github_api/
│       └── {owner}_{repo}.json
└── logs/
    └── cloning.log
```

## 🔄 State Machine

```mermaid
stateDiagram-v2
    [*] --> Pending: Create Request
    Pending --> Cloning: Start Clone
    Cloning --> Cloned: Clone Complete
    Cloning --> Error: Clone Failed
    Cloned --> Parsing: Start Parse
    Parsing --> Ready: Parse Complete
    Parsing --> Error: Parse Failed
    Ready --> [*]: Success
    Error --> [*]: Failure
    
    note right of Cloning
        Background task
        Git clone operation
    end note
    
    note right of Parsing
        Background task
        File scanning & parsing
    end note
```

## 🎯 API Endpoint Architecture

```
/api/v1/repositories/
├── POST   /clone
│   ├── Validate URL
│   ├── Check size
│   ├── Start clone (background)
│   └── Return repo_id
│
├── GET    /{repo_id}
│   ├── Load from storage
│   ├── Return full details
│   └── Include parsed data
│
├── GET    /
│   ├── List all repos
│   ├── Pagination support
│   └── Filter by status
│
├── DELETE /{repo_id}
│   ├── Remove from storage
│   ├── Delete metadata
│   └── Cleanup files
│
└── GET    /{repo_id}/files
    ├── Filter by language
    ├── Return file list
    └── Include content
```

## 🧩 Module Dependencies

```mermaid
graph TD
    A[main.py] --> B[api/v1/router.py]
    B --> C[endpoints/repositories.py]
    C --> D[services/github/cloner.py]
    C --> E[services/github/parser.py]
    C --> F[services/github/metadata.py]
    D --> G[utils/git_utils.py]
    D --> H[utils/validators.py]
    E --> I[utils/file_utils.py]
    F --> J[PyGithub]
    D --> K[GitPython]
    C --> L[models/repository.py]
    C --> M[models/schemas.py]
    A --> N[core/config.py]
    A --> O[core/security.py]
    C --> O
```

## 🚀 Deployment Architecture

```mermaid
graph TB
    subgraph "Render Platform"
        A[Web Service]
        B[Persistent Disk 10GB]
        C[Environment Variables]
    end
    
    subgraph "Application"
        D[FastAPI App]
        E[Uvicorn Server]
        F[Background Workers]
    end
    
    subgraph "External"
        G[GitHub API]
        H[Git Repositories]
        I[Frontend Vercel]
    end
    
    A --> D
    D --> E
    D --> F
    A --> B
    A --> C
    D --> G
    D --> H
    I --> A
```

## 📈 Performance Considerations

### Async Operations
```python
# Sequential (Slow)
repo = clone_repository(url)      # 10s
data = parse_repository(repo)     # 5s
meta = get_metadata(url)          # 2s
# Total: 17s

# Parallel (Fast)
repo = await clone_repository(url)           # 10s
data, meta = await asyncio.gather(
    parse_repository(repo),                  # 5s
    get_metadata(url)                        # 2s
)
# Total: 12s (30% faster)
```

### Caching Strategy
```mermaid
graph LR
    A[Request] --> B{Cache Hit?}
    B -->|Yes| C[Return Cached]
    B -->|No| D[Fetch from GitHub]
    D --> E[Store in Cache]
    E --> F[Return Fresh]
    C --> G[Response]
    F --> G
```

## 🔍 Error Handling Flow

```mermaid
graph TD
    A[Request] --> B{Validation}
    B -->|Invalid URL| C[400 Bad Request]
    B -->|Valid| D{Size Check}
    D -->|Too Large| E[413 Payload Too Large]
    D -->|OK| F{Clone}
    F -->|Network Error| G[502 Bad Gateway]
    F -->|Auth Error| H[401 Unauthorized]
    F -->|Success| I{Parse}
    I -->|Parse Error| J[500 Internal Error]
    I -->|Success| K[200 OK]
```

## 🎨 Code Organization

```
services/github/
├── __init__.py
│   └── Export main classes
│
├── cloner.py
│   ├── RepositoryCloner
│   │   ├── __init__()
│   │   ├── clone_repository()
│   │   ├── validate_github_url()
│   │   ├── check_repo_size()
│   │   └── cleanup_repository()
│   └── Helper functions
│
├── parser.py
│   ├── CodeParser
│   │   ├── __init__()
│   │   ├── parse_repository()
│   │   ├── scan_directory()
│   │   ├── should_ignore_path()
│   │   ├── is_binary_file()
│   │   └── extract_file_content()
│   └── Constants (SUPPORTED_EXTENSIONS, etc.)
│
└── metadata.py
    ├── MetadataExtractor
    │   ├── __init__()
    │   ├── get_github_metadata()
    │   ├── get_language_stats()
    │   └── extract_local_metadata()
    └── Helper functions
```

## 🧪 Testing Architecture

```mermaid
graph TB
    subgraph "Unit Tests"
        A[test_cloner.py]
        B[test_parser.py]
        C[test_metadata.py]
        D[test_utils.py]
    end
    
    subgraph "Integration Tests"
        E[test_repositories.py]
        F[test_workflow.py]
    end
    
    subgraph "Fixtures"
        G[conftest.py]
        H[Mock GitHub API]
        I[Sample Repos]
    end
    
    A --> G
    B --> G
    C --> G
    D --> G
    E --> G
    F --> G
    G --> H
    G --> I
```

---

This architecture provides:
- ✅ **Clear separation of concerns** - Each component has a single responsibility
- ✅ **Scalable design** - Easy to add new features
- ✅ **Testable structure** - Components can be tested independently
- ✅ **Security-first** - Multiple validation layers
- ✅ **Performance-optimized** - Async operations and caching
- ✅ **Production-ready** - Error handling and monitoring