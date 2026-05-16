# LegacyMind AI - Frontend Folder Structure

## Complete Next.js 15 App Router Structure

```
frontend/
├── public/
│   ├── icons/
│   │   ├── github.svg
│   │   ├── logo.svg
│   │   └── favicon.ico
│   └── images/
│       └── hero-bg.png
│
├── src/
│   ├── app/
│   │   ├── (auth)/                    # Route group for authentication
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx
│   │   │
│   │   ├── (dashboard)/               # Route group for dashboard
│   │   │   ├── analyze/
│   │   │   │   └── page.tsx
│   │   │   ├── repository/
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx
│   │   │   │       ├── architecture/
│   │   │   │       │   └── page.tsx
│   │   │   │       ├── dependencies/
│   │   │   │       │   └── page.tsx
│   │   │   │       ├── risks/
│   │   │   │       │   └── page.tsx
│   │   │   │       └── chat/
│   │   │   │           └── page.tsx
│   │   │   └── layout.tsx
│   │   │
│   │   ├── api/                       # API routes (Next.js API routes)
│   │   │   └── health/
│   │   │       └── route.ts
│   │   │
│   │   ├── layout.tsx                 # Root layout
│   │   ├── page.tsx                   # Landing page
│   │   ├── globals.css                # Global styles
│   │   └── error.tsx                  # Error boundary
│   │
│   ├── components/
│   │   ├── ui/                        # Reusable UI components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── skeleton.tsx
│   │   │   ├── tabs.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── toast.tsx
│   │   │   └── progress.tsx
│   │   │
│   │   ├── layout/                    # Layout components
│   │   │   ├── header.tsx
│   │   │   ├── sidebar.tsx
│   │   │   ├── footer.tsx
│   │   │   └── navigation.tsx
│   │   │
│   │   ├── features/                  # Feature-specific components
│   │   │   ├── landing/
│   │   │   │   ├── hero-section.tsx
│   │   │   │   ├── features-section.tsx
│   │   │   │   └── cta-section.tsx
│   │   │   │
│   │   │   ├── repository/
│   │   │   │   ├── repo-input.tsx
│   │   │   │   ├── repo-card.tsx
│   │   │   │   ├── repo-stats.tsx
│   │   │   │   └── repo-summary.tsx
│   │   │   │
│   │   │   ├── analysis/
│   │   │   │   ├── analysis-dashboard.tsx
│   │   │   │   ├── dependency-graph.tsx
│   │   │   │   ├── risk-matrix.tsx
│   │   │   │   └── modernization-panel.tsx
│   │   │   │
│   │   │   ├── architecture/
│   │   │   │   ├── architecture-flow.tsx
│   │   │   │   ├── node-details.tsx
│   │   │   │   └── flow-controls.tsx
│   │   │   │
│   │   │   └── chat/
│   │   │       ├── chat-interface.tsx
│   │   │       ├── message-list.tsx
│   │   │       ├── message-input.tsx
│   │   │       └── code-snippet.tsx
│   │   │
│   │   ├── animations/                # Animation components
│   │   │   ├── fade-in.tsx
│   │   │   ├── slide-in.tsx
│   │   │   ├── scale-in.tsx
│   │   │   └── loading-spinner.tsx
│   │   │
│   │   └── providers/                 # Context providers
│   │       ├── theme-provider.tsx
│   │       ├── toast-provider.tsx
│   │       └── query-provider.tsx
│   │
│   ├── lib/                           # Utility libraries
│   │   ├── api/                       # API client layer
│   │   │   ├── client.ts
│   │   │   ├── endpoints.ts
│   │   │   └── types.ts
│   │   │
│   │   ├── hooks/                     # Custom React hooks
│   │   │   ├── use-repository.ts
│   │   │   ├── use-analysis.ts
│   │   │   ├── use-chat.ts
│   │   │   ├── use-debounce.ts
│   │   │   └── use-intersection-observer.ts
│   │   │
│   │   ├── utils/                     # Utility functions
│   │   │   ├── cn.ts                  # Class name merger
│   │   │   ├── format.ts              # Formatters
│   │   │   ├── validation.ts          # Validators
│   │   │   └── constants.ts           # Constants
│   │   │
│   │   └── animations/                # Animation utilities
│   │       ├── variants.ts            # Framer Motion variants
│   │       └── transitions.ts         # Transition configs
│   │
│   ├── types/                         # TypeScript types
│   │   ├── repository.ts
│   │   ├── analysis.ts
│   │   ├── chat.ts
│   │   └── api.ts
│   │
│   ├── styles/                        # Additional styles
│   │   ├── animations.css
│   │   └── glassmorphism.css
│   │
│   └── config/                        # Configuration files
│       ├── site.ts                    # Site metadata
│       └── api.ts                     # API configuration
│
├── .env.local                         # Environment variables
├── .env.example                       # Example env file
├── .eslintrc.json                     # ESLint config
├── .prettierrc                        # Prettier config
├── next.config.js                     # Next.js config
├── tailwind.config.ts                 # Tailwind config
├── tsconfig.json                      # TypeScript config
├── package.json                       # Dependencies
└── README.md                          # Documentation
```

## Folder Explanations

### 📁 `public/`
**Purpose**: Static assets served directly by Next.js
- `icons/`: SVG icons and favicon
- `images/`: Static images for hero sections, backgrounds

