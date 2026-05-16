# Repository Analysis Dashboard - Implementation Plan

## 🎯 Overview

This document provides a detailed implementation plan for building the LegacyMind AI repository analysis dashboard with a modern, futuristic developer UI.

## 📋 Design Decisions

### Architecture
- **Route**: Single page at `/dashboard/[repoId]`
- **Navigation**: Client-side tab switching (no sub-routes)
- **Chatbot**: Collapsible side panel docked to the right
- **Loading**: Progressive loading - show sections as they complete
- **Graph Detail**: Module-level architecture with adaptive detail based on repo size

### Technology Stack
- **React Flow**: Interactive architecture visualization
- **Framer Motion**: Smooth animations and transitions
- **Tailwind CSS**: Utility-first styling with glassmorphism
- **TypeScript**: Full type safety
- **React Query**: Data fetching and caching

## 🏗️ Component Architecture

```
Dashboard Page (/dashboard/[repoId])
├── DashboardLayout
│   ├── DashboardHeader (repo info, actions)
│   ├── TabNavigation (Summary, Architecture, Dependencies, Risks, Modernization)
│   ├── MainContent (tab-based content)
│   │   ├── SummaryTab
│   │   │   ├── RepoStatsCards (animated cards)
│   │   │   ├── OverviewSection
│   │   │   └── QuickInsights
│   │   ├── ArchitectureTab
│   │   │   ├── ArchitectureFlow (React Flow)
│   │   │   ├── NodeDetailsPanel
│   │   │   └── FlowControls
│   │   ├── DependenciesTab
│   │   │   ├── DependencyMetrics
│   │   │   ├── OutdatedPackages
│   │   │   └── VulnerabilityAlerts
│   │   ├── RisksTab
│   │   │   ├── RiskMatrix
│   │   │   ├── TechnicalDebtScore
│   │   │   └── RiskBreakdown
│   │   └── ModernizationTab
│   │       ├── SuggestionCards
│   │       ├── PriorityMatrix
│   │       └── ActionableSteps
│   └── ChatbotPanel (collapsible, docked right)
│       ├── ChatHeader
│       ├── MessageList
│       ├── MessageInput
│       └── CodeSnippet
```

## 📁 File Structure

