# Dashboard Architecture Diagram

## 🏗️ Component Hierarchy

```mermaid
graph TB
    A[Dashboard Page /dashboard/repoId] --> B[DashboardLayout]
    B --> C[DashboardHeader]
    B --> D[TabNavigation]
    B --> E[MainContent]
    B --> F[ChatbotPanel]
    
    C --> C1[RepoInfo]
    C --> C2[ActionButtons]
    
    D --> D1[Tab: Summary]
    D --> D2[Tab: Architecture]
    D --> D3[Tab: Dependencies]
    D --> D4[Tab: Risks]
    D --> D5[Tab: Modernization]
    
    E --> E1{Active Tab}
    E1 -->|Summary| G[SummaryTab]
    E1 -->|Architecture| H[ArchitectureTab]
    E1 -->|Dependencies| I[DependenciesTab]
    E1 -->|Risks| J[RisksTab]
    E1 -->|Modernization| K[ModernizationTab]
    
    G --> G1[RepoStatsCards]
    G --> G2[OverviewSection]
    G --> G3[QuickInsights]
    
    H --> H1[ArchitectureFlow]
    H --> H2[NodeDetailsPanel]
    H --> H3[FlowControls]
    
    I --> I1[DependencyMetrics]
    I --> I2[OutdatedPackages]
    I --> I3[VulnerabilityAlerts]
    
    J --> J1[RiskMatrix]
    J --> J2[TechnicalDebtScore]
    J --> J3[RiskBreakdown]
    
    K --> K1[SuggestionCards]
    K --> K2[PriorityMatrix]
    K --> K3[ActionableSteps]
    
    F --> F1[ChatHeader]
    F --> F2[MessageList]
    F --> F3[MessageInput]
    
    style A fill:#667eea,stroke:#764ba2,stroke-width:3px,color:#fff
    style B fill:#1e293b,stroke:#334155,stroke-width:2px,color:#fff
    style E fill:#1e293b,stroke:#334155,stroke-width:2px,color:#fff
    style F fill:#1e293b,stroke:#334155,stroke-width:2px,color:#fff
```

## 📊 Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Dashboard
    participant API
    participant Backend
    
    User->>Dashboard: Navigate to /dashboard/repoId
    Dashboard->>API: useRepository(repoId)
    API->>Backend: GET /api/repositories/:id
    Backend-->>API: Repository data
    API-->>Dashboard: Repository state
    
    Dashboard->>API: useAnalysis(repoId)
    API->>Backend: GET /api/repositories/:id/analysis
    Backend-->>API: Analysis results
    API-->>Dashboard: Analysis state
    
    User->>Dashboard: Click Architecture tab
    Dashboard->>API: useArchitecture(repoId)
    API->>Backend: GET /api/repositories/:id/architecture
    Backend-->>API: Architecture data
    API-->>Dashboard: Architecture state
    Dashboard->>Dashboard: Render React Flow graph
    
    User->>Dashboard: Send chat message
    Dashboard->>API: useChatMutation(message)
    API->>Backend: POST /api/repositories/:id/chat
    Backend-->>API: AI response
    API-->>Dashboard: Update chat history
```

## 🎨 Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ Dashboard Header                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Repo Name | Owner | Stars | Language        [Actions]       │ │
│ └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ Tab Navigation                                                   │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ [Summary] [Architecture] [Dependencies] [Risks] [Modernize] │ │
│ └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Main Content Area                    │ Chatbot Panel           │
│ ┌──────────────────────────────────┐ │ ┌────────────────────┐ │
│ │                                  │ │ │ Chat Header        │ │
│ │                                  │ │ ├────────────────────┤ │
│ │                                  │ │ │                    │ │
│ │   Active Tab Content             │ │ │  Message History   │ │
│ │   (Summary/Architecture/etc)     │ │ │                    │ │
│ │                                  │ │ │                    │ │
│ │                                  │ │ ├────────────────────┤ │
│ │                                  │ │ │ Message Input      │ │
│ └──────────────────────────────────┘ │ └────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 State Management

```mermaid
graph LR
    A[URL Params] --> B[repoId]
    B --> C[React Query]
    C --> D[useRepository]
    C --> E[useAnalysis]
    C --> F[useArchitecture]
    C --> G[useDependencies]
    C --> H[useRisks]
    C --> I[useModernization]
    
    J[Local State] --> K[activeTab]
    J --> L[chatOpen]
    J --> M[selectedNode]
    
    D --> N[Repository Data]
    E --> N
    F --> N
    G --> N
    H --> N
    I --> N
    
    K --> O[Tab Content]
    L --> P[Chatbot Panel]
    M --> Q[Node Details]
    
    style C fill:#4facfe,stroke:#00f2fe,stroke-width:2px,color:#fff
    style J fill:#43e97b,stroke:#38f9d7,stroke-width:2px,color:#fff
