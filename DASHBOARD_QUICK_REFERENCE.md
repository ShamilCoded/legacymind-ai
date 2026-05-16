# Dashboard Implementation - Quick Reference Guide

## 🚀 Quick Start Checklist

### Prerequisites
- ✅ Next.js 15 project initialized
- ✅ Tailwind CSS configured
- ✅ Framer Motion installed
- ✅ React Flow installed
- ✅ Base UI components created
- ✅ Glassmorphism styles ready

### Implementation Phases

#### Phase 1: Types & Foundation
```bash
# Create type definitions
frontend/src/types/repository.ts
frontend/src/types/analysis.ts
frontend/src/types/architecture.ts
frontend/src/types/risk.ts
frontend/src/types/dependency.ts
frontend/src/types/chat.ts

# Create base UI components
frontend/src/components/ui/tabs.tsx
frontend/src/components/ui/skeleton.tsx
frontend/src/components/ui/progress.tsx
frontend/src/components/ui/dialog.tsx
frontend/src/components/ui/collapsible.tsx

# Create animation wrappers
frontend/src/components/animations/fade-in.tsx
frontend/src/components/animations/slide-in.tsx
frontend/src/components/animations/scale-in.tsx
frontend/src/components/animations/stagger-container.tsx
```

#### Phase 2: Dashboard Layout
```bash
# Create dashboard structure
frontend/src/app/dashboard/[repoId]/page.tsx
frontend/src/app/dashboard/[repoId]/layout.tsx

# Create layout components
frontend/src/components/features/dashboard/dashboard-layout.tsx
frontend/src/components/features/dashboard/dashboard-header.tsx
frontend/src/components/features/dashboard/tab-navigation.tsx
```

#### Phase 3: Tab Components
```bash
# Summary tab
frontend/src/components/features/summary/repo-stats-cards.tsx
frontend/src/components/features/summary/overview-section.tsx
frontend/src/components/features/summary/quick-insights.tsx

# Architecture tab
frontend/src/components/features/architecture/architecture-flow.tsx
frontend/src/components/features/architecture/custom-nodes.tsx
frontend/src/components/features/architecture/node-details-panel.tsx
frontend/src/components/features/architecture/flow-controls.tsx

# Dependencies tab
frontend/src/components/features/dependencies/dependency-metrics.tsx
frontend/src/components/features/dependencies/outdated-packages.tsx
frontend/src/components/features/dependencies/vulnerability-alerts.tsx

# Risks tab
frontend/src/components/features/risks/risk-matrix.tsx
frontend/src/components/features/risks/technical-debt-score.tsx
frontend/src/components/features/risks/risk-breakdown.tsx

# Modernization tab
frontend/src/components/features/modernization/suggestion-cards.tsx
frontend/src/components/features/modernization/priority-matrix.tsx
frontend/src/components/features/modernization/actionable-steps.tsx
```

#### Phase 4: Chat Integration
```bash
# Chat components
frontend/src/components/features/chat/chatbot-panel.tsx
frontend/src/components/features/chat/chat-header.tsx
frontend/src/components/features/chat/message-list.tsx
frontend/src/components/features/chat/message-bubble.tsx
frontend/src/components/features/chat/message-input.tsx
frontend/src/components/features/chat/code-snippet.tsx
```

#### Phase 5: Data Hooks
```bash
# API hooks
frontend/src/lib/hooks/use-repository.ts
frontend/src/lib/hooks/use-analysis.ts
frontend/src/lib/hooks/use-architecture.ts
frontend/src/lib/hooks/use-dependencies.ts
frontend/src/lib/hooks/use-risks.ts
frontend/src/lib/hooks/use-modernization.ts
frontend/src/lib/hooks/use-chat.ts
frontend/src/lib/hooks/use-tab-state.ts
```

## 📝 Code Snippets

### Type Definition Template
```typescript
// frontend/src/types/[feature].ts
export interface [FeatureName] {
  id: string;
  // Add properties
}

export interface [FeatureName]Data {
  // Add data structure
}
```