```
frontend/src/
├── app/
│   └── dashboard/
│       └── [repoId]/
│           ├── page.tsx                    # Main dashboard page
│           └── layout.tsx                  # Dashboard layout wrapper
│
├── components/
│   ├── ui/
│   │   ├── tabs.tsx                        # Tab navigation component
│   │   ├── skeleton.tsx                    # Loading skeleton
│   │   ├── progress.tsx                    # Progress bar
│   │   ├── dialog.tsx                      # Modal dialog
│   │   └── collapsible.tsx                 # Collapsible panel
│   │
│   ├── animations/
│   │   ├── fade-in.tsx                     # Fade in animation wrapper
│   │   ├── slide-in.tsx                    # Slide in animation wrapper
│   │   ├── scale-in.tsx                    # Scale in animation wrapper
│   │   └── stagger-container.tsx           # Stagger children animation
│   │
│   └── features/
│       ├── dashboard/
│       │   ├── dashboard-layout.tsx        # Main layout with header
│       │   ├── dashboard-header.tsx        # Header with repo info
│       │   └── tab-navigation.tsx          # Tab switcher
│       │
│       ├── summary/
│       │   ├── repo-stats-cards.tsx        # Animated stat cards
│       │   ├── overview-section.tsx        # Repository overview
│       │   └── quick-insights.tsx          # Key insights panel
│       │
│       ├── architecture/
│       │   ├── architecture-flow.tsx       # React Flow graph
│       │   ├── node-details-panel.tsx      # Selected node details
│       │   ├── flow-controls.tsx           # Zoom, fit, layout controls
│       │   └── custom-nodes.tsx            # Custom node components
│       │
│       ├── dependencies/
│       │   ├── dependency-metrics.tsx      # Metrics overview
│       │   ├── outdated-packages.tsx       # Outdated package list
│       │   ├── vulnerability-alerts.tsx    # Security vulnerabilities
│       │   └── dependency-graph.tsx        # Dependency visualization
│       │
│       ├── risks/
│       │   ├── risk-matrix.tsx             # Risk severity matrix
│       │   ├── technical-debt-score.tsx    # Debt score gauge
│       │   ├── risk-breakdown.tsx          # Risk categories
│       │   └── risk-card.tsx               # Individual risk item
│       │
│       ├── modernization/
│       │   ├── suggestion-cards.tsx        # Modernization suggestions
│       │   ├── priority-matrix.tsx         # Priority vs effort matrix
│       │   └── actionable-steps.tsx        # Step-by-step guide
│       │
│       └── chat/
│           ├── chatbot-panel.tsx           # Collapsible chat panel
│           ├── chat-header.tsx             # Chat header with toggle
│           ├── message-list.tsx            # Message history
│           ├── message-bubble.tsx          # Individual message
│           ├── message-input.tsx           # Input with send button
│           └── code-snippet.tsx            # Syntax highlighted code
│
├── lib/
│   ├── hooks/
│   │   ├── use-repository.ts               # Fetch repository data
│   │   ├── use-analysis.ts                 # Fetch analysis results
│   │   ├── use-architecture.ts             # Fetch architecture data
│   │   ├── use-chat.ts                     # Chat functionality
│   │   └── use-tab-state.ts                # Tab state management
│   │
│   └── animations/
│       ├── variants.ts                     # Framer Motion variants
│       └── transitions.ts                  # Transition configs
│
└── types/
    ├── repository.ts                       # Repository types
    ├── analysis.ts                         # Analysis result types
    ├── architecture.ts                     # Architecture graph types
    ├── risk.ts                             # Risk assessment types
    ├── dependency.ts                       # Dependency types
    └── chat.ts                             # Chat message types
```

## 🎨 Design System

### Color Palette
```typescript
// Primary Colors
primary: '#667eea'      // Indigo
secondary: '#764ba2'    // Purple
accent: '#4facfe'       // Cyan

// Status Colors
success: '#43e97b'      // Green
warning: '#f5a623'      // Amber
error: '#f5576c'        // Red
info: '#4facfe'         // Blue

// Neutral Colors
background: '#0f172a'   // Slate 900
surface: '#1e293b'      // Slate 800
border: '#334155'       // Slate 700
text: '#f1f5f9'         // Slate 100
textMuted: '#94a3b8'    // Slate 400
```

### Typography
```typescript
// Font Sizes
xs: '0.75rem'    // 12px
sm: '0.875rem'   // 14px
base: '1rem'     // 16px
lg: '1.125rem'   // 18px
xl: '1.25rem'    // 20px
2xl: '1.5rem'    // 24px
3xl: '1.875rem'  // 30px
4xl: '2.25rem'   // 36px

// Font Weights
normal: 400
medium: 500
semibold: 600
bold: 700
```

### Spacing
```typescript
// Consistent spacing scale
1: '0.25rem'   // 4px
2: '0.5rem'    // 8px
3: '0.75rem'   // 12px
4: '1rem'      // 16px
6: '1.5rem'    // 24px
8: '2rem'      // 32px
12: '3rem'     // 48px
16: '4rem'     // 64px
```

## 📊 Data Types

### Repository Type
```typescript
interface Repository {
  id: string;
  name: string;
  owner: string;
  url: string;
  description: string;
  language: string;
  stars: number;
  forks: number;
  size: number;
  lastUpdated: string;
  analyzedAt: string;
}
```

