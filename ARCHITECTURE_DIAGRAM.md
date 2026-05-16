# LegacyMind AI - Architecture Diagrams

## High-Level System Architecture

```mermaid
graph TB
    subgraph Client["🌐 Client (Browser)"]
        UI[Next.js 15 App]
    end
    
    subgraph Frontend["⚛️ Frontend Layer"]
        Pages[Pages/Routes]
        Components[UI Components]
        API_Client[API Client]
        State[State Management]
    end
    
    subgraph Backend["🐍 Backend Layer"]
        FastAPI[FastAPI Server]
        Routes[API Routes]
        Services[Business Services]
        AI[AI Services]
    end
    
    subgraph Data["💾 Data Layer"]
        VectorDB[(FAISS Vector Store)]
        FileSystem[(File System)]
        Cache[(Cache)]
    end
    
    subgraph External["🌍 External Services"]
        GitHub[GitHub API]
        OpenAI[OpenAI API]
        Models[HuggingFace Models]
    end
    
    UI --> Pages
    Pages --> Components
    Components --> API_Client
    API_Client --> State
    
    API_Client -->|HTTP/REST| FastAPI
    FastAPI --> Routes
    Routes --> Services
    Services --> AI
    
    Services --> VectorDB
    Services --> FileSystem
    Services --> Cache
    
    Services -->|Clone Repos| GitHub
    AI -->|LLM Calls| OpenAI
    AI -->|Embeddings| Models
    
    style Client fill:#1a1a2e
    style Frontend fill:#16213e
    style Backend fill:#0f3460
    style Data fill:#533483
    style External fill:#e94560
```

## Component Architecture

```mermaid
graph LR
    subgraph Frontend Components
        A[Landing Page] --> B[Hero Section]
        A --> C[Features Section]
        A --> D[CTA Section]
        
        E[Dashboard] --> F[Repo Input]
        E --> G[Analysis View]
        E --> H[Architecture View]
        E --> I[Chat View]
        
        G --> J[Summary Card]
        G --> K[Dependencies Card]
        G --> L[Risks Card]
        G --> M[Modernization Card]
        
        H --> N[React Flow Graph]
        H --> O[Node Details]
        
        I --> P[Message List]
        I --> Q[Message Input]
        I --> R[Code Snippets]
    end
    
    style A fill:#667eea
    style E fill:#764ba2
    style G fill:#f093fb
    style H fill:#4facfe
    style I fill:#00f2fe
```

## Backend Service Architecture

```mermaid
graph TB
    subgraph API Layer
        A[FastAPI App] --> B[Health Endpoint]
        A --> C[Repository Endpoints]
        A --> D[Analysis Endpoints]
        A --> E[Chat Endpoints]
    end
    
    subgraph Service Layer
        F[GitHub Service]
        G[Analysis Service]
        H[Embedding Service]
        I[AI Service]
    end
    
    subgraph GitHub Service
        F --> J[Cloner]
        F --> K[Parser]
        F --> L[Analyzer]
    end
    
    subgraph Analysis Service
        G --> M[Code Analyzer]
        G --> N[Dependency Analyzer]
        G --> O[Risk Analyzer]
        G --> P[Architecture Analyzer]
        G --> Q[Modernization]
    end
    
    subgraph Embedding Service
        H --> R[Chunker]
        H --> S[Generator]
        H --> T[Indexer]
    end
    
    subgraph AI Service
        I --> U[LangGraph Workflow]
        I --> V[RAG Chain]
        I --> W[Agents]
    end
    
    C --> F
    D --> G
    D --> I
    E --> I
    
    G --> H
    I --> H
    
    style A fill:#667eea
    style F fill:#764ba2
    style G fill:#f093fb
    style H fill:#4facfe
    style I fill:#00f2fe
```

## Data Flow: Repository Analysis

```mermaid
sequenceDiagram
    actor User
    participant UI as Frontend
    participant API as FastAPI
    participant GH as GitHub Service
    participant Parser as Code Parser
    participant Embed as Embedding Service
    participant FAISS as Vector Store
    participant AI as AI Service
    participant LLM as OpenAI
    
    User->>UI: Enter GitHub URL
    UI->>API: POST /repositories/clone
    
    API->>GH: Clone repository
    GH->>GH: Validate URL
    GH->>GH: Git clone
    GH-->>API: Repository path
    
    API->>Parser: Parse code files
    Parser->>Parser: Traverse files
    Parser->>Parser: Extract structure
    Parser-->>API: Parsed data
    
    API->>Embed: Generate embeddings
    Embed->>Embed: Chunk code
    Embed->>Embed: Generate vectors
    Embed->>FAISS: Store embeddings
    FAISS-->>Embed: Index created
    Embed-->>API: Embeddings ready
    
    API->>AI: Analyze repository
    AI->>AI: Run LangGraph workflow
    AI->>LLM: Generate summary
    LLM-->>AI: AI summary
    AI->>LLM: Analyze architecture
    LLM-->>AI: Architecture insights
    AI->>LLM: Assess risks
    LLM-->>AI: Risk analysis
    AI-->>API: Complete analysis
    
    API-->>UI: Analysis results
    UI-->>User: Display dashboard
```