### UI Component Template
```typescript
// frontend/src/components/ui/[component].tsx
import React from 'react';
import { cn } from '@/lib/utils/cn';

export interface [Component]Props extends React.HTMLAttributes<HTMLDivElement> {
  // Add props
}

export const [Component] = React.forwardRef<HTMLDivElement, [Component]Props>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn('base-styles', className)}
        {...props}
      />
    );
  }
);

[Component].displayName = '[Component]';
```

### Animation Wrapper Template
```typescript
// frontend/src/components/animations/[animation].tsx
'use client';

import { motion } from 'framer-motion';
import React from 'react';

interface [Animation]Props {
  children: React.ReactNode;
  delay?: number;
  className?: string;
}

export const [Animation]: React.FC<[Animation]Props> = ({
  children,
  delay = 0,
  className,
}) => {
  return (
    <motion.div
      initial={{ /* initial state */ }}
      animate={{ /* animate state */ }}
      transition={{ delay, duration: 0.4, ease: [0.4, 0, 0.2, 1] }}
      className={className}
    >
      {children}
    </motion.div>
  );
};
```

### Feature Component Template
```typescript
// frontend/src/components/features/[feature]/[component].tsx
'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { FadeIn } from '@/components/animations/fade-in';

interface [Component]Props {
  data: [DataType];
}

export const [Component]: React.FC<[Component]Props> = ({ data }) => {
  return (
    <FadeIn>
      <Card>
        <CardHeader>
          <CardTitle>[Title]</CardTitle>
        </CardHeader>
        <CardContent>
          {/* Component content */}
        </CardContent>
      </Card>
    </FadeIn>
  );
};
```

### React Query Hook Template
```typescript
// frontend/src/lib/hooks/use-[feature].ts
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

export const use[Feature] = (repoId: string) => {
  return useQuery({
    queryKey: ['[feature]', repoId],
    queryFn: async () => {
      const { data } = await axios.get(`/api/repositories/${repoId}/[feature]`);
      return data;
    },
    enabled: !!repoId,
  });
};
```

## 🎨 Common Patterns

### Glassmorphism Card
```tsx
<div className="glass-card p-6 hover:glass-hover">
  {/* Content */}
</div>
```

### Animated Stats Card
```tsx
<FadeIn delay={index * 0.1}>
  <Card hover glow>
    <CardContent className="flex items-center gap-4">
      <div className="p-3 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600">
        <Icon className="w-6 h-6 text-white" />
      </div>
      <div>
        <p className="text-3xl font-bold text-white">{value}</p>
        <p className="text-sm text-slate-400">{label}</p>
      </div>
    </CardContent>
  </Card>
</FadeIn>
```

### Tab Navigation
```tsx
<div className="glass-card p-2">
  <div className="flex gap-2">
    {tabs.map((tab) => (
      <button
        key={tab.id}
        onClick={() => setActiveTab(tab.id)}
        className={cn(
          'px-4 py-2 rounded-lg transition-all',
          activeTab === tab.id
            ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white'
            : 'text-slate-400 hover:text-white hover:bg-white/5'
        )}
      >
        {tab.label}
      </button>
    ))}
  </div>
</div>
```

### Loading Skeleton
```tsx
{isLoading ? (
  <div className="space-y-4">
    <Skeleton className="h-24 w-full" />
    <Skeleton className="h-24 w-full" />
    <Skeleton className="h-24 w-full" />
  </div>
) : (
  <div>{/* Actual content */}</div>
)}
```

### Collapsible Panel
```tsx
<motion.div
  initial={false}
  animate={isOpen ? 'open' : 'closed'}
  variants={{
    open: { x: 0 },
    closed: { x: '100%' }
  }}
  className="fixed right-0 top-0 h-full w-96 glass-card"
>
  {/* Panel content */}
</motion.div>
```

## 🎯 Key Features Implementation

### 1. Repository Stats Cards
```typescript
const stats = [
  { icon: FileCode, label: 'Total Files', value: data.totalFiles },
  { icon: Code, label: 'Lines of Code', value: data.totalLines },
  { icon: Star, label: 'Quality Score', value: data.qualityScore },
  { icon: Clock, label: 'Tech Debt', value: `${data.debtHours}h` },
];

return (
  <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    {stats.map((stat, index) => (
      <StatCard key={stat.label} {...stat} delay={index * 0.1} />
    ))}
  </StaggerContainer>
);
```