### Analysis Result Type
```typescript
interface AnalysisResult {
  id: string;
  repositoryId: string;
  status: 'pending' | 'analyzing' | 'completed' | 'failed';
  progress: number;
  summary: {
    totalFiles: number;
    totalLines: number;
    languages: Record<string, number>;
    complexity: 'low' | 'medium' | 'high';
  };
  architecture: ArchitectureData;
  dependencies: DependencyData;
  risks: RiskData;
  modernization: ModernizationData;
}
```

### Architecture Data Type
```typescript
interface ArchitectureData {
  pattern: 'mvc' | 'microservices' | 'monolith' | 'layered' | 'unknown';
  modules: Module[];
  relationships: Relationship[];
  metrics: {
    coupling: number;
    cohesion: number;
    complexity: number;
  };
}

interface Module {
  id: string;
  name: string;
  type: 'component' | 'service' | 'utility' | 'config';
  path: string;
  size: number;
  dependencies: string[];
}

interface Relationship {
  source: string;
  target: string;
  type: 'imports' | 'extends' | 'implements' | 'calls';
  strength: number;
}
```

### Risk Data Type
```typescript
interface RiskData {
  overallScore: number;
  categories: RiskCategory[];
  technicalDebt: {
    score: number;
    estimatedHours: number;
    issues: TechnicalDebtIssue[];
  };
}

interface RiskCategory {
  name: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  count: number;
  items: RiskItem[];
}

interface RiskItem {
  id: string;
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  impact: string;
  recommendation: string;
  files: string[];
}
```

### Dependency Data Type
```typescript
interface DependencyData {
  total: number;
  outdated: number;
  vulnerable: number;
  packages: Package[];
  vulnerabilities: Vulnerability[];
}

interface Package {
  name: string;
  currentVersion: string;
  latestVersion: string;
  isOutdated: boolean;
  updateType: 'major' | 'minor' | 'patch';
}

interface Vulnerability {
  id: string;
  package: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  fixedIn: string;
}
```

### Modernization Data Type
```typescript
interface ModernizationData {
  suggestions: Suggestion[];
  priorityMatrix: PriorityItem[];
  estimatedEffort: string;
}

interface Suggestion {
  id: string;
  category: 'framework' | 'architecture' | 'dependencies' | 'practices';
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  effort: 'low' | 'medium' | 'high';
  impact: string;
  steps: string[];
}
```

### Chat Types
```typescript
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  codeSnippets?: CodeSnippet[];
  references?: FileReference[];
}

interface CodeSnippet {
  language: string;
  code: string;
  file?: string;
  lineStart?: number;
  lineEnd?: number;
}

interface FileReference {
  path: string;
  lineNumber?: number;
}
```

## 🎬 Animation Specifications

### Card Entrance Animation
```typescript
const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: {
      duration: 0.4,
      ease: [0.4, 0, 0.2, 1]
    }
  }
};
```

### Stagger Container
```typescript
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
};
```

### Tab Transition
```typescript
const tabContentVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: { 
    opacity: 1, 
    x: 0,
    transition: {
      duration: 0.3,
      ease: 'easeOut'
    }
  },
  exit: { 
    opacity: 0, 
    x: 20,
    transition: {
      duration: 0.2
    }
  }
};
```

### Chatbot Panel Slide
```typescript
const chatPanelVariants = {
  closed: { 
    x: '100%',
    transition: {
      duration: 0.3,
      ease: [0.4, 0, 0.2, 1]
    }
  },
  open: { 
    x: 0,
    transition: {
      duration: 0.3,
      ease: [0.4, 0, 0.2, 1]
    }
  }
};
```

## 🔧 Component Specifications

### 1. Dashboard Layout
**File**: `components/features/dashboard/dashboard-layout.tsx`

**Features**:
- Responsive grid layout
- Fixed header with repo info
- Tab navigation below header
- Main content area with padding
- Collapsible chatbot panel on right
- Mobile: Stack layout, chatbot as overlay

**Props**:
```typescript
interface DashboardLayoutProps {
  repository: Repository;
  children: React.ReactNode;
}
```