```

## 🎯 Component Interaction Flow

```mermaid
graph TD
    A[User Action] --> B{Action Type}
    
    B -->|Tab Click| C[Update activeTab state]
    C --> D[Animate tab transition]
    D --> E[Render new tab content]
    E --> F[Fetch tab-specific data]
    
    B -->|Node Click| G[Update selectedNode state]
    G --> H[Show NodeDetailsPanel]
    H --> I[Highlight node in graph]
    
    B -->|Chat Toggle| J[Toggle chatOpen state]
    J --> K[Animate panel slide]
    K --> L[Show/hide chat interface]
    
    B -->|Send Message| M[Call useChatMutation]
    M --> N[Show typing indicator]
    N --> O[Receive AI response]
    O --> P[Update message list]
    P --> Q[Auto-scroll to bottom]
    
    B -->|Filter/Search| R[Update filter state]
    R --> S[Re-render filtered list]
    
    style A fill:#667eea,stroke:#764ba2,stroke-width:2px,color:#fff
    style B fill:#f093fb,stroke:#f5576c,stroke-width:2px,color:#fff
```

## 📱 Responsive Behavior

```mermaid
graph LR
    A[Screen Size] --> B{Breakpoint}
    
    B -->|Mobile < 640px| C[Stack Layout]
    C --> C1[Full width tabs]
    C --> C2[Chatbot as overlay]
    C --> C3[Single column cards]
    
    B -->|Tablet 640-1024px| D[Hybrid Layout]
    D --> D1[Scrollable tabs]
    D --> D2[Chatbot as drawer]
    D --> D3[Two column cards]
    
    B -->|Desktop > 1024px| E[Full Layout]
    E --> E1[All tabs visible]
    E --> E2[Chatbot side panel]
    E --> E3[Three column cards]
    
    style A fill:#667eea,stroke:#764ba2,stroke-width:2px,color:#fff
    style C fill:#43e97b,stroke:#38f9d7,stroke-width:2px,color:#fff
    style D fill:#f5a623,stroke:#f5576c,stroke-width:2px,color:#fff
    style E fill:#4facfe,stroke:#00f2fe,stroke-width:2px,color:#fff
```

## 🎬 Animation Timeline

```mermaid
gantt
    title Dashboard Load Animation Sequence
    dateFormat X
    axisFormat %L ms
    
    section Initial Load
    Page mount           :0, 0
    Fade in layout       :0, 300
    
    section Header
    Header slide in      :100, 400
    Repo info appear     :200, 500
    
    section Tabs
    Tabs fade in         :300, 600
    Active tab highlight :400, 700
    
    section Content
    Content container    :500, 800
    Stats cards stagger  :600, 1200
    Card 1               :600, 1000
    Card 2               :700, 1100
    Card 3               :800, 1200
    Card 4               :900, 1300
    
    section Chatbot
    Chat panel ready     :1000, 1300
```

## 🔌 API Hook Dependencies

```mermaid
graph TB
    A[Dashboard Page] --> B[useRepository]
    A --> C[useAnalysis]
    
    B --> D[Repository Data]
    C --> E[Analysis Status]
    
    D --> F{Analysis Complete?}
    E --> F
    
    F -->|Yes| G[Enable Tab Data Hooks]
    F -->|No| H[Show Loading State]
    
    G --> I[useArchitecture]
    G --> J[useDependencies]
    G --> K[useRisks]
    G --> L[useModernization]
    G --> M[useChat]
    
    I --> N[Architecture Tab]
    J --> O[Dependencies Tab]
    K --> P[Risks Tab]
    L --> Q[Modernization Tab]
    M --> R[Chatbot Panel]
    
    style A fill:#667eea,stroke:#764ba2,stroke-width:3px,color:#fff
    style F fill:#f5a623,stroke:#f5576c,stroke-width:2px,color:#fff
    style G fill:#43e97b,stroke:#38f9d7,stroke-width:2px,color:#fff
```

## 📦 Component Dependencies

```mermaid
graph LR
    A[UI Components] --> B[Card]
    A --> C[Button]
    A --> D[Badge]
    A --> E[Input]
    A --> F[Tabs]
    A --> G[Skeleton]
    A --> H[Progress]
    
    I[Animation Components] --> J[FadeIn]
    I --> K[SlideIn]
    I --> L[ScaleIn]
    I --> M[StaggerContainer]
    
    N[Feature Components] --> O[Dashboard]
    N --> P[Summary]
    N --> Q[Architecture]
    N --> R[Dependencies]
    N --> S[Risks]
    N --> T[Modernization]
    N --> U[Chat]
    
    O --> A
    O --> I
    P --> A
    P --> I
    Q --> A
    Q --> I
    Q --> V[React Flow]
    R --> A
    R --> I
    S --> A
    S --> I
    T --> A
    T --> I
    U --> A
    U --> I
    
    style A fill:#4facfe,stroke:#00f2fe,stroke-width:2px,color:#fff
    style I fill:#43e97b,stroke:#38f9d7,stroke-width:2px,color:#fff
    style N fill:#667eea,stroke:#764ba2,stroke-width:2px,color:#fff
```

---

This architecture provides a clear visual representation of how all components interact and flow together in the dashboard.