## Data Flow: AI Chat

```mermaid
sequenceDiagram
    actor User
    participant UI as Chat Interface
    participant API as FastAPI
    participant FAISS as Vector Store
    participant RAG as RAG Chain
    participant LLM as OpenAI
    
    User->>UI: Ask question
    UI->>API: POST /chat
    
    API->>FAISS: Search similar code
    FAISS->>FAISS: Vector similarity search
    FAISS-->>API: Top K chunks
    
    API->>RAG: Create context
    RAG->>RAG: Format prompt
    RAG->>LLM: Generate response
    
    LLM-->>RAG: Stream tokens
    RAG-->>API: Stream response
    API-->>UI: Stream to client
    UI-->>User: Display answer
    
    Note over UI,User: Real-time streaming
```

## LangGraph Workflow

```mermaid
graph TB
    Start([Start]) --> Clone[Clone Repository]
    Clone --> Parse[Parse Code Files]
    Parse --> Embed[Generate Embeddings]
    Embed --> Structure[Analyze Structure]
    
    Structure --> Dependencies[Analyze Dependencies]
    Dependencies --> Risks[Assess Risks]
    Risks --> Architecture[Detect Architecture]
    Architecture --> Modernization[Generate Suggestions]
    
    Modernization --> Summary[Create Summary]
    Summary --> End([End])
    
    style Start fill:#667eea
    style Clone fill:#764ba2
    style Parse fill:#f093fb
    style Embed fill:#4facfe
    style Structure fill:#00f2fe
    style Dependencies fill:#43e97b
    style Risks fill:#fa709a
    style Architecture fill:#fee140
    style Modernization fill:#30cfd0
    style Summary fill:#a8edea
    style End fill:#667eea
```

## Technology Stack Layers

```mermaid
graph TB
    subgraph Presentation["🎨 Presentation Layer"]
        A1[Next.js 15]
        A2[React 18]
        A3[TypeScript]
        A4[Tailwind CSS]
        A5[Framer Motion]
    end
    
    subgraph Application["⚙️ Application Layer"]
        B1[FastAPI]
        B2[Pydantic]
        B3[Python 3.11+]
    end
    
    subgraph Business["💼 Business Logic Layer"]
        C1[LangGraph]
        C2[LangChain]
        C3[Custom Services]
    end
    
    subgraph Data["💾 Data Layer"]
        D1[FAISS]
        D2[File System]
        D3[Cache]
    end
    
    subgraph AI["🤖 AI/ML Layer"]
        E1[OpenAI GPT-4]
        E2[sentence-transformers]
        E3[HuggingFace]
    end
    
    subgraph Infrastructure["🏗️ Infrastructure"]
        F1[Vercel]
        F2[Render]
        F3[GitHub]
    end
    
    A1 --> B1
    B1 --> C1
    C1 --> D1
    C1 --> E1
    B1 --> F2
    A1 --> F1
    
    style Presentation fill:#667eea
    style Application fill:#764ba2
    style Business fill:#f093fb
    style Data fill:#4facfe
    style AI fill:#00f2fe
    style Infrastructure fill:#43e97b
```

## Deployment Architecture

```mermaid
graph TB
    subgraph Internet["🌐 Internet"]
        Users[Users]
    end
    
    subgraph Vercel["☁️ Vercel (Frontend)"]
        NextJS[Next.js App]
        Edge[Edge Functions]
        CDN[Global CDN]
    end
    
    subgraph Render["☁️ Render (Backend)"]
        API[FastAPI Server]
        Worker[Background Workers]
        Storage[Persistent Storage]
    end
    
    subgraph External["🔌 External APIs"]
        GitHub[GitHub API]
        OpenAI[OpenAI API]
        HF[HuggingFace]
    end
    
    Users --> CDN
    CDN --> NextJS
    NextJS --> Edge
    Edge --> API
    
    API --> Worker
    API --> Storage
    
    API --> GitHub
    API --> OpenAI
    API --> HF
    
    style Internet fill:#1a1a2e
    style Vercel fill:#667eea
    style Render fill:#764ba2
    style External fill:#f093fb
```