### 2. Tab Navigation
**File**: `components/features/dashboard/tab-navigation.tsx`

**Features**:
- Horizontal tab list with glassmorphism
- Active tab indicator with gradient
- Smooth transition animation
- Icons for each tab
- Mobile: Scrollable horizontal tabs

**Tabs**:
1. Summary (Home icon)
2. Architecture (Network icon)
3. Dependencies (Package icon)
4. Risks (Alert icon)
5. Modernization (Sparkles icon)

### 3. Repository Stats Cards
**File**: `components/features/summary/repo-stats-cards.tsx`

**Features**:
- Grid of 4-6 animated cards
- Each card shows a key metric
- Icon, value, label, trend indicator
- Hover effect with glow
- Stagger animation on mount

**Metrics**:
- Total Files
- Lines of Code
- Code Quality Score
- Technical Debt Hours
- Dependencies Count
- Last Updated

### 4. Architecture Flow
**File**: `components/features/architecture/architecture-flow.tsx`

**Features**:
- React Flow canvas with custom nodes
- Module-level visualization
- Color-coded by type (component, service, utility)
- Edge thickness based on relationship strength
- Zoom, pan, fit view controls
- Node click shows details panel
- Auto-layout with dagre

**Node Types**:
- Component Node (rounded rectangle, blue)
- Service Node (hexagon, purple)
- Utility Node (circle, green)
- Config Node (diamond, orange)

### 5. Risk Matrix
**File**: `components/features/risks/risk-matrix.tsx`

**Features**:
- 2D grid: Severity (Y) vs Impact (X)
- Color-coded quadrants
- Risk items as draggable dots
- Hover shows risk details
- Click opens detailed view
- Legend with counts

**Quadrants**:
- Low/Low: Green
- Low/High: Yellow
- High/Low: Orange
- High/High: Red

### 6. Dependency Metrics
**File**: `components/features/dependencies/dependency-metrics.tsx`

**Features**:
- Overview cards with counts
- Outdated packages list with versions
- Vulnerability alerts with severity badges
- Update recommendations
- Filter by severity/type
- Search functionality

### 7. Modernization Suggestions
**File**: `components/features/modernization/suggestion-cards.tsx`

**Features**:
- Card grid with suggestions
- Priority badge (High/Medium/Low)
- Effort indicator (1-5 scale)
- Expandable details
- Action steps checklist
- Impact description

### 8. Chatbot Panel
**File**: `components/features/chat/chatbot-panel.tsx`

**Features**:
- Fixed width (400px), full height
- Collapsible with toggle button
- Message history with scroll
- Input at bottom
- Code snippet rendering
- File reference links
- Typing indicator
- Auto-scroll to latest

## 🎯 Implementation Order

### Phase 1: Foundation (Tasks 1-3)
1. ✅ Create TypeScript type definitions
2. ✅ Build additional UI components (Tabs, Skeleton, Progress, Dialog, Collapsible)
3. ✅ Create animation wrapper components (FadeIn, SlideIn, ScaleIn, StaggerContainer)

### Phase 2: Layout & Navigation (Task 4)
4. ✅ Implement dashboard layout with header and tab navigation
   - Dashboard route at `/dashboard/[repoId]/page.tsx`
   - Dashboard layout component
   - Tab navigation with state management

### Phase 3: Summary Tab (Task 5)
5. ✅ Build repository summary section
   - Animated stats cards
   - Overview section
   - Quick insights panel

### Phase 4: Architecture Tab (Task 6)
6. ✅ Create React Flow architecture graph
   - Custom node components
   - Edge rendering
   - Controls and interactions
   - Node details panel

### Phase 5: Risk & Dependencies (Tasks 7-8)
7. ✅ Implement risk analysis section
   - Risk matrix visualization
   - Technical debt score
   - Risk breakdown cards

8. ✅ Build dependency metrics panel
   - Metrics overview
   - Outdated packages list
   - Vulnerability alerts