### 📁 `src/app/`
**Purpose**: Next.js 15 App Router directory (file-based routing)

#### Route Groups (parentheses don't affect URL)
- `(auth)/`: Authentication pages (login, signup)
- `(dashboard)/`: Protected dashboard routes
  - `analyze/`: Repository analysis page
  - `repository/[id]/`: Dynamic repository details
    - `architecture/`: Architecture visualization
    - `dependencies/`: Dependency analysis
    - `risks/`: Risk assessment
    - `chat/`: AI chatbot interface

#### Special Files
- `layout.tsx`: Root layout (wraps all pages)
- `page.tsx`: Landing page (/)
- `globals.css`: Global CSS and Tailwind directives
- `error.tsx`: Error boundary component

### 📁 `src/components/`
**Purpose**: Reusable React components organized by type

#### `ui/`
**Purpose**: Base UI components (design system)
- Atomic, reusable components
- No business logic
- Styled with Tailwind + glassmorphism
- Examples: Button, Card, Input, Badge

#### `layout/`
**Purpose**: Layout structure components
- Header with navigation
- Sidebar for dashboard
- Footer with links
- Responsive navigation

#### `features/`
**Purpose**: Feature-specific components (business logic)
- Organized by feature domain
- Contains complex, composed components
- Examples:
  - `landing/`: Landing page sections
  - `repository/`: Repo input and display
  - `analysis/`: Analysis dashboards
  - `architecture/`: React Flow visualizations
  - `chat/`: Chat interface components

#### `animations/`
**Purpose**: Reusable animation wrapper components
- Framer Motion wrappers
- Fade, slide, scale animations
- Loading states

#### `providers/`
**Purpose**: React Context providers
- Theme provider (dark mode)
- Toast notifications
- React Query provider

### 📁 `src/lib/`
**Purpose**: Core utilities and business logic

#### `api/`
**Purpose**: API client layer (communicates with FastAPI backend)
- `client.ts`: Axios/Fetch wrapper with interceptors
- `endpoints.ts`: API endpoint definitions
- `types.ts`: API request/response types

#### `hooks/`
**Purpose**: Custom React hooks
- `use-repository.ts`: Repository data fetching
- `use-analysis.ts`: Analysis data management
- `use-chat.ts`: Chat functionality
- `use-debounce.ts`: Input debouncing
- `use-intersection-observer.ts`: Lazy loading

#### `utils/`
**Purpose**: Pure utility functions
- `cn.ts`: Class name merger (clsx + tailwind-merge)
- `format.ts`: Date, number, text formatters
- `validation.ts`: Input validators
- `constants.ts`: App-wide constants

#### `animations/`
**Purpose**: Framer Motion configuration
- `variants.ts`: Reusable animation variants
- `transitions.ts`: Transition configurations

### 📁 `src/types/`
**Purpose**: TypeScript type definitions
- `repository.ts`: Repository data types
- `analysis.ts`: Analysis result types
- `chat.ts`: Chat message types
- `api.ts`: API response types

### 📁 `src/styles/`
**Purpose**: Additional CSS files
- `animations.css`: Custom CSS animations
- `glassmorphism.css`: Glassmorphism effects

### 📁 `src/config/`
**Purpose**: Configuration files
- `site.ts`: Site metadata, SEO
- `api.ts`: API base URLs, timeouts

## Naming Conventions

### Files
- **Components**: `kebab-case.tsx` (e.g., `repo-input.tsx`)
- **Utilities**: `kebab-case.ts` (e.g., `use-repository.ts`)
- **Types**: `kebab-case.ts` (e.g., `repository.ts`)
- **Pages**: `page.tsx` (Next.js convention)
- **Layouts**: `layout.tsx` (Next.js convention)

### Components
- **PascalCase**: `RepoInput`, `AnalysisDashboard`
- **Prefixes**:
  - `use-`: Custom hooks (e.g., `useRepository`)
  - No prefix for components

### Variables
- **camelCase**: `repoData`, `analysisResults`
- **UPPER_SNAKE_CASE**: Constants (e.g., `API_BASE_URL`)

### Types/Interfaces
- **PascalCase**: `Repository`, `AnalysisResult`
- **Suffix**: `Type` for type aliases, `Interface` optional

## Key Architecture Decisions

### 1. **Route Groups**
Using `(auth)` and `(dashboard)` to organize routes without affecting URLs

### 2. **Feature-Based Components**
Components organized by feature domain for better scalability

### 3. **API Service Layer**
Centralized API client in `lib/api/` for consistent backend communication

### 4. **Custom Hooks**
Business logic extracted into hooks for reusability

### 5. **Type Safety**
Dedicated `types/` folder for shared TypeScript definitions

### 6. **Animation Utilities**
Centralized Framer Motion configurations for consistent animations

### 7. **Glassmorphism Design**
Custom CSS in `styles/` for dark glassmorphism effects

## Next Steps

1. Initialize Next.js project with TypeScript
2. Install dependencies (Tailwind, Framer Motion, React Flow)
3. Set up folder structure
4. Create base UI components
5. Implement API client layer
6. Build feature components
7. Add animations and transitions
8. Configure deployment for Vercel

This structure supports:
- ✅ Scalability (feature-based organization)
- ✅ Reusability (atomic UI components)
- ✅ Type safety (TypeScript throughout)
- ✅ Performance (Next.js 15 optimizations)
- ✅ Developer experience (clear conventions)