## File Structure Visualization

```
LegacyMind-AI/
│
├── 📁 frontend/                    # Next.js 15 Application
│   ├── 📁 src/
│   │   ├── 📁 app/                # App Router
│   │   │   ├── 📄 page.tsx        # Landing page
│   │   │   ├── 📄 layout.tsx      # Root layout
│   │   │   └── 📁 (dashboard)/    # Dashboard routes
│   │   │
│   │   ├── 📁 components/         # React Components
│   │   │   ├── 📁 ui/            # Base components
│   │   │   ├── 📁 features/      # Feature components
│   │   │   └── 📁 layout/        # Layout components
│   │   │
│   │   ├── 📁 lib/               # Utilities
│   │   │   ├── 📁 api/           # API client
│   │   │   ├── 📁 hooks/         # Custom hooks
│   │   │   └── 📁 utils/         # Helper functions
│   │   │
│   │   └── 📁 types/             # TypeScript types
│   │
│   └── 📄 package.json
│
└── 📁 backend/                     # FastAPI Application
    ├── 📁 app/
    │   ├── 📄 main.py             # FastAPI entry
    │   │
    │   ├── 📁 api/                # API routes
    │   │   └── 📁 v1/
    │   │       └── 📁 endpoints/
    │   │
    │   ├── 📁 services/           # Business logic
    │   │   ├── 📁 github/        # GitHub integration
    │   │   ├── 📁 analysis/      # Code analysis
    │   │   ├── 📁 embeddings/    # Vector embeddings
    │   │   ├── 📁 ai/            # AI services
    │   │   └── 📁 vector_store/  # FAISS operations
    │   │
    │   ├── 📁 models/            # Data models
    │   ├── 📁 core/              # Configuration
    │   └── 📁 utils/             # Utilities
    │
    └── 📄 requirements.txt
```

## Security Architecture

```mermaid
graph TB
    subgraph Client
        A[User Browser]
    end
    
    subgraph Frontend
        B[Next.js App]
        C[Environment Variables]
    end
    
    subgraph Backend
        D[FastAPI]
        E[API Key Validation]
        F[Rate Limiting]
        G[Input Sanitization]
    end
    
    subgraph Secrets
        H[GitHub Token]
        I[OpenAI API Key]
        J[Environment Secrets]
    end
    
    A -->|HTTPS| B
    B -->|HTTPS| D
    D --> E
    E --> F
    F --> G
    
    D -.->|Secure Access| H
    D -.->|Secure Access| I
    D -.->|Secure Access| J
    
    style A fill:#667eea
    style B fill:#764ba2
    style D fill:#f093fb
    style E fill:#4facfe
    style F fill:#00f2fe
    style G fill:#43e97b
    style H fill:#fa709a
    style I fill:#fee140
    style J fill:#30cfd0
```

## Performance Optimization Strategy

```mermaid
graph LR
    subgraph Frontend Optimizations
        A1[Code Splitting]
        A2[Lazy Loading]
        A3[Image Optimization]
        A4[Caching]
        A5[Memoization]
    end
    
    subgraph Backend Optimizations
        B1[Async Operations]
        B2[Batch Processing]
        B3[Connection Pooling]
        B4[Response Caching]
        B5[Streaming]
    end
    
    subgraph AI Optimizations
        C1[Embedding Cache]
        C2[Vector Index]
        C3[Prompt Optimization]
        C4[Model Selection]
    end
    
    A1 --> Performance[⚡ Fast Performance]
    A2 --> Performance
    A3 --> Performance
    A4 --> Performance
    A5 --> Performance
    
    B1 --> Performance
    B2 --> Performance
    B3 --> Performance
    B4 --> Performance
    B5 --> Performance
    
    C1 --> Performance
    C2 --> Performance
    C3 --> Performance
    C4 --> Performance
    
    style Performance fill:#43e97b
```

## Conclusion

These diagrams provide a comprehensive visual overview of the LegacyMind AI architecture, showing:

1. **System Architecture**: High-level component interaction
2. **Component Structure**: Frontend and backend organization
3. **Data Flows**: How data moves through the system
4. **LangGraph Workflow**: AI analysis pipeline
5. **Technology Stack**: Layered architecture
6. **Deployment**: Cloud infrastructure
7. **Security**: Protection mechanisms
8. **Performance**: Optimization strategies

This architecture is designed for:
- ✅ Scalability
- ✅ Maintainability
- ✅ Performance
- ✅ Security
- ✅ Developer Experience