### Phase 6: Modernization (Task 9)
9. ✅ Create modernization suggestions
   - Suggestion cards
   - Priority matrix
   - Actionable steps

### Phase 7: Chat Integration (Task 10)
10. ✅ Implement collapsible chatbot panel
    - Chat header with toggle
    - Message list with history
    - Message input
    - Code snippet rendering

### Phase 8: Polish (Tasks 11-13)
11. ✅ Add loading states and skeleton screens
12. ✅ Create responsive layout
13. ✅ Add Framer Motion animations

### Phase 9: Data Integration (Tasks 14-15)
14. ✅ Implement API hooks
15. ✅ Integrate all components in dashboard route

## 🎨 UI/UX Guidelines

### Glassmorphism Effects
- Use `glass-card` class for main containers
- Add `glass-hover` for interactive elements
- Apply subtle borders with `border-white/10`
- Use backdrop blur for depth

### Color Usage
- **Primary gradient**: Buttons, active states
- **Success**: Positive metrics, completed items
- **Warning**: Outdated dependencies, medium risks
- **Error**: Vulnerabilities, critical risks
- **Info**: Informational badges, tips

### Spacing
- Card padding: `p-6`
- Section gaps: `gap-6`
- Grid gaps: `gap-4`
- Text spacing: `space-y-2`

### Responsive Breakpoints
- Mobile: `< 640px` - Stack layout, full width
- Tablet: `640px - 1024px` - 2-column grid
- Desktop: `> 1024px` - 3-column grid, side panel

### Loading States
- Skeleton screens for initial load
- Shimmer effect on placeholders
- Progress bar for long operations
- Spinner for button actions

### Animations
- Card entrance: Fade + slide up
- Tab transition: Fade + slide horizontal
- Hover effects: Scale + glow
- Stagger: 100ms delay between items

## 🔌 API Integration

### Endpoints
```typescript
// Repository data
GET /api/repositories/:id

// Analysis results
GET /api/repositories/:id/analysis

// Architecture data
GET /api/repositories/:id/architecture

// Dependencies
GET /api/repositories/:id/dependencies

// Risks
GET /api/repositories/:id/risks

// Modernization suggestions
GET /api/repositories/:id/modernization

// Chat
POST /api/repositories/:id/chat
GET /api/repositories/:id/chat/history
```

### React Query Hooks
```typescript
// Fetch repository
const { data: repository, isLoading } = useRepository(repoId);

// Fetch analysis
const { data: analysis } = useAnalysis(repoId);

// Fetch architecture
const { data: architecture } = useArchitecture(repoId);

// Chat mutation
const { mutate: sendMessage } = useChatMutation(repoId);
```

## ✅ Acceptance Criteria

### Functionality
- [ ] Dashboard loads with repository data
- [ ] All tabs are accessible and functional
- [ ] Architecture graph is interactive
- [ ] Risk matrix displays correctly
- [ ] Dependencies show update status
- [ ] Modernization suggestions are actionable
- [ ] Chatbot sends and receives messages
- [ ] All animations work smoothly

### Performance
- [ ] Initial load < 2 seconds
- [ ] Tab switching < 300ms
- [ ] Smooth 60fps animations
- [ ] No layout shifts

### Responsive Design
- [ ] Works on mobile (320px+)
- [ ] Works on tablet (768px+)
- [ ] Works on desktop (1024px+)
- [ ] Chatbot adapts to screen size

### Accessibility
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Color contrast meets WCAG AA
- [ ] Screen reader friendly

## 🚀 Next Steps

1. Review this plan and confirm approach
2. Switch to Code mode to begin implementation
3. Start with Phase 1 (Foundation)
4. Implement components incrementally
5. Test each component before moving forward
6. Integrate with backend API
7. Polish and optimize

---

**Ready to build?** Switch to Code mode and let's start implementing! 🎉