### 2. React Flow Architecture
```typescript
const nodes = architectureData.modules.map((module) => ({
  id: module.id,
  type: 'custom',
  position: { x: module.x, y: module.y },
  data: { label: module.name, type: module.type },
}));

const edges = architectureData.relationships.map((rel) => ({
  id: `${rel.source}-${rel.target}`,
  source: rel.source,
  target: rel.target,
  animated: true,
}));

return (
  <ReactFlow
    nodes={nodes}
    edges={edges}
    nodeTypes={nodeTypes}
    fitView
  />
);
```

### 3. Risk Matrix
```typescript
const quadrants = [
  { severity: 'low', impact: 'low', color: 'bg-emerald-500/20' },
  { severity: 'low', impact: 'high', color: 'bg-amber-500/20' },
  { severity: 'high', impact: 'low', color: 'bg-orange-500/20' },
  { severity: 'high', impact: 'high', color: 'bg-red-500/20' },
];

return (
  <div className="grid grid-cols-2 gap-4">
    {quadrants.map((quadrant) => (
      <div key={`${quadrant.severity}-${quadrant.impact}`} 
           className={cn('p-6 rounded-lg', quadrant.color)}>
        {/* Risk items */}
      </div>
    ))}
  </div>
);
```

### 4. Chat Interface
```typescript
const [messages, setMessages] = useState<ChatMessage[]>([]);
const { mutate: sendMessage } = useChatMutation(repoId);

const handleSend = (content: string) => {
  sendMessage({ content }, {
    onSuccess: (response) => {
      setMessages([...messages, response]);
    },
  });
};

return (
  <div className="flex flex-col h-full">
    <MessageList messages={messages} />
    <MessageInput onSend={handleSend} />
  </div>
);
```

## 🔧 Utility Functions

### Format Numbers
```typescript
export const formatNumber = (num: number): string => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
  return num.toString();
};
```

### Get Severity Color
```typescript
export const getSeverityColor = (severity: string): string => {
  const colors = {
    low: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
    medium: 'text-amber-400 bg-amber-500/10 border-amber-500/30',
    high: 'text-orange-400 bg-orange-500/10 border-orange-500/30',
    critical: 'text-red-400 bg-red-500/10 border-red-500/30',
  };
  return colors[severity] || colors.low;
};
```

### Format Date
```typescript
export const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};
```

## 📱 Responsive Utilities

### Breakpoint Hook
```typescript
export const useBreakpoint = () => {
  const [breakpoint, setBreakpoint] = useState('desktop');

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 640) setBreakpoint('mobile');
      else if (window.innerWidth < 1024) setBreakpoint('tablet');
      else setBreakpoint('desktop');
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return breakpoint;
};
```

## 🎬 Animation Variants

### Card Variants
```typescript
export const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.4, ease: [0.4, 0, 0.2, 1] }
  },
};
```

### Stagger Variants
```typescript
export const staggerContainerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};
```

### Tab Variants
```typescript
export const tabContentVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: { 
    opacity: 1, 
    x: 0,
    transition: { duration: 0.3, ease: 'easeOut' }
  },
  exit: { 
    opacity: 0, 
    x: 20,
    transition: { duration: 0.2 }
  },
};
```

## ✅ Testing Checklist

### Component Tests
- [ ] All UI components render correctly
- [ ] Props are properly typed
- [ ] Animations work smoothly
- [ ] Responsive behavior is correct

### Integration Tests
- [ ] Tab navigation works
- [ ] Data fetching works
- [ ] Chat sends/receives messages
- [ ] Graph interactions work

### Visual Tests
- [ ] Glassmorphism effects display
- [ ] Colors match design system
- [ ] Spacing is consistent
- [ ] Loading states show properly

### Performance Tests
- [ ] Initial load < 2s
- [ ] Tab switching < 300ms
- [ ] Animations run at 60fps
- [ ] No memory leaks

## 🚀 Deployment Checklist

- [ ] All TypeScript errors resolved
- [ ] All ESLint warnings fixed
- [ ] Environment variables configured
- [ ] API endpoints tested
- [ ] Build succeeds locally
- [ ] Preview deployment works
- [ ] Production deployment successful

---

**Ready to implement?** Use this guide as a reference while building! 🎉